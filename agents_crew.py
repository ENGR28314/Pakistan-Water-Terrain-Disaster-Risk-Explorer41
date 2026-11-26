"""
agents_crew.py
Agentic analysis for every sector of the dashboard.

Two modes, same output format (insights + chart specs):

1. Rule-based agents (default, no API key, works offline):
       Profiler -> Analyst -> Chart Planner -> Reviewer
   Every number they report is computed from the data table of the sector.

2. CrewAI crew (optional, needs `pip install crewai` and your own LLM API key):
       Data Analyst + Domain Reviewer + Chart Planner + Briefing Writer
   The agents get tools that read the sector table (describe / top-N / value counts /
   correlation). The Chart Planner must answer with JSON chart specs; the specs are
   validated against the real columns before anything is drawn, and the rule-based
   planner is used if the LLM's answer is unusable.

This module has no Streamlit code (see agents_ui.py) so it can be tested on its own.
Chart types supported: bar, pie, scatter, line, histogram.
"""
from __future__ import annotations

import json
import re
import time
from typing import Callable, Dict, List, Optional

import pandas as pd

import data_loader as d
import energy_minerals as em
import army_role as ar

CHART_TYPES = ["bar", "pie", "scatter", "line", "histogram"]
EVIDENCE_COL = "Evidence"


# ---------------------------------------------------------------------------
# Sector tables (built from the dashboard's own data modules)
# ---------------------------------------------------------------------------
def _dams() -> pd.DataFrame:
    rows = [{"Name": k, "Type": v.get("type"), "River": v.get("river"), "Province": v.get("province"),
             "Year completed": v.get("year_completed"), "Capacity (MW)": v.get("capacity_MW")}
            for k, v in d.DAMS_BARRAGES.items()]
    return pd.DataFrame(rows)


def _rivers() -> pd.DataFrame:
    rows = [{"Name": k, "Length (km)": v.get("length_km"),
             "Provinces (count)": len(v.get("provinces", []) or []),
             "Confluences (count)": len(v.get("confluences", []) or []),
             "Dams/barrages (count)": len(v.get("dams_barrages", []) or [])}
            for k, v in d.RIVERS.items()]
    return pd.DataFrame(rows)


def _provinces() -> pd.DataFrame:
    rows = [{"Name": k, "Area (km²)": v.get("area_km2"), "Capital": v.get("capital"),
             "Major rivers (count)": len(v.get("major_rivers", []) or [])}
            for k, v in d.PROVINCES.items()]
    return pd.DataFrame(rows)


def _deserts() -> pd.DataFrame:
    return pd.DataFrame([{"Name": k, "Province": v.get("province"), "Area (km²)": v.get("area_km2"),
                          "Type": v.get("type")} for k, v in d.DESERTS.items()])


def _lakes() -> pd.DataFrame:
    return pd.DataFrame([{"Name": k, "Province": v.get("province"), "Type": v.get("type")}
                         for k, v in d.LAKES.items()])


def _parks() -> pd.DataFrame:
    return pd.DataFrame([{"Name": k, "Province": v.get("province"), "Type": v.get("type")}
                         for k, v in d.NATIONAL_PARKS.items()])


def _forests() -> pd.DataFrame:
    return pd.DataFrame([{"Name": k, "Forest type": v.get("forest_type"),
                          "Location": str(v.get("location", ""))[:60]}
                         for k, v in d.NOTABLE_FORESTS.items()])


def _climate() -> pd.DataFrame:
    return pd.DataFrame([{"Region": k, "Areas (count)": len(v.get("areas", []) or [])}
                         for k, v in d.CLIMATIC_REGIONS.items()])


def _mountains() -> pd.DataFrame:
    rows = []
    for group in d.MOUNTAIN_RANGES.values():
        for rng, v in group.items():
            for p in v.get("other_notable_peaks", []) or []:
                rows.append({"Peak": p.get("name"), "Range": rng, "Elevation (m)": p.get("elevation_m")})
    return pd.DataFrame(rows)


def _links() -> pd.DataFrame:
    return pd.DataFrame([{"Name": k, "Province": v.get("province"), "Connects": v.get("connects")}
                         for k, v in d.LINK_CANALS.items()])


