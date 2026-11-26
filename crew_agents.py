"""
crew_agents.py
Sector "agents" for every sector of the dashboard, with results shown as
bar graphs, pie charts, scatter plots, line charts and histograms.

Two layers
----------
1. Built-in agents (always available, no API key, no internet):
     DataProfilerAgent  -> profiles the sector table
     ChartPlannerAgent  -> decides which of the 5 chart types fit the data
     InsightAgent       -> writes plain-language findings from the numbers
     ChartAgent         -> draws the charts (Plotly)
2. Optional CrewAI crew (needs `pip install crewai`, a model name and an API key):
     a 3-agent crew (Sector Data Analyst -> Chart Strategist -> Briefing Writer)
     that turns the same profile into an LLM-written brief. Charts are always
     drawn locally from the data, never invented by the LLM.

All figures come from the curated tables already inside this project; the agents
add no new facts. Text-only sectors (Army, Solar, Mining, Dry Fruit) are charted
from evidence tags, finding lengths and the first figure quoted in each finding.
"""
from __future__ import annotations

import re
import os

import pandas as pd
import streamlit as st
import plotly.express as px

import data_loader as d
import army_role
import energy_minerals as em

CHART_KINDS = ["Bar graph", "Pie chart", "Scatter plot", "Line chart", "Histogram"]


# ---------------------------------------------------------------------------
# Sector tables (built from the project's own data)
# ---------------------------------------------------------------------------
def _num(series):
    return pd.to_numeric(series, errors="coerce")


def _provinces():
    rows = []
    for n, v in d.PROVINCES.items():
        rows.append({"Province": n, "area_km2": v.get("area_km2"),
                     "Rivers": len(v.get("major_rivers", [])),
                     "Dams & barrages": len(v.get("major_dams_barrages", [])),
                     "Mountain ranges": len(v.get("mountain_ranges", [])),
                     "Lakes": len(v.get("key_lakes", []))})
    return pd.DataFrame(rows)


def _rivers():
    rows = []
    for n, v in d.RIVERS.items():
        rows.append({"River": n, "length_km": v.get("length_km"),
                     "Provinces crossed": len(v.get("provinces", []) or []),
                     "Dams & barrages": len(v.get("dams_barrages", []) or [])})
    return pd.DataFrame(rows)


def _dams():
    rows = []
    for n, v in d.DAMS_BARRAGES.items():
        rows.append({"Dam / barrage": n, "type": v.get("type"), "river": v.get("river"),
                     "province": v.get("province"), "year_completed": v.get("year_completed"),
                     "capacity_MW": v.get("capacity_MW")})
    df = pd.DataFrame(rows)
    for c in ("year_completed", "capacity_MW"):
        df[c] = _num(df[c])
    return df


def _links():
    return pd.DataFrame([{"Canal": n, "province": v.get("province"), "connects": v.get("connects")}
                         for n, v in d.LINK_CANALS.items()])


def _lakes():
    return pd.DataFrame([{"Lake": n, "province": v.get("province"), "type": v.get("type")}
                         for n, v in d.LAKES.items()])


def _deserts():
    df = pd.DataFrame([{"Desert": n, "province": v.get("province"), "area_km2": v.get("area_km2"),
                        "type": v.get("type")} for n, v in d.DESERTS.items()])
    df["area_km2"] = _num(df["area_km2"])
    return df


def _parks():
    rows = []
    for n, v in d.NATIONAL_PARKS.items():
        m = re.search(r"\b(1[89]\d\d|20\d\d)\b", str(v.get("established", "")))
        rows.append({"Park": n, "province": v.get("province"), "type": v.get("type"),
                     "established": int(m.group(1)) if m else None})
    df = pd.DataFrame(rows)
    df["established"] = _num(df["established"])
    return df


def _disasters():
    rows = [{"Event": e["name"], "year": e["year"], "hazard_type": e["hazard_type"],
             "Provinces affected": len(e.get("provinces", []))} for e in d.DISASTER_HISTORICAL_EVENTS]
    return pd.DataFrame(rows)


