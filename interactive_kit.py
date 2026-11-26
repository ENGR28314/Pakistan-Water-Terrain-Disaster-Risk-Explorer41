"""
interactive_kit.py
Reusable interactivity for every data table in the dashboard:
  explore(df, key)  ->  search box, column filters, numeric range filters, sort,
                        filtered table, CSV download and a one-click chart builder.
Uses only widgets available in older Streamlit releases (no `key=` on
st.*_chart; keys are passed only to widgets and st.plotly_chart).
"""
from __future__ import annotations

import re

import pandas as pd
import streamlit as st
import plotly.express as px

_NUM_RE = re.compile(r"\d[\d,]*\.?\d*|\.\d+")
_LEAD_RE = re.compile(r"^[\s~\u2248<>+\u2264\u2265]*(?:Rs\.?|PKR|USD|US\$|\$|\u20b9)?\s*[\d.]", re.I)
_LATLON = {"latitude": "lat", "lat": "lat", "longitude": "lon", "lon": "lon", "lng": "lon", "long": "lon"}


def _first_number(cell):
    """Number at the start of a text cell: '18,629 acres' -> 18629, '~3,500-4,000' -> 3750 (range
    midpoint), '45%' -> 45. None when the cell does not start with a number."""
    s = str(cell).strip()
    if not _LEAD_RE.match(s):
        return None
    nums = []
    for m in _NUM_RE.finditer(s[:40]):
        try:
            nums.append(float(m.group(0).replace(",", "")))
        except ValueError:
            continue
        if len(nums) == 2:
            break
    if not nums:
        return None
    if len(nums) == 2 and re.match(r"^[^\d]*[\d,.]+\s*[-\u2013\u2014]\s*[\d.,]+", s):
        return (nums[0] + nums[1]) / 2.0
    return nums[0]


def _text_to_numeric(series: pd.Series):
    """Numeric version of a text column when most of its cells start with a number, else None."""
    vals = series.dropna()
    vals = vals[vals.astype(str).str.strip() != ""]
    if len(vals) < 2:
        return None
    parsed = series.map(lambda v: _first_number(v) if pd.notna(v) else None)
    ok = parsed.notna().sum()
    if ok < 2 or ok < 0.6 * len(vals):
        return None
    out = pd.to_numeric(parsed, errors="coerce")
    return out if out.nunique() > 1 else None


def _by_cardinality(work: pd.DataFrame, cols):
    """Category-like columns (2-30 distinct values) first, most useful for 'count by' charts."""
    def rank(c):
        n = work[c].astype(str).nunique()
        return (0 if 2 <= n <= 30 else 1, n if 2 <= n <= 30 else -n)
    return sorted(cols, key=rank)


def _chart_frame(out: pd.DataFrame):
    """(frame with derived numeric columns, numeric columns, label columns, lat col, lon col)."""
    work = out.copy()
    derived = []
    for c in list(work.columns):
        if not pd.api.types.is_numeric_dtype(work[c]) and not pd.api.types.is_bool_dtype(work[c]):
            num = _text_to_numeric(work[c])
            if num is not None:
                name = f"{c} (numeric)"
                work[name] = num
                derived.append(name)
    lat = next((c for c in work.columns if str(c).lower() in _LATLON and _LATLON[str(c).lower()] == "lat"
                and pd.api.types.is_numeric_dtype(work[c])), None)
    lon = next((c for c in work.columns if str(c).lower() in _LATLON and _LATLON[str(c).lower()] == "lon"
                and pd.api.types.is_numeric_dtype(work[c])), None)
    coord = {c for c in (lat, lon) if c}
    num_cols = [c for c in work.columns if pd.api.types.is_numeric_dtype(work[c])
                and not pd.api.types.is_bool_dtype(work[c]) and c not in coord and work[c].notna().any()]
    if not num_cols and coord:
        num_cols = [c for c in work.columns if c in coord]
    label_cols = [c for c in out.columns if not pd.api.types.is_numeric_dtype(out[c])]
    return work, num_cols, label_cols, lat, lon



def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    return df.reset_index(drop=True)


