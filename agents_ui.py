"""
agents_ui.py - Streamlit front-end for the sector agents (see agents_crew.py).

  render_page()            full page "AI Agents (CrewAI)": any sector, rule-based or CrewAI, all-sector run,
                           your own CSV.
  render_panel(section)    compact panel shown at the bottom of every dashboard section.
"""
from __future__ import annotations

import os
import zlib

import pandas as pd
import streamlit as st

import agents_crew as ac

PROVIDERS = {
    "OpenAI": ("openai/gpt-4o-mini", "OPENAI_API_KEY"),
    "Anthropic": ("anthropic/claude-sonnet-4-5", "ANTHROPIC_API_KEY"),
    "Google Gemini": ("gemini/gemini-2.0-flash", "GEMINI_API_KEY"),
    "Other (LiteLLM model string)": ("", ""),
}


def _secret(name: str) -> str:
    try:
        return str(st.secrets.get(name, "")) or os.environ.get(name, "")
    except Exception:
        return os.environ.get(name, "")


def _show_result(df: pd.DataFrame, sector: str, res: dict, key: str) -> None:
    st.caption(f"Mode: **{res['mode']}** · agents run: " + " → ".join(s["agent"] for s in res["log"])
               + (f" · {res['total_seconds']} s" if res.get("total_seconds") else ""))
    if res.get("briefing"):
        st.subheader("Briefing (CrewAI)")
        st.write(res["briefing"])
    st.subheader("Findings computed from the data")
    for line in res["insights"]:
        st.markdown(f"- {line}")
    if res.get("agent_analysis"):
        with st.expander("Analyst agent (LLM) — raw output"):
            st.write(res["agent_analysis"])
    if res.get("agent_review"):
        with st.expander("Reviewer agent (LLM) — raw output"):
            st.write(res["agent_review"])
    if res.get("planner_fallback"):
        st.info("The LLM's chart plan was not usable, so the rule-based Chart Planner chose the charts.")

    specs = res["specs"]
    if not specs:
        st.info("This table has no numeric or repeated-category columns to chart.")
    else:
        kinds = [k for k in ac.CHART_TYPES if any(s["chart"] == k for s in specs)]
        absent = [k for k in ac.CHART_TYPES if k not in kinds]
        tabs = st.tabs([k.title() for k in kinds] + ["Data"])
        for tab, kind in zip(tabs, kinds):
            with tab:
                for i, spec in enumerate([s for s in specs if s["chart"] == kind]):
                    try:
                        fig = ac.build_figure(df, spec)
                        st.plotly_chart(fig, use_container_width=True, key=f"{key}_{kind}_{i}")
                    except Exception as e:  # noqa: BLE001
                        st.warning(f"Could not draw '{spec.get('title', kind)}': {e}")
        with tabs[-1]:
            st.dataframe(df, use_container_width=True, hide_index=True)
        if absent:
            st.caption("Not drawn for this table (data does not support it): " + ", ".join(absent)
                       + ". Scatter needs two numeric columns; histogram needs a numeric (or repeated-category) column.")
    st.subheader("Reviewer caveats")
    for n in res["review"]:
        st.markdown(f"- {n}")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("⬇️ Report (Markdown)", ac.to_markdown(sector, res).encode("utf-8"),
                           file_name="agent_report.md", mime="text/markdown", key=f"{key}_dlmd")
    with c2:
        st.download_button("⬇️ Table (CSV)", df.to_csv(index=False).encode("utf-8"),
                           file_name="sector_table.csv", mime="text/csv", key=f"{key}_dlcsv")