def _disasters() -> pd.DataFrame:
    return pd.DataFrame([{"Year": e.get("year"), "Event": e.get("name"), "Hazard type": e.get("hazard_type"),
                          "Provinces affected (count)": len(e.get("provinces", []) or [])}
                         for e in d.DISASTER_HISTORICAL_EVENTS])


def _hazards_by_province() -> pd.DataFrame:
    return pd.DataFrame([{"Province": k, "Hazards listed (count)": len(v)}
                         for k, v in d.DISASTER_HAZARD_BY_PROVINCE.items()])


def _delta() -> pd.DataFrame:
    return pd.DataFrame(d.INDUS_DELTA_SAMPLE_SITES).rename(
        columns={"site": "Site", "district": "District", "EC_dS_per_m": "EC (dS/m)", "ESP_pct": "ESP (%)",
                 "classification": "Classification"})


def _agro() -> pd.DataFrame:
    return pd.DataFrame(d.REGIONAL_AGRO_SOCIO_DATA)


def _cpec() -> pd.DataFrame:
    proj = d.CHINA_HYDROPOWER_FOOTPRINT.get("Major Hydropower Asset Portfolio", {})
    return pd.DataFrame([{"Project": k, "Capacity (MW)": v.get("capacity_MW"), "River": v.get("river"),
                          "Status": v.get("status")} for k, v in proj.items()])


def _india() -> pd.DataFrame:
    return pd.DataFrame([{"Project": k, "Capacity (MW)": v.get("capacity_MW"), "River": v.get("river")}
                         for k, v in d.INDIA_DAM_DESIGN_DISPUTES.items()])


def _text_sector(sectors: Dict[str, dict]) -> pd.DataFrame:
    rows = []
    for tab, v in sectors.items():
        for txt, tag in v.get("points", []):
            rows.append({"Tab": tab, "Finding": txt, EVIDENCE_COL: tag, "Words": len(str(txt).split()),
                         "Numbers cited": len(re.findall(r"\d[\d,\.]*", str(txt)))})
    return pd.DataFrame(rows)


def _army() -> pd.DataFrame:
    return _text_sector(ar.SECTORS)


SECTOR_BUILDERS: Dict[str, Callable[[], pd.DataFrame]] = {
    "Provinces": _provinces,
    "Rivers": _rivers,
    "Dams & Barrages": _dams,
    "Link Canals": _links,
    "Climatic Regions": _climate,
    "Mountain Ranges (peaks)": _mountains,
    "Lakes": _lakes,
    "Deserts": _deserts,
    "Forests": _forests,
    "National Parks": _parks,
    "Indus Delta Soil Salinity": _delta,
    "Disaster Risk — historical events": _disasters,
    "Disaster Risk — hazards by province": _hazards_by_province,
    "Socio-Economic & Agro-Economic": _agro,
    "China Hydropower (CPEC)": _cpec,
    "Chenab / India Projects": _india,
    "Pakistan Army's Role": _army,
    "Solar Energy": lambda: _text_sector(em.SOLAR),
    "Mining": lambda: _text_sector(em.MINING),
    "Dry Fruit": lambda: _text_sector(em.DRYFRUIT),
}

