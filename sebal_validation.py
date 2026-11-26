"""
sebal_validation.py
Validation of SEBAL evapotranspiration / energy-balance outputs against FIELD MEASUREMENTS
(weighing lysimeters, eddy-covariance towers, Bowen-ratio stations, scintillometers,
soil-water-balance plots).

Honest scope
------------
This module provides the validation WORKFLOW and statistics. A model is only "validated" once
it has been compared with real, independent field data for the same place, day and footprint -
the dashboard therefore reports "NOT VALIDATED" until field measurements are supplied, and
shows the real result (pass / partial / fail) once they are. The built-in demo mode uses
SYNTHETIC "measurements" generated from the model output and is labelled as a demonstration
only; it must never be quoted as validation.

Statistics (standard in the ET-validation literature):
  MBE (bias), % bias, MAE, RMSE, normalised RMSE (% of mean observed), Pearson r and R^2,
  OLS slope / intercept, Nash-Sutcliffe efficiency (NSE), Willmott index of agreement (d),
  and the share of points within +/-10 % and +/-20 % of the observation.

Indicative acceptance criteria (editable in the UI) follow the accuracy levels usually quoted
for SEBAL / METRIC studies (e.g. Bastiaanssen et al. 2005, J. Irrig. Drain. Eng. 131(1);
Allen et al. 2007, J. Irrig. Drain. Eng. 133(4)): daily-scale errors of roughly 10-20 %,
smaller for seasonal totals. They are guidance, not a standard - verify against the
literature that fits your crop, climate and scale.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

# result column, observed column, unit
VARIABLES = {
    "ET24 - daily ET (mm/day)": ("ET24_mm_day", "ET_obs_mm_day", "mm/day"),
    "Instantaneous ET (mm/hr)": ("ET_inst_mm_hr", "ET_obs_inst_mm_hr", "mm/hr"),
    "Latent heat flux LE (W/m2)": ("LE_Wm2", "LE_obs_Wm2", "W/m2"),
    "Sensible heat flux H (W/m2)": ("H_Wm2", "H_obs_Wm2", "W/m2"),
    "Net radiation Rn (W/m2)": ("Rn_Wm2", "Rn_obs_Wm2", "W/m2"),
    "Soil heat flux G (W/m2)": ("G_Wm2", "G_obs_Wm2", "W/m2"),
}
METHODS = ["Weighing lysimeter", "Eddy covariance", "Bowen ratio",
           "Large-aperture scintillometer", "Soil-water balance", "Other"]

DEFAULT_CRITERIA = {"nrmse": 20.0, "pbias": 10.0, "r2": 0.70, "d": 0.85}


# ----------------------------------------------------------------------------- statistics
def compute_metrics(obs, sim) -> dict:
    """Goodness-of-fit statistics for paired observed / simulated values (NaN pairs dropped)."""
    o = np.asarray(obs, dtype=float)
    s = np.asarray(sim, dtype=float)
    ok = np.isfinite(o) & np.isfinite(s)
    o, s = o[ok], s[ok]
    n = int(len(o))
    out = {"n": n}
    if n == 0:
        return out
    mo, ms = float(o.mean()), float(s.mean())
    err = s - o
    rmse = float(np.sqrt(np.mean(err ** 2)))
    out.update({
        "mean_obs": mo, "mean_sim": ms,
        "mbe": float(err.mean()),
        "pbias": float(100.0 * err.sum() / o.sum()) if o.sum() != 0 else float("nan"),
        "mae": float(np.mean(np.abs(err))),
        "rmse": rmse,
        "nrmse": float(100.0 * rmse / mo) if mo != 0 else float("nan"),
    })
    den_nse = float(np.sum((o - mo) ** 2))
    out["nse"] = float(1.0 - np.sum(err ** 2) / den_nse) if den_nse > 0 else float("nan")
    den_d = float(np.sum((np.abs(s - mo) + np.abs(o - mo)) ** 2))
    out["d"] = float(1.0 - np.sum(err ** 2) / den_d) if den_d > 0 else float("nan")
    if n >= 3 and np.std(o) > 0 and np.std(s) > 0:
        r = float(np.corrcoef(o, s)[0, 1])
        slope, intercept = np.polyfit(o, s, 1)
        out.update({"r": r, "r2": r * r, "slope": float(slope), "intercept": float(intercept)})
    else:
        out.update({"r": float("nan"), "r2": float("nan"), "slope": float("nan"),
                    "intercept": float("nan")})
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.abs(err) / np.abs(o)
    rel = rel[np.isfinite(rel)]
    out["within10"] = float(100.0 * np.mean(rel <= 0.10)) if len(rel) else float("nan")
    out["within20"] = float(100.0 * np.mean(rel <= 0.20)) if len(rel) else float("nan")
    return out


def check_criteria(m: dict, crit: dict) -> list:
    """List of (name, value, requirement, passed) for the acceptance criteria."""
    def _ok(v, test):
        return bool(np.isfinite(v) and test(v))
    return [
        ("Normalised RMSE (% of mean observed)", m.get("nrmse", np.nan), f"<= {crit['nrmse']:g} %",
         _ok(m.get("nrmse", np.nan), lambda v: v <= crit["nrmse"])),
        ("Absolute % bias", abs(m.get("pbias", np.nan)), f"<= {crit['pbias']:g} %",
         _ok(abs(m.get("pbias", np.nan)), lambda v: v <= crit["pbias"])),
        ("R-squared", m.get("r2", np.nan), f">= {crit['r2']:g}",
         _ok(m.get("r2", np.nan), lambda v: v >= crit["r2"])),
        ("Willmott index of agreement (d)", m.get("d", np.nan), f">= {crit['d']:g}",
         _ok(m.get("d", np.nan), lambda v: v >= crit["d"])),
    ]


def loocv_bias_correction(obs, sim):
    """Leave-one-out cross-validated linear correction obs ~ a + b*sim.
    Returns the corrected simulated values (each point predicted by a fit that excluded it)."""
    o = np.asarray(obs, dtype=float)
    s = np.asarray(sim, dtype=float)
    out = np.full(len(o), np.nan)
    for i in range(len(o)):
        keep = np.arange(len(o)) != i
        so, oo = s[keep], o[keep]
        if len(so) >= 3 and np.std(so) > 0:
            b, a = np.polyfit(so, oo, 1)
            out[i] = a + b * s[i]
        else:
            out[i] = s[i] + float(np.mean(oo - so))
    return out


def force_energy_balance_closure(df: pd.DataFrame) -> pd.DataFrame:
    """Eddy-covariance / Bowen-ratio closure correction: keep the Bowen ratio H/LE and force
    H + LE = Rn - G. Adds LE_obs_Wm2_closed and H_obs_Wm2_closed (needs LE, H, Rn, G columns)."""
    work = df.copy()
    need = ["LE_obs_Wm2", "H_obs_Wm2", "Rn_obs_Wm2", "G_obs_Wm2"]
    if not all(c in work.columns for c in need):
        return work
    le = pd.to_numeric(work["LE_obs_Wm2"], errors="coerce")
    h = pd.to_numeric(work["H_obs_Wm2"], errors="coerce")
    avail = pd.to_numeric(work["Rn_obs_Wm2"], errors="coerce") - pd.to_numeric(work["G_obs_Wm2"], errors="coerce")
    tot = le + h
    ratio = avail / tot.where(tot != 0)
    work["Closure_ratio"] = (tot / avail.where(avail != 0))
    work["LE_obs_Wm2_closed"] = le * ratio
    work["H_obs_Wm2_closed"] = h * ratio
    return work


# ----------------------------------------------------------------------------- data helpers
def field_template() -> pd.DataFrame:
    return pd.DataFrame([{
        "Name": "Dense irrigated cropland - Zone 1", "Day_of_Year": 180,
        "Method": "Weighing lysimeter", "ET_obs_mm_day": 6.1, "LE_obs_Wm2": "", "H_obs_Wm2": "",
        "Rn_obs_Wm2": "", "G_obs_Wm2": "", "Notes": "example row - replace with your measurements",
    }])


def synthetic_field_data(results: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    """SYNTHETIC 'measurements' = model output with noise and a small bias. Demonstration only."""
    rng = np.random.default_rng(seed)
    et = results["ET24_mm_day"].to_numpy(float)
    obs = np.clip(et * (1.0 + rng.normal(-0.03, 0.12, len(et))) + rng.normal(0, 0.25, len(et)), 0.05, None)
    methods = [METHODS[i % 3] for i in range(len(et))]
    return pd.DataFrame({"Name": results["Name"].astype(str).to_numpy(), "Method": methods,
                         "ET_obs_mm_day": np.round(obs, 2)})


def _norm_name(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.casefold()


def pair_with_results(field: pd.DataFrame, results: pd.DataFrame, sim_col: str, obs_col: str):
    """Match field rows to SEBAL rows by Name (and Day_of_Year when both tables have it)."""
    f = field.copy()
    f.columns = [str(c).strip() for c in f.columns]
    if "Name" not in f.columns or obs_col not in f.columns:
        raise ValueError(f"Field file needs the columns 'Name' and '{obs_col}'.")
    f["_key"] = _norm_name(f["Name"])
    f[obs_col] = pd.to_numeric(f[obs_col], errors="coerce")
    f = f.dropna(subset=[obs_col])
    r = results.copy()
    r["_key"] = _norm_name(r["Name"])
    keys = ["_key"]
    if "Day_of_Year" in f.columns and "Day_of_Year" in r.columns:
        f["Day_of_Year"] = pd.to_numeric(f["Day_of_Year"], errors="coerce")
        r["Day_of_Year"] = pd.to_numeric(r["Day_of_Year"], errors="coerce")
        keys.append("Day_of_Year")
    keep_f = keys + [obs_col] + (["Method"] if "Method" in f.columns else [])
    keep_f = list(dict.fromkeys(keep_f))
    merged = f[keep_f].merge(r[keys + ["Name", sim_col]], on=keys, how="inner")
    merged = merged.rename(columns={obs_col: "Observed", sim_col: "SEBAL"})
    cols = ["Name", "Observed", "SEBAL"] + (["Method"] if "Method" in merged.columns else [])
    return merged[cols].reset_index(drop=True), int(len(f)), int(len(merged))


# ----------------------------------------------------------------------------- figures
def scatter_figure(paired: pd.DataFrame, unit: str, label: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    o = paired["Observed"].to_numpy(float)
    s = paired["SEBAL"].to_numpy(float)
    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    hi = float(max(np.nanmax(o), np.nanmax(s)) * 1.1) if len(o) else 1.0
    xs = np.array([0, hi])
    ax.fill_between(xs, xs * 0.8, xs * 1.2, color="#d9ead3", alpha=0.7, label="+/-20 %")
    ax.plot(xs, xs, color="#222", lw=1.4, label="1:1 line")
    if len(o) >= 3 and np.std(o) > 0:
        b, a = np.polyfit(o, s, 1)
        ax.plot(xs, a + b * xs, color="#c0392b", lw=1.6, ls="--", label=f"fit: y = {a:.2f} + {b:.2f}x")
    if "Method" in paired.columns:
        for m, g in paired.groupby("Method"):
            ax.scatter(g["Observed"], g["SEBAL"], s=48, label=str(m), edgecolor="white", zorder=3)
    else:
        ax.scatter(o, s, s=48, color="#2c6fbb", edgecolor="white", zorder=3, label="sites")
    ax.set_xlim(0, hi)
    ax.set_ylim(0, hi)
    ax.set_xlabel(f"Observed {label} ({unit})")
    ax.set_ylabel(f"SEBAL {label} ({unit})")
    ax.set_title("SEBAL vs field measurements", fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=7.5, loc="upper left")
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def bars_figure(paired: pd.DataFrame, unit: str, label: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [str(n)[:28] for n in paired["Name"]]
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(max(6.0, 0.7 * len(names) + 2), 4.2))
    ax.bar(x - 0.2, paired["Observed"], width=0.4, color="#4a8fd6", label="Observed (field)")
    ax.bar(x + 0.2, paired["SEBAL"], width=0.4, color="#e08a3c", label="SEBAL")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel(f"{label} ({unit})")
    ax.set_title("Observed vs SEBAL by site", fontsize=11)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


# ----------------------------------------------------------------------------- UI
def _fmt(v, nd=2):
    return "n/a" if v is None or not np.isfinite(v) else f"{v:.{nd}f}"


def _metric_row(m: dict, unit: str):
    c = st.columns(4)
    c[0].metric("Observations (n)", m["n"])
    c[1].metric("RMSE", f"{_fmt(m.get('rmse'))} {unit}")
    c[2].metric("Normalised RMSE", f"{_fmt(m.get('nrmse'), 1)} %")
    c[3].metric("% bias", f"{_fmt(m.get('pbias'), 1)} %")
    c = st.columns(4)
    c[0].metric("MAE", f"{_fmt(m.get('mae'))} {unit}")
    c[1].metric("R-squared", _fmt(m.get("r2")))
    c[2].metric("Willmott d", _fmt(m.get("d")))
    c[3].metric("NSE", _fmt(m.get("nse")))


def render(results):
    """results = the SEBAL results DataFrame from the model tab (or None)."""
    st.subheader("✅ Validate SEBAL against field measurements")
    st.markdown(
        "SEBAL is only trustworthy for a place once its output has been **compared with independent "
        "field data** - weighing lysimeters, eddy-covariance towers, Bowen-ratio stations, "
        "scintillometers or soil-water-balance plots. Upload your measurements below; this tab pairs "
        "them with the SEBAL run, computes the standard error statistics and checks them against "
        "acceptance criteria that you can edit."
    )
    st.warning(
        "**Status: NOT VALIDATED** until you upload real field measurements for the same sites and "
        "dates. The demo mode below uses *synthetic* data to show the workflow only - never quote it "
        "as validation."
    )

    mode = st.radio(
        "Validation data",
        ["Upload field measurements (match to the SEBAL run by Name)",
         "Upload a paired table (Observed + SEBAL columns)",
         "Demo with SYNTHETIC measurements (workflow only)"],
        key="sebv_mode",
    )
    var_label = st.selectbox("Variable to validate", list(VARIABLES), key="sebv_var")
    sim_col, obs_col, unit = VARIABLES[var_label]
    short = var_label.split("(")[0].strip()

    synthetic = mode.startswith("Demo")
    paired = None
    n_field = n_match = None

    with st.expander("📄 What to upload", expanded=False):
        st.markdown(
            "**Field-measurement CSV** (matched to the SEBAL run by `Name`): columns `Name`, "
            f"`{obs_col}` (the measured value in {unit}), optional `Day_of_Year` (matched when the "
            "SEBAL table has it too), `Method`, and for eddy-covariance / Bowen-ratio data `LE_obs_Wm2`, "
            "`H_obs_Wm2`, `Rn_obs_Wm2`, `G_obs_Wm2`.\n\n"
            "**Paired table:** one row per observation with `Observed` and `SEBAL` columns "
            "(optional `Name`, `Method`) - use this to validate SEBAL results you computed elsewhere "
            "(e.g. from satellite imagery).\n\n"
            "**For a fair comparison:** use the same day / satellite overpass, a field that fills the "
            "sensor footprint and the ~30 m pixel, and for eddy-covariance data apply energy-balance "
            "closure correction (option below)."
        )
        st.download_button("⬇️ Download field-measurement template",
                           data=field_template().to_csv(index=False).encode("utf-8"),
                           file_name="sebal_field_measurements_template.csv", mime="text/csv",
                           key="sebv_tpl")

    if mode.startswith("Upload field"):
        if results is None or len(results) == 0:
            st.info("Run the SEBAL model in the first tab (demo, upload or table) so there is a result to "
                    "validate, then upload your field measurements here.")
        else:
            up = st.file_uploader("Upload field-measurement CSV", type=["csv"], key="sebv_up")
            if up is not None:
                try:
                    field = pd.read_csv(up)
                except Exception as e:  # noqa: BLE001
                    st.error(f"Could not read the CSV: {e}")
                    field = None
                if field is not None:
                    if st.checkbox("Apply energy-balance closure correction to eddy-covariance / "
                                   "Bowen-ratio fluxes (needs LE, H, Rn and G columns)",
                                   value=False, key="sebv_close"):
                        field = force_energy_balance_closure(field)
                        if "LE_obs_Wm2_closed" in field.columns and obs_col == "LE_obs_Wm2":
                            field["LE_obs_Wm2"] = field["LE_obs_Wm2_closed"]
                        if "H_obs_Wm2_closed" in field.columns and obs_col == "H_obs_Wm2":
                            field["H_obs_Wm2"] = field["H_obs_Wm2_closed"]
                        if "Closure_ratio" in field.columns:
                            cr = pd.to_numeric(field["Closure_ratio"], errors="coerce").dropna()
                            if len(cr):
                                st.caption(f"Mean energy-balance closure ratio (H+LE)/(Rn-G) before "
                                           f"correction: {cr.mean():.2f}")
                    try:
                        paired, n_field, n_match = pair_with_results(field, results, sim_col, obs_col)
                    except ValueError as e:
                        st.error(str(e))
                    if paired is not None and n_match < n_field:
                        st.warning(f"{n_field - n_match} of {n_field} field rows did not match a SEBAL "
                                   "row by Name (and Day_of_Year) and were skipped.")
            else:
                st.info("Upload your field-measurement CSV to start the validation.")

    elif mode.startswith("Upload a paired"):
        up = st.file_uploader("Upload paired CSV (Observed, SEBAL)", type=["csv"], key="sebv_up2")
        if up is not None:
            try:
                p = pd.read_csv(up)
                p.columns = [str(c).strip() for c in p.columns]
                low = {c.lower(): c for c in p.columns}
                if "observed" not in low or "sebal" not in low:
                    st.error("The file needs 'Observed' and 'SEBAL' columns.")
                else:
                    paired = pd.DataFrame({
                        "Name": p[low["name"]].astype(str) if "name" in low else
                        [f"Obs {i + 1}" for i in range(len(p))],
                        "Observed": pd.to_numeric(p[low["observed"]], errors="coerce"),
                        "SEBAL": pd.to_numeric(p[low["sebal"]], errors="coerce"),
                    })
                    if "method" in low:
                        paired["Method"] = p[low["method"]].astype(str)
                    paired = paired.dropna(subset=["Observed", "SEBAL"]).reset_index(drop=True)
            except Exception as e:  # noqa: BLE001
                st.error(f"Could not read the CSV: {e}")
        else:
            st.info("Upload a CSV with Observed and SEBAL columns.")

    else:  # synthetic demo
        if results is None or len(results) == 0:
            st.info("Run the SEBAL model in the first tab first - the demo creates synthetic "
                    "'measurements' from its output.")
        else:
            st.error("DEMONSTRATION ONLY - the 'field measurements' below are synthetic (SEBAL output "
                     "plus random noise). This is not validation.")
            fake = synthetic_field_data(results)
            if obs_col != "ET_obs_mm_day":
                st.info("The synthetic demo only provides daily ET; switch the variable to ET24.")
            else:
                paired, n_field, n_match = pair_with_results(fake, results, "ET24_mm_day", "ET_obs_mm_day")
                unit, short = "mm/day", "ET24"

    if paired is None or len(paired) == 0:
        return

    # ------------------------------------------------------------- results
    st.markdown("---")
    with st.expander("⚙️ Acceptance criteria (editable)", expanded=False):
        c1, c2, c3, c4, c5 = st.columns(5)
        crit = {
            "nrmse": c1.number_input("Max nRMSE (%)", value=DEFAULT_CRITERIA["nrmse"], step=1.0, key="sebv_c1"),
            "pbias": c2.number_input("Max |% bias|", value=DEFAULT_CRITERIA["pbias"], step=1.0, key="sebv_c2"),
            "r2": c3.number_input("Min R-squared", value=DEFAULT_CRITERIA["r2"], step=0.05, key="sebv_c3"),
            "d": c4.number_input("Min Willmott d", value=DEFAULT_CRITERIA["d"], step=0.05, key="sebv_c4"),
        }
        min_n = int(c5.number_input("Min observations", value=10, step=1, min_value=3, key="sebv_c5"))
        st.caption("Defaults reflect accuracy levels commonly quoted for SEBAL / METRIC (daily errors of "
                   "roughly 10-20 %). They are guidance, not a standard - set them to what your project "
                   "requires.")

    m = compute_metrics(paired["Observed"], paired["SEBAL"])
    checks = check_criteria(m, crit)
    n_pass = sum(1 for c in checks if c[3])

    if synthetic:
        st.error("DEMO RESULT (synthetic data) - not a validation of SEBAL.")
    elif m["n"] < min_n:
        st.warning(f"**INSUFFICIENT DATA** - {m['n']} observation(s); at least {min_n} are needed before "
                   f"claiming validation. {n_pass} of {len(checks)} criteria currently met.")
    elif n_pass == len(checks):
        st.success(f"**VALIDATED for this dataset** - all {len(checks)} criteria met against {m['n']} field "
                   "observations. Valid only for the conditions, sites and season covered by the data.")
    elif n_pass >= 2:
        st.warning(f"**PARTIALLY VALIDATED** - {n_pass} of {len(checks)} criteria met. Review bias and "
                   "scatter below; consider calibration (hot/cold pixels) or checking the field data.")
    else:
        st.error(f"**NOT VALIDATED** - only {n_pass} of {len(checks)} criteria met.")

    _metric_row(m, unit)
    st.dataframe(pd.DataFrame([{"Criterion": c[0], "Value": round(float(c[1]), 3) if np.isfinite(c[1]) else None,
                                "Requirement": c[2], "Result": "✅ pass" if c[3] else "❌ fail"}
                               for c in checks]), use_container_width=True, hide_index=True)

    colA, colB = st.columns(2)
    with colA:
        st.pyplot(scatter_figure(paired, unit, short), clear_figure=True)
    with colB:
        st.pyplot(bars_figure(paired, unit, short), clear_figure=True)

    st.markdown(
        f"Regression of SEBAL on observed: slope **{_fmt(m.get('slope'))}**, intercept "
        f"**{_fmt(m.get('intercept'))} {unit}** (ideal: 1 and 0). Mean observed "
        f"{_fmt(m.get('mean_obs'))} {unit}, mean SEBAL {_fmt(m.get('mean_sim'))} {unit}. "
        f"{_fmt(m.get('within10'), 0)} % of points are within +/-10 % and "
        f"{_fmt(m.get('within20'), 0)} % within +/-20 % of the observation."
    )

    detail = paired.copy()
    detail["Error"] = detail["SEBAL"] - detail["Observed"]
    detail["Error %"] = np.where(detail["Observed"] != 0, 100.0 * detail["Error"] / detail["Observed"], np.nan)
    st.subheader("Site-by-site comparison")
    st.dataframe(detail.round(3), use_container_width=True, hide_index=True)

    if "Method" in paired.columns and paired["Method"].nunique() > 1:
        rows = []
        for meth, g in paired.groupby("Method"):
            mm = compute_metrics(g["Observed"], g["SEBAL"])
            rows.append({"Method": meth, "n": mm["n"], "RMSE": mm.get("rmse"), "nRMSE %": mm.get("nrmse"),
                         "% bias": mm.get("pbias"), "R2": mm.get("r2"), "d": mm.get("d")})
        st.subheader("Performance by measurement method")
        st.dataframe(pd.DataFrame(rows).round(3), use_container_width=True, hide_index=True)

    if m["n"] >= 6:
        with st.expander("🔧 Bias correction with leave-one-out cross-validation", expanded=False):
            st.markdown(
                "Fits a linear correction `observed = a + b x SEBAL`. To avoid grading the model on the "
                "data it was tuned on, each point is corrected by a fit that **excluded that point** "
                "(leave-one-out cross-validation). If the cross-validated error is not clearly lower, "
                "the correction is not adding real skill."
            )
            corr = loocv_bias_correction(paired["Observed"], paired["SEBAL"])
            m2 = compute_metrics(paired["Observed"], corr)
            cmp_df = pd.DataFrame([
                {"Version": "Raw SEBAL", "RMSE": m["rmse"], "nRMSE %": m["nrmse"], "% bias": m["pbias"],
                 "R2": m["r2"], "d": m["d"]},
                {"Version": "Bias-corrected (LOO-CV)", "RMSE": m2["rmse"], "nRMSE %": m2["nrmse"],
                 "% bias": m2["pbias"], "R2": m2["r2"], "d": m2["d"]},
            ])
            st.dataframe(cmp_df.round(3), use_container_width=True, hide_index=True)

    st.subheader("Export")
    metrics_df = pd.DataFrame([{"Metric": k, "Value": v} for k, v in m.items()])
    c1, c2 = st.columns(2)
    c1.download_button("⬇️ Paired observed / SEBAL table (CSV)",
                       data=detail.to_csv(index=False).encode("utf-8"),
                       file_name="sebal_validation_pairs.csv", mime="text/csv", key="sebv_dl1")
    c2.download_button("⬇️ Validation statistics (CSV)",
                       data=metrics_df.to_csv(index=False).encode("utf-8"),
                       file_name="sebal_validation_metrics.csv", mime="text/csv", key="sebv_dl2")