def _hazards():
    return pd.DataFrame([{"Province": p, "Hazards listed": len(h)} for p, h in d.DISASTER_HAZARD_BY_PROVINCE.items()])


def _agro():
    df = pd.DataFrame(d.REGIONAL_AGRO_SOCIO_DATA)
    for c in df.columns[1:]:
        df[c] = _num(df[c])
    return df


def _delta():
    df = pd.DataFrame(d.INDUS_DELTA_SAMPLE_SITES)
    for c in ("EC_dS_per_m", "pH", "ESP_pct"):
        if c in df:
            df[c] = _num(df[c])
    return df


_FIG = re.compile(r"(\d[\d,]*\.?\d*)\s*(GW|MW|MWp|km2|km|%|million tonnes|million|billion|tonnes|ha|acres|MT)?", re.I)


def _first_figure(text):
    for m in _FIG.finditer(text):
        raw = m.group(1).replace(",", "")
        try:
            v = float(raw)
        except ValueError:
            continue
        if 1900 <= v <= 2100 and not m.group(2):
            continue  # looks like a year
        return v, (m.group(2) or "")
    return None, ""


def _text_rows(items, sector, tab=None, tag_default="Source-backed"):
    rows = []
    for pt in items:
        text, tag = (pt if isinstance(pt, (tuple, list)) and len(pt) >= 2 else (str(pt), tag_default))
        fig, unit = _first_figure(str(text))
        rows.append({"Sector": sector, "Tab": tab or sector, "Evidence": tag,
                     "Finding": str(text), "Length (chars)": len(str(text)), "First figure": fig, "Unit": unit})
    return rows


def _energy(source, label):
    rows = []
    for tab, v in source.items():
        rows += _text_rows(v.get("points", []), label, tab)
    return pd.DataFrame(rows)


def _army():
    rows = []
    for name, v in army_role.SECTORS.items():
        rows += _text_rows(v.get("points", []), "Army role", name)
    return pd.DataFrame(rows)


SECTOR_BUILDERS = {
    "Provinces": _provinces,
    "Rivers": _rivers,
    "Dams & Barrages": _dams,
    "Link Canals": _links,
    "Lakes": _lakes,
    "Deserts": _deserts,
    "National Parks": _parks,
    "Disaster Events": _disasters,
    "Disaster Hazards by Province": _hazards,
    "Agro-Socio-Economic": _agro,
    "Indus Delta Soil": _delta,
    "Army Role": _army,
    "Solar Energy": lambda: _energy(em.SOLAR, "Solar"),
    "Mining": lambda: _energy(em.MINING, "Mining"),
    "Dry Fruit": lambda: _energy(em.DRYFRUIT, "Dry Fruit"),
}

PAGE_TO_SECTOR = {
    "🗺️ Provinces": "Provinces",
    "🌊 Rivers": "Rivers",
    "🚧 Dams & Barrages": "Dams & Barrages",
    "🔀 Link Canals": "Link Canals",
    "🏞️ Lakes": "Lakes",
    "🏜️ Deserts": "Deserts",
    "🌳 National Parks": "National Parks",
    "⚠️ Disaster Risk Context": "Disaster Events",
    "📈 Socio-Economic & Agro-Economic": "Agro-Socio-Economic",
    "🧂 Indus Delta Soil Salinity (EMI Survey)": "Indus Delta Soil",
    "🪖 Pakistan Army's Role Across Sectors": "Army Role",
    "☀️ Solar Energy Sectors": "Solar Energy",
    "⛏️ Mining Sectors": "Mining",
    "🥜 Dry Fruit Sector": "Dry Fruit",
}