# Dashboard section -> sector table(s) it should offer
SECTION_TO_SECTORS: Dict[str, List[str]] = {
    "🗺️ Provinces": ["Provinces"],
    "🌊 Rivers": ["Rivers"],
    "🚧 Dams & Barrages": ["Dams & Barrages"],
    "🔀 Link Canals": ["Link Canals"],
    "🌡️ Climatic Regions": ["Climatic Regions"],
    "⛰️ Mountain Ranges": ["Mountain Ranges (peaks)"],
    "🏞️ Lakes": ["Lakes"],
    "🏜️ Deserts": ["Deserts"],
    "🌲 Forests": ["Forests"],
    "🌳 National Parks": ["National Parks"],
    "🧂 Indus Delta Soil Salinity (EMI Survey)": ["Indus Delta Soil Salinity"],
    "⚠️ Disaster Risk Context": ["Disaster Risk — historical events", "Disaster Risk — hazards by province"],
    "📈 Socio-Economic & Agro-Economic": ["Socio-Economic & Agro-Economic"],
    "🇨🇳 China Hydropower (CPEC)": ["China Hydropower (CPEC)"],
    "🇮🇳 Chenab Projects, Flow Concerns & Indus Waters Treaty": ["Chenab / India Projects"],
    "🪖 Pakistan Army's Role Across Sectors": ["Pakistan Army's Role"],
    "☀️ Solar Energy Sectors": ["Solar Energy"],
    "⛏️ Mining Sectors": ["Mining"],
    "🥜 Dry Fruit Sector": ["Dry Fruit"],
}


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Turn text columns that are mostly numbers (e.g. '1976', '2,300') into numeric columns."""
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object:
            s = pd.to_numeric(df[c].astype(str).str.replace(",", "", regex=False), errors="coerce")
            if len(df) and s.notna().mean() >= 0.7:
                df[c] = s
    return df


def load_sector(name: str) -> pd.DataFrame:
    return coerce_numeric(SECTOR_BUILDERS[name]()).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Column roles
# ---------------------------------------------------------------------------
def _roles(df: pd.DataFrame) -> dict:
    n = len(df)
    nums, cats, ident, year = [], [], None, None
    for c in df.columns:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            if s.nunique(dropna=True) <= 1:
                continue
            if "year" in str(c).lower():
                year = year or c
            nums.append(c)
        else:
            u = s.astype(str).nunique()
            avg = s.astype(str).str.len().mean() if n else 0
            if u == n and n > 1 and ident is None and avg < 70:
                ident = c
            elif 2 <= u <= max(12, n // 2) and avg < 60:
                cats.append(c)
    nums_noyear = [c for c in nums if c != year]
    return {"nums": nums_noyear, "cats": cats, "id": ident, "year": year}


# ---------------------------------------------------------------------------
# Agent 1: Profiler
# ---------------------------------------------------------------------------
def profile(df: pd.DataFrame) -> dict:
    r = _roles(df)
    miss = int(df.isna().sum().sum())
    stats = {}
    for c in r["nums"] + ([r["year"]] if r["year"] else []):
        s = pd.to_numeric(df[c], errors="coerce").dropna()
        if len(s):
            stats[c] = {"min": float(s.min()), "max": float(s.max()), "mean": float(s.mean()),
                        "median": float(s.median()), "sum": float(s.sum())}
    return {"rows": len(df), "columns": list(df.columns), "roles": r, "missing_cells": miss, "stats": stats}


def profile_text(df: pd.DataFrame, max_rows: int = 40) -> str:
    p = profile(df)
    head = df.head(max_rows).to_csv(index=False)
    return (f"Rows: {p['rows']}\nColumns: {', '.join(p['columns'])}\nNumeric: {p['roles']['nums']}\n"
            f"Categorical: {p['roles']['cats']}\nIdentifier column: {p['roles']['id']}\n"
            f"Year column: {p['roles']['year']}\nSummary stats: {json.dumps(p['stats'])}\n"
            f"First rows (CSV):\n{head}")


# ---------------------------------------------------------------------------
# Agent 2: Analyst (facts computed from the table only)
# ---------------------------------------------------------------------------
def _fmt(x: float) -> str:
    return f"{x:,.0f}" if abs(x) >= 100 else f"{x:,.2f}".rstrip("0").rstrip(".")


def analyse(df: pd.DataFrame) -> List[str]:
    r = _roles(df)
    out: List[str] = [f"The table has {len(df)} records and {len(df.columns)} columns."]
    ident = r["id"]
    for c in r["nums"][:3]:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() < 2:
            continue
        top = s.idxmax()
        label = df.loc[top, ident] if ident else f"row {top + 1}"
        share = s.max() / s.sum() * 100 if s.sum() else 0
        out.append(f"**{c}**: highest is {label} ({_fmt(s.max())}); median {_fmt(s.median())}, "
                   f"mean {_fmt(s.mean())}; top record = {share:.0f}% of the total.")
        q1, q3 = s.quantile(.25), s.quantile(.75)
        iqr = q3 - q1
        if iqr > 0:
            o = df[(s > q3 + 1.5 * iqr) | (s < q1 - 1.5 * iqr)]
            if len(o):
                names = ", ".join(str(x) for x in list(o[ident] if ident else (o.index + 1))[:5])
                out.append(f"Outliers in **{c}** (1.5×IQR rule): {names}.")
    if len(r["nums"]) >= 2:
        num = df[r["nums"]].apply(pd.to_numeric, errors="coerce")
        cm = num.corr().abs()
        best, pair = 0.0, None
        for i, a in enumerate(cm.columns):
            for b in cm.columns[i + 1:]:
                v = cm.loc[a, b]
                if pd.notna(v) and v > best and num[[a, b]].dropna().shape[0] >= 5:
                    best, pair = v, (a, b)
        if pair:
            sign = num[pair[0]].corr(num[pair[1]])
            out.append(f"Strongest numeric relationship: **{pair[0]}** vs **{pair[1]}** "
                       f"(correlation {sign:+.2f}, n={num[list(pair)].dropna().shape[0]}).")
    for c in r["cats"][:2]:
        vc = df[c].astype(str).value_counts()
        out.append(f"Most common **{c}**: {vc.index[0]} ({vc.iloc[0]} of {len(df)} records, "
                   f"{vc.iloc[0] / len(df) * 100:.0f}%).")
    if r["year"]:
        y = pd.to_numeric(df[r["year"]], errors="coerce").dropna()
        if len(y):
            out.append(f"Time span in **{r['year']}**: {int(y.min())}–{int(y.max())}.")
    if EVIDENCE_COL in df.columns:
        vc = df[EVIDENCE_COL].value_counts()
        ver = int(sum(v for k, v in vc.items() if "verify" in str(k).lower()))
        out.append(f"Evidence labels: " + ", ".join(f"{k}: {v}" for k, v in vc.items())
                   + f" — {ver} of {len(df)} findings still need verification.")
    return out


# ---------------------------------------------------------------------------
# Agent 3: Chart Planner (rule-based)
# ---------------------------------------------------------------------------
def plan_charts(df: pd.DataFrame, allowed: Optional[List[str]] = None, top_n: int = 15) -> List[dict]:
    allowed = allowed or CHART_TYPES
    r = _roles(df)
    nums, cats, ident, year = r["nums"], r["cats"], r["id"], r["year"]
    specs: List[dict] = []
    if "bar" in allowed:
        if ident and nums:
            specs.append({"chart": "bar", "x": ident, "y": nums[0], "agg": "sum",
                          "title": f"{nums[0]} by {ident} (top {top_n})", "top_n": top_n})
        elif cats:
            specs.append({"chart": "bar", "x": cats[0], "y": None, "agg": "count",
                          "title": f"Records per {cats[0]}"})
        if cats and nums and len(specs) < 2:
            specs.append({"chart": "bar", "x": cats[0], "y": nums[0], "agg": "sum",
                          "title": f"Total {nums[0]} per {cats[0]}"})
    if "pie" in allowed:
        if cats:
            specs.append({"chart": "pie", "x": cats[0], "y": None, "agg": "count",
                          "title": f"Share of records by {cats[0]}"})
        elif ident and nums:
            specs.append({"chart": "pie", "x": ident, "y": nums[0], "agg": "sum",
                          "title": f"Share of {nums[0]} by {ident}" + (" (top 8 + other)" if len(df) > 9 else "")})
    if "scatter" in allowed and len(nums) >= 2 and len(df) >= 5:
        specs.append({"chart": "scatter", "x": nums[0], "y": nums[1], "color": cats[0] if cats else None,
                      "hover": ident, "title": f"{nums[1]} vs {nums[0]}"})
    elif "scatter" in allowed and year and nums:
        specs.append({"chart": "scatter", "x": year, "y": nums[0], "color": cats[0] if cats else None,
                      "hover": ident, "title": f"{nums[0]} vs {year}"})
    if "line" in allowed:
        if year and nums:
            specs.append({"chart": "line", "x": year, "y": nums[0], "agg": "cumsum",
                          "title": f"Cumulative {nums[0]} over {year}"})
        elif year:
            specs.append({"chart": "line", "x": year, "y": None, "agg": "count",
                          "title": f"Records per {year}"})
        elif ident and nums:
            specs.append({"chart": "line", "x": ident, "y": nums[0], "agg": "sorted",
                          "title": f"{nums[0]} ranked (sorted line)"})
    if "histogram" in allowed:
        if nums:
            specs.append({"chart": "histogram", "x": nums[0], "title": f"Distribution of {nums[0]}"})
        elif "Words" in df.columns:
            specs.append({"chart": "histogram", "x": "Words", "title": "Distribution of finding length (words)"})
    # make sure every requested type appears at least once when a fallback exists
    if "histogram" in allowed and not any(s["chart"] == "histogram" for s in specs):
        if year:
            specs.append({"chart": "histogram", "x": year, "title": f"Distribution of {year}"})
        elif cats:
            specs.append({"chart": "histogram", "x": cats[0], "of_counts": True,
                          "title": f"How many records per {cats[0]} value (distribution of counts)"})
    if "line" in allowed and not any(s["chart"] == "line" for s in specs) and cats:
        specs.append({"chart": "line", "x": cats[0], "y": None, "agg": "count_sorted",
                      "title": f"Records per {cats[0]} (ranked)"})
    return specs


# ---------------------------------------------------------------------------
# Spec validation + rendering (plotly)
# ---------------------------------------------------------------------------
def validate_specs(df: pd.DataFrame, specs) -> List[dict]:
    good = []
    if not isinstance(specs, list):
        return good
    cols = set(df.columns)
    for s in specs:
        if not isinstance(s, dict) or s.get("chart") not in CHART_TYPES:
            continue
        x, y = s.get("x"), s.get("y")
        if x not in cols or (y is not None and y not in cols):
            continue
        if s["chart"] in ("scatter",) and (y is None or not pd.api.types.is_numeric_dtype(df[y])
                                           or not pd.api.types.is_numeric_dtype(df[x])):
            continue
        if s["chart"] == "histogram" and not s.get("of_counts") and not pd.api.types.is_numeric_dtype(df[x]):
            continue
        if s["chart"] in ("bar", "line") and y is not None and not pd.api.types.is_numeric_dtype(df[y]):
            continue
        for k in ("color", "hover"):
            if s.get(k) not in cols:
                s[k] = None
        s["title"] = str(s.get("title") or f"{s['chart'].title()} of {x}")[:90]
        good.append(s)
    return good


def build_figure(df: pd.DataFrame, spec: dict):
    import plotly.express as px
    kind, x, y = spec["chart"], spec["x"], spec.get("y")
    title = spec.get("title", "")
    agg = spec.get("agg", "sum")
    if kind == "histogram":
        if spec.get("of_counts"):
            t = df[x].astype(str).value_counts().reset_index()
            t.columns = [x, "Records"]
            return px.histogram(t, x="Records", nbins=spec.get("bins", 8), title=title)
        return px.histogram(df, x=x, nbins=spec.get("bins", 12), title=title)
    if kind == "scatter":
        return px.scatter(df, x=x, y=y, color=spec.get("color"), hover_name=spec.get("hover"), title=title)
    if kind == "pie":
        if y is None:
            t = df[x].astype(str).value_counts().reset_index()
            t.columns = [x, "Count"]
            return px.pie(t, names=x, values="Count", title=title)
        t = df.groupby(x, dropna=True)[y].sum().reset_index().sort_values(y, ascending=False)
        if len(t) > 9:
            other = t.iloc[8:][y].sum()
            t = pd.concat([t.head(8), pd.DataFrame({x: ["Other"], y: [other]})], ignore_index=True)
        return px.pie(t, names=x, values=y, title=title)
    if kind == "line":
        if agg == "cumsum" and y:
            t = df.groupby(x)[y].sum().sort_index().cumsum().reset_index()
            return px.line(t, x=x, y=y, markers=True, title=title)
        if agg == "count_sorted":
            t = df[x].astype(str).value_counts().reset_index()
            t.columns = [x, "Count"]
            return px.line(t, x=x, y="Count", markers=True, title=title)
        if agg == "count":
            t = df.groupby(x).size().reset_index(name="Count").sort_values(x)
            return px.line(t, x=x, y="Count", markers=True, title=title)
        t = df[[x, y]].dropna().sort_values(y, ascending=False)
        return px.line(t, x=x, y=y, markers=True, title=title)
    # bar
    top_n = int(spec.get("top_n", 15))
    if y is None or agg == "count":
        t = df[x].astype(str).value_counts().reset_index()
        t.columns = [x, "Count"]
        return px.bar(t.head(top_n), x=x, y="Count", title=title)
    t = df.groupby(x, dropna=True)[y].sum().reset_index().sort_values(y, ascending=False).head(top_n)
    return px.bar(t, x=x, y=y, title=title)


# ---------------------------------------------------------------------------
# Agent 4: Reviewer (rule-based data-quality / caveats)
# ---------------------------------------------------------------------------
def review(df: pd.DataFrame, sector: str) -> List[str]:
    notes = []
    p = profile(df)
    if p["missing_cells"]:
        notes.append(f"{p['missing_cells']} empty cells in the table — averages ignore them.")
    if len(df) < 8:
        notes.append(f"Only {len(df)} records: percentages and correlations are indicative, not statistical.")
    if EVIDENCE_COL in df.columns and df[EVIDENCE_COL].astype(str).str.contains("verify", case=False).any():
        notes.append("Some findings are tagged 'verify' — confirm against official sources before citing.")
    notes.append("Charts summarise the dashboard's curated data; they are not official statistics. "
                 "Verify against WAPDA, IRSA, PMD, NDMA, PBS and primary sources before formal use.")
    return notes


def run_rule_based(df: pd.DataFrame, sector: str, allowed=None, top_n: int = 15) -> dict:
    log = []

    def step(name, fn):
        t0 = time.time()
        res = fn()
        log.append({"agent": name, "seconds": round(time.time() - t0, 3)})
        return res
    prof = step("Profiler", lambda: profile(df))
    insights = step("Analyst", lambda: analyse(df))
    specs = step("Chart Planner", lambda: validate_specs(df, plan_charts(df, allowed, top_n)))
    notes = step("Reviewer", lambda: review(df, sector))
    return {"mode": "rule-based", "profile": prof, "insights": insights, "specs": specs,
            "review": notes, "log": log, "briefing": None}


# ---------------------------------------------------------------------------
# CrewAI crew (optional)
# ---------------------------------------------------------------------------
def crewai_available() -> bool:
    try:
        import crewai  # noqa: F401
        return True
    except Exception:
        return False


def _extract_json(text: str):
    m = re.search(r"\[.*\]", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def _make_tools(df: pd.DataFrame):
    """Tools the agents can call to inspect the sector table."""
    from crewai.tools import tool

    @tool("describe_columns")
    def describe_columns() -> str:
        """List every column of the sector table with its type and one example value."""
        return "\n".join(f"{c} [{df[c].dtype}] e.g. {df[c].dropna().iloc[0] if df[c].notna().any() else ''}"
                         for c in df.columns)

    @tool("top_n_rows")
    def top_n_rows(column: str, n: int = 5) -> str:
        """Return the n rows with the largest value in a numeric column (column name must exist)."""
        if column not in df.columns:
            return f"Unknown column {column}. Columns: {list(df.columns)}"
        return df.sort_values(column, ascending=False).head(int(n)).to_csv(index=False)

    @tool("value_counts")
    def value_counts(column: str) -> str:
        """Return counts of each distinct value of a column."""
        if column not in df.columns:
            return f"Unknown column {column}. Columns: {list(df.columns)}"
        return df[column].astype(str).value_counts().head(25).to_string()

    @tool("correlation")
    def correlation(column_a: str, column_b: str) -> str:
        """Return the Pearson correlation between two numeric columns."""
        try:
            return f"{pd.to_numeric(df[column_a]).corr(pd.to_numeric(df[column_b])):.3f}"
        except Exception as e:  # noqa: BLE001
            return f"Cannot compute: {e}"

    return [describe_columns, top_n_rows, value_counts, correlation]


def run_crewai(df: pd.DataFrame, sector: str, api_key: str, model: str, allowed=None,
               top_n: int = 15, temperature: float = 0.2) -> dict:
    """Run a sequential CrewAI crew on one sector. Raises on setup problems (caller shows the message)."""
    from crewai import Agent, Task, Crew, Process, LLM

    allowed = allowed or CHART_TYPES
    llm = LLM(model=model, api_key=api_key, temperature=temperature)
    tools = []
    try:
        tools = _make_tools(df)
    except Exception:
        tools = []
    ctx = profile_text(df)
    cols = list(df.columns)

    analyst = Agent(
        role="Pakistan Sector Data Analyst",
        goal=f"Extract the 5 most decision-relevant, numerically supported findings about '{sector}'.",
        backstory="A careful analyst of Pakistan's water, terrain, energy, minerals and defence-support data. "
                  "Uses only numbers that appear in the table or that tools return; never invents figures.",
        llm=llm, tools=tools, allow_delegation=False, verbose=False)
    reviewer = Agent(
        role="Domain Risk Reviewer",
        goal="Challenge the analyst: flag weak evidence, small samples, and claims that need verification.",
        backstory="A sceptical reviewer who knows the dataset is a curated educational summary, "
                  "and who marks anything unsupported as 'verify'.",
        llm=llm, tools=tools, allow_delegation=False, verbose=False)
    planner = Agent(
        role="Chart Planner",
        goal=f"Choose up to 6 charts from {allowed} that best show the findings, using ONLY real column names.",
        backstory="A visualisation specialist who answers strictly in JSON.",
        llm=llm, allow_delegation=False, verbose=False)
    writer = Agent(
        role="Briefing Writer",
        goal="Write a short, plain-language briefing (max 180 words) combining analysis and review.",
        backstory="Writes for engineers and officers who want the facts and the caveats.",
        llm=llm, allow_delegation=False, verbose=False)

    t1 = Task(description=f"Sector: {sector}\n\nTable profile:\n{ctx}\n\nUse the tools if you need more detail. "
                          "List 5 findings, each with the numbers behind it.",
              expected_output="Five bullet findings with supporting numbers.", agent=analyst)
    t2 = Task(description="Review the analyst's findings. For each, say OK or 'verify' and why. "
                          "Mention sample-size or data-quality limits.",
              expected_output="A short review with an OK/verify mark per finding.", agent=reviewer, context=[t1])
    t3 = Task(description=("Return ONLY a JSON list (no prose) of chart specs. Each item: "
                           '{"chart": one of ' + json.dumps(allowed) + ', "x": column, "y": column or null, '
                           '"color": column or null, "agg": "sum"|"count"|"cumsum"|"sorted", "title": short title}. '
                           f"Valid columns: {cols}. Use histogram only with a numeric x; scatter needs numeric x and y. "
                           f"Include each requested chart type at most twice. Bars show at most {top_n} items."),
              expected_output="A JSON list of chart specs.", agent=planner, context=[t1])
    t4 = Task(description="Write the briefing: 3 short paragraphs (what the data shows, what to be careful about, "
                          "what to check next).",
              expected_output="A briefing of at most 180 words.", agent=writer, context=[t1, t2])

    crew = Crew(agents=[analyst, reviewer, planner, writer], tasks=[t1, t2, t3, t4],
                process=Process.sequential, verbose=False)
    t0 = time.time()
    crew.kickoff()

    def raw(t):
        o = getattr(t, "output", None)
        return str(getattr(o, "raw", o) or "")

    analysis, review_txt, plan_txt, briefing = raw(t1), raw(t2), raw(t3), raw(t4)
    specs = validate_specs(df, _extract_json(plan_txt) or [])
    fallback = False
    if not specs:
        specs = validate_specs(df, plan_charts(df, allowed, top_n))
        fallback = True
    base = run_rule_based(df, sector, allowed, top_n)
    return {"mode": "crewai", "profile": base["profile"], "insights": base["insights"],
            "specs": specs, "review": base["review"], "briefing": briefing,
            "agent_analysis": analysis, "agent_review": review_txt, "planner_fallback": fallback,
            "log": [{"agent": "Data Analyst", "seconds": None}, {"agent": "Domain Reviewer", "seconds": None},
                    {"agent": "Chart Planner", "seconds": None}, {"agent": "Briefing Writer", "seconds": None}],
            "total_seconds": round(time.time() - t0, 1)}


def to_markdown(sector: str, res: dict) -> str:
    lines = [f"# Agent report — {sector}", f"_Mode: {res['mode']}_", ""]
    if res.get("briefing"):
        lines += ["## Briefing", res["briefing"], ""]
    lines += ["## Findings (computed from the table)"] + [f"- {i}" for i in res["insights"]]
    if res.get("agent_analysis"):
        lines += ["", "## Analyst agent", res["agent_analysis"]]
    if res.get("agent_review"):
        lines += ["", "## Reviewer agent", res["agent_review"]]
    lines += ["", "## Caveats"] + [f"- {n}" for n in res["review"]]
    lines += ["", "## Charts planned"] + [f"- {s['chart']}: {s['title']}" for s in res["specs"]]
    return "\n".join(lines)