def _controls(key: str, allow_crew: bool):
    mode = "Rule-based agents (no API key)"
    creds = {}
    if allow_crew:
        mode = st.radio("Agent mode", ["Rule-based agents (no API key)", "CrewAI crew + LLM (your API key)"],
                        key=f"{key}_mode", horizontal=True)
        if mode.startswith("CrewAI"):
            if not ac.crewai_available():
                st.warning("CrewAI is not installed here. Add `crewai` to requirements "
                           "(see requirements-agents.txt) and redeploy, or use the rule-based agents.")
            prov = st.selectbox("LLM provider", list(PROVIDERS), key=f"{key}_prov")
            default_model, env_name = PROVIDERS[prov]
            creds["model"] = st.text_input("Model (LiteLLM name — edit if yours differs)", value=default_model,
                                           key=f"{key}_model")
            stored = _secret(env_name) if env_name else ""
            creds["key"] = st.text_input("API key (kept only in this session; or set it in Streamlit secrets)",
                                         value="", type="password", key=f"{key}_apikey") or stored
            creds["temp"] = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05, key=f"{key}_temp")
    kinds = st.multiselect("Chart types", ac.CHART_TYPES, default=ac.CHART_TYPES, key=f"{key}_kinds")
    top_n = st.slider("Bars / pie slices to show", 5, 30, 15, key=f"{key}_topn")
    return mode, creds, kinds or ac.CHART_TYPES, top_n


def _run(df, sector, mode, creds, kinds, top_n):
    if mode.startswith("CrewAI"):
        if not ac.crewai_available():
            st.error("CrewAI is not installed — running the rule-based agents instead.")
        elif not creds.get("key") or not creds.get("model"):
            st.error("Enter a model name and an API key for CrewAI mode (or switch to rule-based agents).")
            return None
        else:
            with st.spinner("CrewAI agents are working (this can take a minute)…"):
                try:
                    return ac.run_crewai(df, sector, creds["key"], creds["model"], kinds, top_n, creds["temp"])
                except Exception as e:  # noqa: BLE001
                    st.error(f"CrewAI run failed: {type(e).__name__}: {str(e)[:300]}. Showing rule-based results.")
    return ac.run_rule_based(df, sector, kinds, top_n)


def render_panel(section: str) -> None:
    """Compact panel for one dashboard section (rule-based + optional CrewAI)."""
    sectors = ac.SECTION_TO_SECTORS.get(section)
    if not sectors:
        return
    with st.expander("🤖 AI agents for this section — charts & findings"):
        key = "ap_" + str(zlib.crc32(section.encode("utf-8")))
        sector = st.selectbox("Data table", sectors, key=f"{key}_sec") if len(sectors) > 1 else sectors[0]
        st.caption("Agents analyse this section's data table and draw bar, pie, scatter, line and histogram charts. "
                   "For the CrewAI + LLM mode use the **🤖 AI Agents (CrewAI)** page.")
        mode, creds, kinds, top_n = _controls(key, allow_crew=False)
        df = ac.load_sector(sector)
        if st.button("▶ Run agents", key=f"{key}_run"):
            st.session_state[f"{key}_res"] = (sector, _run(df, sector, mode, creds, kinds, top_n))
        saved = st.session_state.get(f"{key}_res")
        if saved and saved[0] == sector and saved[1]:
            _show_result(df, sector, saved[1], key)


def _all_sectors_summary(kinds, top_n):
    rows, finds = [], []
    for name in ac.SECTOR_BUILDERS:
        df = ac.load_sector(name)
        res = ac.run_rule_based(df, name, kinds, top_n)
        rows.append({"Sector": name, "Records": len(df), "Columns": len(df.columns),
                     "Numeric columns": len(res["profile"]["roles"]["nums"]),
                     "Charts planned": len(res["specs"]), "Missing cells": res["profile"]["missing_cells"]})
        for line in res["insights"][1:3]:
            finds.append({"Sector": name, "Finding": line})
    return pd.DataFrame(rows), pd.DataFrame(finds)