def sector_table(name: str) -> pd.DataFrame:
    try:
        df = SECTOR_BUILDERS[name]()
    except Exception:  # a missing field must never break a page
        df = pd.DataFrame()
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Built-in agents
# ---------------------------------------------------------------------------
class DataProfilerAgent:
    """Finds the label column, numeric columns and low-cardinality categories."""
    role = "Data Profiler"

    @staticmethod
    def profile(df: pd.DataFrame) -> dict:
        text = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c]) and c != "Finding"]
        label = next((c for c in text if df[c].nunique() == len(df)), None)
        nums = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 1]
        cats = [c for c in text if c != label and 2 <= df[c].astype(str).nunique() <= 15]
        years = [c for c in nums if "year" in c.lower() or "establish" in c.lower()]
        return {"rows": len(df), "label": label, "numeric": nums, "categorical": cats, "year": years[0] if years else None,
                "missing": int(df.isna().sum().sum())}


class ChartPlannerAgent:
    """Decides which chart kinds can be drawn from this table, and with which columns."""
    role = "Chart Planner"

    @staticmethod
    def plan(df: pd.DataFrame, prof: dict) -> dict:
        nums, cats, label = prof["numeric"], prof["categorical"], prof["label"]
        plan = {}
        if cats or (label and nums):
            bar_num = next((n for n in nums if n != prof["year"]), None)
            plan["Bar graph"] = {"cat": cats[0] if cats else None, "label": label, "num": bar_num}
        if cats:
            plan["Pie chart"] = {"cat": cats[0]}
        if len(nums) >= 2:
            plan["Scatter plot"] = {"x": nums[0], "y": nums[1], "color": cats[0] if cats else None, "hover": label}
        if nums:
            plan["Line chart"] = {"x": prof["year"], "y": next((n for n in nums if n != prof["year"]), nums[0]), "label": label}
            plan["Histogram"] = {"x": nums[0]}
        return plan


class InsightAgent:
    """Rule-based findings (no LLM): extremes, averages, shares, strongest correlation."""
    role = "Insight Analyst"

    @staticmethod
    def insights(df: pd.DataFrame, prof: dict) -> list:
        out = [f"{prof['rows']} records; {len(prof['numeric'])} numeric and {len(prof['categorical'])} category columns; "
               f"{prof['missing']} blank cells."]
        label = prof["label"]
        for c in prof["numeric"][:3]:
            s = df[c].dropna()
            if s.empty:
                continue
            top = df.loc[s.idxmax()]
            who = f" ({top[label]})" if label else ""
            out.append(f"{c}: max {s.max():,.4g}{who}, median {s.median():,.4g}, mean {s.mean():,.4g}.")
        for c in prof["categorical"][:2]:
            vc = df[c].astype(str).value_counts(normalize=True)
            out.append(f"{c}: most common is “{vc.index[0]}” ({vc.iloc[0]:.0%} of records).")
        if len(prof["numeric"]) >= 2:
            cm = df[prof["numeric"]].corr().abs()
            best, pair = 0, None
            cols = list(cm.columns)
            for i, a in enumerate(cols):
                for b in cols[i + 1:]:
                    v = cm.loc[a, b]
                    if pd.notna(v) and v > best:
                        best, pair = v, (a, b)
            if pair:
                out.append(f"Strongest numeric relationship: {pair[0]} vs {pair[1]} (|r| = {best:.2f}; association only).")
        return out