def explore(df: pd.DataFrame, key: str, title: str = "🔍 Search, filter, sort & chart this table",
            chart: bool = True, expanded: bool = False):
    """Render df with interactive controls. Returns the filtered DataFrame."""
    if df is None or len(df) == 0:
        st.dataframe(df, use_container_width=True, hide_index=True)
        return df
    df = _clean(df)
    out = df

    with st.expander(title, expanded=expanded):
        q = st.text_input("Search (matches any column)", value="", key=f"{key}_q")
        if q.strip():
            needle = q.strip().lower()
            mask = out.astype(str).apply(lambda col: col.str.lower().str.contains(needle, regex=False)).any(axis=1)
            out = out[mask]

        cat_cols = [c for c in df.columns
                    if not pd.api.types.is_numeric_dtype(df[c]) and 2 <= df[c].astype(str).nunique() <= 15]
        if cat_cols:
            pick = st.multiselect("Filter by column", cat_cols, default=[], key=f"{key}_fc")
            for c in pick:
                opts = sorted(df[c].astype(str).unique())
                sel = st.multiselect(f"{c} is…", opts, default=opts, key=f"{key}_f_{c}")
                out = out[out[c].astype(str).isin(sel)]

        num_cols = [c for c in df.columns
                    if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 1
                    and c.lower() not in ("latitude", "longitude")]
        if num_cols:
            npick = st.multiselect("Numeric range filter", num_cols, default=[], key=f"{key}_nc")
            for c in npick:
                lo, hi = float(df[c].min()), float(df[c].max())
                r = st.slider(f"{c} range", lo, hi, (lo, hi), key=f"{key}_r_{c}")
                out = out[(out[c] >= r[0]) & (out[c] <= r[1])]

        c1, c2 = st.columns(2)
        with c1:
            sort_col = st.selectbox("Sort by", ["(original order)"] + list(df.columns), key=f"{key}_s")
        with c2:
            desc = st.checkbox("Descending", value=False, key=f"{key}_d")
        if sort_col != "(original order)":
            out = out.sort_values(sort_col, ascending=not desc, kind="stable")

        st.caption(f"Showing {len(out)} of {len(df)} rows.")

    st.dataframe(out, use_container_width=True, hide_index=True)

    if len(out):
        st.download_button("⬇️ Download these rows (CSV)", out.to_csv(index=False).encode("utf-8"),
                           file_name=f"{key}.csv", mime="text/csv", key=f"{key}_dl")

    if chart and len(out) >= 2:
        with st.expander("📊 Chart this table"):
            work, num_cols_o, label_cols, lat_c, lon_c = _chart_frame(out)
            COUNT = "Number of rows (count)"
            kinds = ["Bar", "Line", "Scatter", "Pie", "Histogram"] + (["Map"] if lat_c and lon_c else [])
            kind = st.selectbox("Chart type", kinds, key=f"{key}_ct")
            if len(num_cols_o) != len([c for c in out.columns if pd.api.types.is_numeric_dtype(out[c])]):
                st.caption("Columns whose cells start with a number (e.g. '18,629 acres', '~3,500-4,000', "
                           "'45%') are also offered as '<column> (numeric)'.")
            try:
                fig = None
                label_default = label_cols or list(work.columns)
                if kind == "Map":
                    hover = label_cols[0] if label_cols else None
                    color_opts = ["(none)"] + [c for c in label_cols if 2 <= work[c].astype(str).nunique() <= 20]
                    size_opts = ["(none)"] + [c for c in num_cols_o if c not in (lat_c, lon_c)]
                    cm1, cm2 = st.columns(2)
                    color_by = cm1.selectbox("Colour by", color_opts, key=f"{key}_mc")
                    size_by = cm2.selectbox("Size by", size_opts, key=f"{key}_ms")
                    mp = work.dropna(subset=[lat_c, lon_c]).copy()
                    if size_by != "(none)":
                        mp["_size"] = pd.to_numeric(mp[size_by], errors="coerce").fillna(0).clip(lower=0) + 1e-6
                    fig = px.scatter_map(
                        mp, lat=lat_c, lon=lon_c, hover_name=hover,
                        color=None if color_by == "(none)" else color_by,
                        size="_size" if size_by != "(none)" else None, size_max=28,
                        zoom=4, height=520, map_style="open-street-map")
                elif kind == "Histogram":
                    if num_cols_o:
                        y = st.selectbox("Column", num_cols_o, key=f"{key}_hy")
                        fig = px.histogram(work, x=y)
                    else:
                        st.info("No numeric column to bin - showing how many rows fall in each category.")
                        x = st.selectbox("Category", _by_cardinality(work, label_default), key=f"{key}_hx")
                        cnt = work.groupby(x).size().reset_index(name=COUNT).sort_values(COUNT, ascending=False)
                        fig = px.bar(cnt.head(40), x=x, y=COUNT)
                elif kind == "Scatter":
                    if len(num_cols_o) >= 2:
                        x = st.selectbox("X (numeric)", num_cols_o, key=f"{key}_sx")
                        y = st.selectbox("Y (numeric)", num_cols_o, index=1, key=f"{key}_sy")
                        fig = px.scatter(work, x=x, y=y, hover_name=label_cols[0] if label_cols else None)
                    else:
                        st.info("Scatter needs two numeric columns - this table has "
                                f"{len(num_cols_o)}. Use Bar / Pie (counts) instead.")
                else:  # Bar / Line / Pie
                    coord_only = bool(num_cols_o) and all(c in (lat_c, lon_c) for c in num_cols_o)
                    measures = ([COUNT] + num_cols_o) if (coord_only or not num_cols_o) else (num_cols_o + [COUNT])
                    y = st.selectbox("Value (Y)", measures, key=f"{key}_y")
                    if y == COUNT:
                        x_opts = _by_cardinality(work, label_default)
                    else:
                        x_opts = label_default
                    x = st.selectbox("Label (X)", x_opts, key=f"{key}_x")
                    if y == COUNT:
                        data = work.groupby(x).size().reset_index(name=COUNT).sort_values(COUNT, ascending=False)
                        data = data.head(40)
                        yv = COUNT
                    else:
                        data = work.dropna(subset=[y])
                        yv = y
                    if kind == "Pie":
                        fig = px.pie(data, names=x, values=yv)
                    elif kind == "Line":
                        fig = px.line(data, x=x, y=yv, markers=True)
                    else:
                        fig = px.bar(data, x=x, y=yv)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True, key=f"{key}_fig")
            except Exception as e:  # never break the page over an optional chart
                st.info(f"Could not draw that chart for this selection ({type(e).__name__}: {e}).")
    return out