def render_page() -> None:
    st.title("🤖 AI Agents (CrewAI) — all sectors")
    st.markdown(
        "Pick any sector of this project (or upload your own CSV). A team of agents — **Profiler → Analyst → "
        "Chart Planner → Reviewer** — reads the data table, writes findings and draws **bar, pie, scatter, line "
        "and histogram** charts.\n\n"
        "* **Rule-based agents** run instantly, offline, with no key. Every number is computed from the table.\n"
        "* **CrewAI crew + LLM** adds a Data Analyst, Domain Reviewer, Chart Planner and Briefing Writer powered "
        "by your own LLM key. The LLM's chart plan is checked against the real columns before anything is drawn."
    )
    tab_one, tab_all, tab_csv = st.tabs(["🎯 One sector", "🌐 All sectors", "📤 My CSV"])

    with tab_one:
        sector = st.selectbox("Sector", list(ac.SECTOR_BUILDERS), key="aa_sector")
        mode, creds, kinds, top_n = _controls("aa1", allow_crew=True)
        df = ac.load_sector(sector)
        if st.button("▶ Run agents", key="aa1_run"):
            st.session_state["aa1_res"] = (sector, _run(df, sector, mode, creds, kinds, top_n))
        saved = st.session_state.get("aa1_res")
        if saved and saved[0] == sector and saved[1]:
            _show_result(df, sector, saved[1], "aa1")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_all:
        st.caption("Runs the rule-based agents on every sector table and compares the sectors.")
        kinds_all = st.multiselect("Chart types", ac.CHART_TYPES, default=ac.CHART_TYPES, key="aa2_kinds")
        if st.button("▶ Run all sectors", key="aa2_run"):
            st.session_state["aa2_res"] = _all_sectors_summary(kinds_all or ac.CHART_TYPES, 15)
        saved = st.session_state.get("aa2_res")
        if saved:
            import plotly.express as px
            summ, finds = saved
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(px.bar(summ.sort_values("Records", ascending=False), x="Sector", y="Records",
                                       title="Records per sector"), use_container_width=True, key="aa2_bar")
                st.plotly_chart(px.scatter(summ, x="Records", y="Numeric columns", hover_name="Sector",
                                           size="Columns", title="Records vs numeric columns"),
                                use_container_width=True, key="aa2_sc")
                st.plotly_chart(px.histogram(summ, x="Records", nbins=10, title="Distribution of sector sizes"),
                                use_container_width=True, key="aa2_hi")
            with c2:
                st.plotly_chart(px.pie(summ, names="Sector", values="Records", title="Share of all records"),
                                use_container_width=True, key="aa2_pie")
                st.plotly_chart(px.line(summ.sort_values("Records", ascending=False), x="Sector",
                                        y="Charts planned", markers=True, title="Charts planned per sector"),
                                use_container_width=True, key="aa2_line")
            st.subheader("Sector table")
            st.dataframe(summ, use_container_width=True, hide_index=True)
            st.subheader("Key findings per sector")
            st.dataframe(finds, use_container_width=True, hide_index=True)
            st.download_button("⬇️ All findings (CSV)", finds.to_csv(index=False).encode("utf-8"),
                               file_name="all_sector_findings.csv", mime="text/csv", key="aa2_dl")

    with tab_csv:
        up = st.file_uploader("Upload a CSV", type=["csv"], key="aa3_up")
        if up is not None:
            try:
                df = ac.coerce_numeric(pd.read_csv(up))
            except Exception as e:  # noqa: BLE001
                st.error(f"Could not read that file: {e}")
                df = None
            if df is not None and len(df):
                st.caption(f"{len(df)} rows × {len(df.columns)} columns")
                mode, creds, kinds, top_n = _controls("aa3", allow_crew=True)
                if st.button("▶ Run agents on my CSV", key="aa3_run"):
                    st.session_state["aa3_res"] = _run(df, "Uploaded CSV", mode, creds, kinds, top_n)
                if st.session_state.get("aa3_res"):
                    _show_result(df, "Uploaded CSV", st.session_state["aa3_res"], "aa3")
        else:
            st.info("Upload a CSV to analyse it with the same agents.")