class ChartAgent:
    """Draws the five chart types with Plotly."""
    role = "Chart Builder"

    @staticmethod
    def bar(df, spec):
        if spec.get("label") and spec.get("num"):
            t = df.dropna(subset=[spec["num"]]).nlargest(15, spec["num"])
            return px.bar(t, x=spec["label"], y=spec["num"], title=f"Top {len(t)} by {spec['num']}")
        vc = df[spec["cat"]].astype(str).value_counts().reset_index()
        vc.columns = [spec["cat"], "count"]
        return px.bar(vc, x=spec["cat"], y="count", title=f"Records by {spec['cat']}")

    @staticmethod
    def pie(df, spec):
        vc = df[spec["cat"]].astype(str).value_counts().reset_index()
        vc.columns = [spec["cat"], "count"]
        return px.pie(vc, names=spec["cat"], values="count", title=f"Share of records by {spec['cat']}")

    @staticmethod
    def scatter(df, spec):
        t = df.dropna(subset=[spec["x"], spec["y"]])
        kw = {"x": spec["x"], "y": spec["y"], "title": f"{spec['y']} vs {spec['x']}"}
        if spec.get("color"):
            kw["color"] = spec["color"]
        if spec.get("hover"):
            kw["hover_name"] = spec["hover"]
        return px.scatter(t, **kw)

    @staticmethod
    def line(df, spec):
        t = df.dropna(subset=[spec["y"]])
        if spec.get("x"):
            t = t.dropna(subset=[spec["x"]]).sort_values(spec["x"])
            return px.line(t, x=spec["x"], y=spec["y"], markers=True, title=f"{spec['y']} over {spec['x']}")
        t = t.sort_values(spec["y"], ascending=False).reset_index(drop=True)
        t["rank"] = t.index + 1
        kw = {"x": "rank", "y": spec["y"], "markers": True, "title": f"{spec['y']} ranked high → low"}
        if spec.get("label"):
            kw["hover_name"] = spec["label"]
        return px.line(t, **kw)

    @staticmethod
    def histogram(df, spec):
        t = df.dropna(subset=[spec["x"]])
        return px.histogram(t, x=spec["x"], nbins=min(12, max(4, len(t) // 2)), title=f"Distribution of {spec['x']}")

    @classmethod
    def draw(cls, kind, df, spec):
        fn = {"Bar graph": cls.bar, "Pie chart": cls.pie, "Scatter plot": cls.scatter,
              "Line chart": cls.line, "Histogram": cls.histogram}[kind]
        return fn(df, spec)


# ---------------------------------------------------------------------------
# Optional CrewAI crew
# ---------------------------------------------------------------------------
def crewai_available() -> bool:
    try:
        import crewai  # noqa: F401
        return True
    except Exception:
        return False


def run_crew(sector: str, df: pd.DataFrame, insights: list, model: str, api_key: str) -> str:
    """3-agent sequential CrewAI crew. Returns the final brief as text (raises on failure)."""
    from crewai import Agent, Task, Crew, Process
    try:
        from crewai import LLM
        llm = LLM(model=model, api_key=api_key)
    except Exception:
        os.environ.setdefault("OPENAI_API_KEY", api_key)
        llm = model  # older crewai versions accept a model-name string
    sample = df.head(40).to_csv(index=False)
    context = ("Sector: %s\nBuilt-in findings:\n- %s\n\nData sample (CSV):\n%s" % (sector, "\n- ".join(insights), sample))

    analyst = Agent(role="Sector Data Analyst",
                    goal=f"Describe what the {sector} data of Pakistan shows, using only the supplied table.",
                    backstory="Engineer-analyst who never invents numbers and flags weak or missing data.",
                    llm=llm, allow_delegation=False, verbose=False)
    strategist = Agent(role="Chart Strategist",
                       goal="Say which of bar graph, pie chart, scatter plot, line chart and histogram best show this data and why.",
                       backstory="Data-visualisation specialist who matches chart type to data type.",
                       llm=llm, allow_delegation=False, verbose=False)
    writer = Agent(role="Briefing Writer",
                   goal="Write a short, plain-English briefing a project engineer can read in one minute.",
                   backstory="Technical writer who keeps claims tied to the data and states limits clearly.",
                   llm=llm, allow_delegation=False, verbose=False)

    t1 = Task(description=f"{context}\n\nList the 4-6 most important observations. Use only numbers present above.",
              expected_output="Bullet list of observations with the supporting values.", agent=analyst)
    t2 = Task(description="Given the observations, recommend the best chart type(s) from: bar graph, pie chart, scatter plot, "
                          "line chart, histogram. One line of reasoning each.",
              expected_output="Chart recommendations with one-line reasons.", agent=strategist)
    t3 = Task(description="Combine the observations and chart advice into a briefing of at most 8 bullets, ending with one "
                          "caution about data quality or verification.",
              expected_output="Final briefing, at most 8 bullets.", agent=writer)
    crew = Crew(agents=[analyst, strategist, writer], tasks=[t1, t2, t3], process=Process.sequential, verbose=False)
    result = crew.kickoff()
    return getattr(result, "raw", None) or str(result)


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
def render(default_sector: str = "Dams & Barrages", key: str = "ca", expanded: bool = True, title: str = None):
    """Draws the whole agent panel. `key` must be unique per placement on a page."""
    names = list(SECTOR_BUILDERS)
    idx = names.index(default_sector) if default_sector in names else 0
    with st.expander(title or "🤖 Sector agents — charts & insights", expanded=expanded):
        sector = st.selectbox("Sector", names, index=idx, key=f"{key}_sector")
        df = sector_table(sector)
        if df.empty:
            st.info("No data available for this sector.")
            return
        prof = DataProfilerAgent.profile(df)
        plan = ChartPlannerAgent.plan(df, prof)
        ins = InsightAgent.insights(df, prof)

        st.markdown("**Agent team (built-in):** Data Profiler → Chart Planner → Insight Analyst → Chart Builder")
        for line in ins:
            st.markdown(f"- {line}")

        kinds = st.multiselect("Charts to draw", CHART_KINDS, default=[k for k in CHART_KINDS if k in plan], key=f"{key}_kinds")
        for k in kinds:
            if k not in plan:
                st.caption(f"{k}: this table doesn't have the columns it needs.")
                continue
            try:
                st.plotly_chart(ChartAgent.draw(k, df, plan[k]), use_container_width=True, key=f"{key}_fig_{k}")
            except Exception as e:  # keep the page alive
                st.caption(f"{k}: could not be drawn ({type(e).__name__}).")

        with st.expander("🧩 Build your own chart", expanded=False):
            cols = list(df.columns)
            kind = st.selectbox("Chart type", CHART_KINDS, key=f"{key}_ck")
            x = st.selectbox("X / category column", cols, key=f"{key}_cx")
            y = st.selectbox("Y / value column (not used by pie & histogram)", ["(none)"] + cols, key=f"{key}_cy")
            color = st.selectbox("Colour by", ["(none)"] + cols, key=f"{key}_cc")
            try:
                if kind == "Histogram":
                    fig = px.histogram(df, x=x, color=None if color == "(none)" else color)
                elif kind == "Pie chart":
                    vc = df[x].astype(str).value_counts().reset_index()
                    vc.columns = [x, "count"]
                    fig = px.pie(vc, names=x, values="count")
                elif y == "(none)":
                    st.info("Pick a Y column for this chart type.")
                    fig = None
                else:
                    kw = {"x": x, "y": y}
                    if color != "(none)":
                        kw["color"] = color
                    fig = {"Bar graph": px.bar, "Scatter plot": px.scatter, "Line chart": px.line}[kind](df, **kw)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True, key=f"{key}_custom")
            except Exception as e:
                st.caption(f"Could not draw that combination ({type(e).__name__}). Try numeric columns for Y.")

        with st.expander("📄 Data behind the charts", expanded=False):
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"),
                               file_name=f"{sector.lower().replace(' ', '_')}.csv", mime="text/csv", key=f"{key}_dl")

        with st.expander("🧠 CrewAI crew (LLM-written brief — optional)", expanded=False):
            st.caption("Needs `pip install crewai`, a model name and your own API key. The key is used for this run only "
                       "and is not stored. Charts above never depend on this.")
            if not crewai_available():
                st.info("CrewAI is not installed in this environment, so only the built-in agents are available. "
                        "Install with `pip install -r requirements-crewai.txt`.")
            else:
                model = st.text_input("Model (provider/name or name)", value="gpt-4o-mini", key=f"{key}_model")
                api_key = st.text_input("API key", value="", type="password", key=f"{key}_apikey")
                if st.button("Run the crew", key=f"{key}_run"):
                    if not api_key.strip():
                        st.warning("Enter an API key first.")
                    else:
                        with st.spinner("The crew is working…"):
                            try:
                                st.markdown(run_crew(sector, df, ins, model.strip(), api_key.strip()))
                            except Exception as e:
                                st.error(f"Crew run failed: {type(e).__name__}: {e}")
