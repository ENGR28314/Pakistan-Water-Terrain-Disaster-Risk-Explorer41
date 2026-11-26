"""
sebal_engine.py
SEBAL Model: Indus Basin Advanced Evapotranspiration Engine
Created and designed by Engr. Syed Hassan Iqbal Shah (ELECT/28314).

An offline, upload-driven implementation of the published SEBAL / METRIC
surface-energy-balance evapotranspiration algorithm. This module does NOT
pull live satellite imagery (no earthengine-api / geemap / GEE account) —
it operates on a per-zone or per-pixel table of remote-sensing-derived
inputs that the user uploads or edits by hand (NDVI, albedo, land-surface
temperature, air temperature, incoming shortwave radiation, wind speed,
optionally crop/canopy height, elevation, and coordinates), the same
upload-driven pattern used elsewhere in this dashboard
(file_import.load_csv_generic / load_any_generic).

Physics and formulation implemented here (re-derived from the published
literature; no proprietary or third-party source code was used):

  - Bastiaanssen, W.G.M. et al. (1998). "A remote sensing surface energy
    balance algorithm for land (SEBAL) 1. Formulation." J. Hydrology 212-213.
    -> original SEBAL formulation: Rn = G + H + LE, soil heat flux (G) as an
       empirical function of NDVI, albedo and surface temperature, hot/cold
       anchor-pixel calibration of the near-surface temperature gradient.

  - Allen, R.G., Tasumi, M., Trezza, R. (2007). "Satellite-Based Energy
    Balance for Mapping Evapotranspiration with Internalized Calibration
    (METRIC) — Model." J. Irrigation and Drainage Engineering 133(4).
    -> METRIC refinements used here: NDVI-based LAI and surface emissivity,
       the dT = a + b*Ts hot/cold pixel calibration, evaporative-fraction
       upscaling of instantaneous LE to a 24-hour ET24 depth.

  - Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). FAO Irrigation
    and Drainage Paper 56 ("FAO-56"). -> solar-geometry formulas for
    extraterrestrial radiation (Ra) and clear-sky radiation (Rso) from
    latitude, day-of-year and elevation, used as a fallback when the user
    does not supply measured daily radiation.

  - Brutsaert, W. (1982). "Evaporation into the Atmosphere." -> empirical
    relation between vegetation (canopy) height and aerodynamic roughness
    length for momentum (zom).

  - Paulson, C.A. (1970) and Webb, E.K. (1970). -> Monin-Obukhov atmospheric
    stability correction functions (psi_m, psi_h) used in the iterative
    aerodynamic-resistance solution for sensible heat flux.

This is an educational / illustrative re-implementation. It has NOT been
validated against field lysimeter or eddy-covariance data and should not be
used for operational irrigation scheduling or water-allocation decisions
without independent calibration and validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
STEFAN_BOLTZMANN = 5.670374e-8      # W / m^2 / K^4
SOLAR_CONSTANT = 1367.0              # W / m^2 (extraterrestrial)
VON_KARMAN = 0.41
AIR_DENSITY_SEA_LEVEL = 1.225        # kg / m^3 (approx, used if not derived)
SPECIFIC_HEAT_AIR = 1004.0           # J / kg / K
GRAVITY = 9.81                       # m / s^2
BLENDING_HEIGHT_M = 200.0            # SEBAL's standard reference height
WIND_MEASUREMENT_HEIGHT_M = 2.0      # default anemometer height if not supplied
LATENT_HEAT_VAPORIZATION = 2.45e6    # J / kg (~constant, at ~20C)

REQUIRED_COLUMNS = ["Name", "NDVI", "Albedo", "Ts_C", "Ta_C", "Rs_down", "Wind_ms"]
OPTIONAL_COLUMNS = [
    "Latitude", "Longitude", "Elevation_m", "Crop_Height_m",
    "Day_of_Year", "Transmissivity",
]

COLUMN_ALIASES = {
    "name": "Name", "zone": "Name", "site": "Name", "id": "Name", "label": "Name",
    "ndvi": "NDVI",
    "albedo": "Albedo", "surface_albedo": "Albedo",
    "ts_c": "Ts_C", "ts": "Ts_C", "lst_c": "Ts_C", "surface_temp_c": "Ts_C", "lst": "Ts_C",
    "ta_c": "Ta_C", "ta": "Ta_C", "air_temp_c": "Ta_C",
    "rs_down": "Rs_down", "rs": "Rs_down", "incoming_shortwave": "Rs_down", "solar_radiation": "Rs_down",
    "wind_ms": "Wind_ms", "wind_speed": "Wind_ms", "wind_speed_ms": "Wind_ms", "u2": "Wind_ms",
    "latitude": "Latitude", "lat": "Latitude",
    "longitude": "Longitude", "lon": "Longitude", "lng": "Longitude",
    "elevation_m": "Elevation_m", "elevation": "Elevation_m", "elev": "Elevation_m",
    "crop_height_m": "Crop_Height_m", "crop_height": "Crop_Height_m", "canopy_height_m": "Crop_Height_m",
    "day_of_year": "Day_of_Year", "doy": "Day_of_Year",
    "transmissivity": "Transmissivity", "tau": "Transmissivity",
}


class SebalInputError(Exception):
    """Raised when an uploaded dataset can't be used for the SEBAL run."""


# ---------------------------------------------------------------------------
# Input normalization
# ---------------------------------------------------------------------------
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename recognizable headers to the canonical schema used below."""
    if df is None or df.empty:
        raise SebalInputError("The uploaded table has no rows.")
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    rename_map = {}
    for col in out.columns:
        key = col.strip().lower().replace(" ", "_").replace("-", "_")
        if key in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[key]
    out = out.rename(columns=rename_map)

    missing = [c for c in REQUIRED_COLUMNS if c not in out.columns]
    if missing:
        raise SebalInputError(
            "Missing required column(s) for a SEBAL run: " + ", ".join(missing) +
            ". Required: Name, NDVI, Albedo, Ts_C (surface temperature), "
            "Ta_C (air temperature), Rs_down (incoming shortwave, W/m^2), "
            "Wind_ms (wind speed, m/s). Use the downloadable template as a guide."
        )

    for c in REQUIRED_COLUMNS[1:]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    for c in OPTIONAL_COLUMNS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    out = out.dropna(subset=REQUIRED_COLUMNS[1:]).reset_index(drop=True)
    if out.empty:
        raise SebalInputError(
            "No rows had valid numeric values in all required columns after parsing."
        )
    return out


def generate_sample_dataset(n: int = 8, seed: int = 42) -> pd.DataFrame:
    """A clearly-synthetic demo dataset spanning a plausible Indus-basin range
    of land covers (bare soil/desert fringe through irrigated cropland), so
    the page has something to show before a real file is uploaded."""
    rng = np.random.default_rng(seed)
    land_covers = [
        "Dense irrigated cropland", "Moderate cropland", "Mixed cropland/fallow",
        "Sparse vegetation", "Bare soil / fallow", "Desert fringe",
        "Orchard / tree cover", "Riparian / wetland",
    ]
    rows = []
    for i in range(n):
        cover = land_covers[i % len(land_covers)]
        # NDVI roughly tracks vegetation density of the label
        base_ndvi = {
            "Dense irrigated cropland": 0.75, "Moderate cropland": 0.55,
            "Mixed cropland/fallow": 0.40, "Sparse vegetation": 0.28,
            "Bare soil / fallow": 0.12, "Desert fringe": 0.08,
            "Orchard / tree cover": 0.65, "Riparian / wetland": 0.70,
        }[cover]
        ndvi = float(np.clip(base_ndvi + rng.normal(0, 0.03), 0.02, 0.92))
        albedo = float(np.clip(0.30 - 0.18 * ndvi + rng.normal(0, 0.01), 0.08, 0.35))
        ts = float(np.clip(42 - 10 * ndvi + rng.normal(0, 0.8), 22, 48))
        rows.append({
            "Name": f"{cover} — Zone {i + 1}",
            "NDVI": round(ndvi, 3),
            "Albedo": round(albedo, 3),
            "Ts_C": round(ts, 2),
            "Ta_C": round(float(34 + rng.normal(0, 0.5)), 2),
            "Rs_down": round(float(820 + rng.normal(0, 15)), 1),
            "Wind_ms": round(float(np.clip(2.5 + rng.normal(0, 0.6), 0.5, 6.0)), 2),
            "Crop_Height_m": round(float(np.clip(0.1 + 1.1 * ndvi, 0.03, 1.2)), 2),
            "Latitude": round(float(29.5 + rng.uniform(-2.5, 2.5)), 4),
            "Longitude": round(float(70.5 + rng.uniform(-3.0, 3.0)), 4),
            "Elevation_m": round(float(150 + rng.uniform(0, 120)), 1),
            "Day_of_Year": 180,
        })
    return pd.DataFrame(rows)


def csv_template() -> pd.DataFrame:
    """One illustrative row showing the expected upload schema."""
    df = generate_sample_dataset(n=1)
    return df


# ---------------------------------------------------------------------------
# FAO-56 solar-geometry fallback (Allen et al. 1998)
# ---------------------------------------------------------------------------
def extraterrestrial_radiation(latitude_deg: float, day_of_year: int) -> float:
    """Ra, daily extraterrestrial radiation, converted to W/m^2 (FAO-56 eq. 21)."""
    lat_rad = math.radians(latitude_deg)
    dr = 1 + 0.033 * math.cos(2 * math.pi * day_of_year / 365.0)
    decl = 0.409 * math.sin(2 * math.pi * day_of_year / 365.0 - 1.39)
    x = -math.tan(lat_rad) * math.tan(decl)
    x = max(-1.0, min(1.0, x))
    ws = math.acos(x)
    gsc = 0.0820  # MJ / m^2 / min
    ra_mj = (24 * 60 / math.pi) * gsc * dr * (
        ws * math.sin(lat_rad) * math.sin(decl) + math.cos(lat_rad) * math.cos(decl) * math.sin(ws)
    )
    ra_wm2 = ra_mj * 1e6 / 86400.0
    return max(ra_wm2, 1.0)


def clear_sky_radiation(ra_wm2: float, elevation_m: float) -> float:
    """Rso, clear-sky solar radiation (FAO-56 eq. 37)."""
    return ra_wm2 * (0.75 + 2e-5 * elevation_m)


# ---------------------------------------------------------------------------
# Net radiation (Rn)
# ---------------------------------------------------------------------------
def surface_emissivity(ndvi: np.ndarray) -> np.ndarray:
    """NDVI-based broadband surface emissivity (METRIC-style approximation)."""
    ndvi = np.clip(ndvi, 0.001, 0.999)
    ndvi_for_lai = np.clip(ndvi, 0.001, 0.68)  # formula is undefined at/above NDVI=0.69
    lai = -np.log((0.69 - ndvi_for_lai) / 0.59) / 0.91
    lai = np.clip(lai, 0.0, 6.0)
    eps = np.where(ndvi > 0.0, 0.95 + 0.01 * lai, 0.985)
    eps = np.where(ndvi < 0.0, 0.985, eps)  # water/snow-like
    return np.clip(eps, 0.95, 0.99), lai


def compute_net_radiation(df: pd.DataFrame, atm_emissivity: float = 0.85) -> pd.DataFrame:
    out = df.copy()
    ndvi = out["NDVI"].to_numpy(float)
    albedo = out["Albedo"].to_numpy(float)
    ts_k = out["Ts_C"].to_numpy(float) + 273.15
    ta_k = out["Ta_C"].to_numpy(float) + 273.15
    rs_down = out["Rs_down"].to_numpy(float)

    eps_s, lai = surface_emissivity(ndvi)
    out["LAI"] = lai
    out["Surface_Emissivity"] = eps_s

    rs_up = albedo * rs_down                                   # reflected shortwave
    rl_down = atm_emissivity * STEFAN_BOLTZMANN * ta_k ** 4      # incoming longwave
    rl_up = eps_s * STEFAN_BOLTZMANN * ts_k ** 4                 # emitted longwave

    rn = (rs_down - rs_up) + (rl_down - rl_up)
    out["Rs_up"] = rs_up
    out["Rl_down"] = rl_down
    out["Rl_up"] = rl_up
    out["Rn_Wm2"] = rn
    return out


# ---------------------------------------------------------------------------
# Soil heat flux (G) — Bastiaanssen et al. 1998 empirical formula
# ---------------------------------------------------------------------------
def compute_soil_heat_flux(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    ndvi = out["NDVI"].to_numpy(float)
    albedo = out["Albedo"].to_numpy(float)
    ts_c = out["Ts_C"].to_numpy(float)
    rn = out["Rn_Wm2"].to_numpy(float)

    ndvi4 = np.clip(ndvi, 0.001, None) ** 4
    g_ratio = (ts_c / albedo) * (0.0038 * albedo + 0.0074 * albedo ** 2) * (1 - 0.98 * ndvi4)
    g_ratio = np.clip(g_ratio, 0.05, 0.5)   # physically-plausible bound (G/Rn)
    g = g_ratio * rn
    out["G_over_Rn"] = g_ratio
    out["G_Wm2"] = g
    return out


# ---------------------------------------------------------------------------
# Aerodynamics: roughness length, wind extrapolation, Monin-Obukhov iteration
# ---------------------------------------------------------------------------
def roughness_length_momentum(crop_height_m: np.ndarray, ndvi: np.ndarray) -> np.ndarray:
    """zom via Brutsaert (1982) when canopy height is known (zom = 0.123 * h);
    falls back to an NDVI-scaled heuristic (flagged as non-literature) when
    crop height wasn't supplied."""
    h = np.asarray(crop_height_m, dtype=float)
    has_height = ~np.isnan(h) & (h > 0)
    zom = np.where(has_height, 0.123 * np.where(has_height, h, 1.0), np.nan)
    # Heuristic fallback (not from the cited literature — clearly documented):
    fallback = 0.005 + 0.20 * np.clip(ndvi, 0.0, 1.0)
    zom = np.where(has_height, zom, fallback)
    return np.clip(zom, 0.001, 2.0)


def _wind_to_blending_height(u_z: float, z: float, zom: float) -> float:
    """Neutral logarithmic wind profile extrapolation to 200 m."""
    friction_velocity = (u_z * VON_KARMAN) / math.log(max(z / zom, 1.0001))
    u200 = friction_velocity / VON_KARMAN * math.log(BLENDING_HEIGHT_M / zom)
    return max(u200, 0.1)


def _psi_m(zeta: float) -> float:
    """Paulson (1970) stability correction for momentum."""
    if zeta < 0:
        x = (1 - 16 * zeta) ** 0.25
        return 2 * math.log((1 + x) / 2) + math.log((1 + x ** 2) / 2) - 2 * math.atan(x) + math.pi / 2
    return -5 * zeta  # stable (Webb 1970)


def _psi_h(zeta: float) -> float:
    """Paulson (1970) / Webb (1970) stability correction for heat."""
    if zeta < 0:
        x = (1 - 16 * zeta) ** 0.25
        return 2 * math.log((1 + x ** 2) / 2)
    return -5 * zeta


def _solve_sensible_heat_one_pixel(
    rn: float, g: float, dT: float, u_z: float, zom: float, ts_k: float,
    z_wind: float = WIND_MEASUREMENT_HEIGHT_M, max_iter: int = 20,
) -> dict:
    """Iteratively solve H via Monin-Obukhov-corrected aerodynamic resistance,
    given a (pre-calibrated) near-surface temperature difference dT = Ts - Ta
    scaled by the hot/cold pixel calibration (dT = a + b*Ts)."""
    zoh = zom / 7.0  # standard SEBAL assumption: roughness length for heat ~ zom/7
    u200 = _wind_to_blending_height(u_z, z_wind, zom)
    air_density = AIR_DENSITY_SEA_LEVEL

    # Neutral initial aerodynamic resistance (2 m -> blending height path via u*):
    friction_velocity = VON_KARMAN * u200 / math.log(BLENDING_HEIGHT_M / zom)
    friction_velocity = max(friction_velocity, 0.01)
    rah = math.log(BLENDING_HEIGHT_M / zoh) / (VON_KARMAN * friction_velocity)
    rah = max(rah, 1.0)

    h = air_density * SPECIFIC_HEAT_AIR * dT / rah

    for _ in range(max_iter):
        # Monin-Obukhov length
        if abs(h) < 1e-6:
            L = 1e6
        else:
            L = -(air_density * SPECIFIC_HEAT_AIR * friction_velocity ** 3 * ts_k) / (
                VON_KARMAN * GRAVITY * h
            )
        L = max(min(L, 1e6), -1e6)

        zeta_m = BLENDING_HEIGHT_M / L
        zeta_h = BLENDING_HEIGHT_M / L
        psi_m = _psi_m(zeta_m)
        psi_h = _psi_h(zeta_h)

        denom_u = math.log(BLENDING_HEIGHT_M / zom) - psi_m
        denom_u = denom_u if abs(denom_u) > 1e-3 else 1e-3
        friction_velocity_new = VON_KARMAN * u200 / denom_u
        friction_velocity_new = max(abs(friction_velocity_new), 0.01)

        denom_h = math.log(BLENDING_HEIGHT_M / zoh) - psi_h
        denom_h = denom_h if abs(denom_h) > 1e-3 else 1e-3
        rah_new = denom_h / (VON_KARMAN * friction_velocity_new)
        rah_new = max(rah_new, 1.0)

        h_new = air_density * SPECIFIC_HEAT_AIR * dT / rah_new

        if abs(h_new - h) < 0.5 and abs(friction_velocity_new - friction_velocity) < 1e-3:
            h, rah, friction_velocity = h_new, rah_new, friction_velocity_new
            break
        h, rah, friction_velocity = h_new, rah_new, friction_velocity_new

    return {"H_Wm2": h, "rah_s_per_m": rah, "u_star": friction_velocity, "u200_ms": u200}


# ---------------------------------------------------------------------------
# Hot / cold anchor-pixel calibration (Bastiaanssen 1998 / Allen et al. 2007)
# ---------------------------------------------------------------------------
def calibrate_hot_cold_pixels(df: pd.DataFrame, hot_idx: int = None, cold_idx: int = None) -> dict:
    """Pick (or accept user-chosen) hot/cold anchor pixels and fit the linear
    dT = a + b * Ts relationship SEBAL uses to avoid needing absolute air
    temperature at every pixel. Cold pixel: well-watered vegetation (highest
    NDVI, lowest Ts) assumed at ~full ET (dT ~ 0). Hot pixel: bare/dry soil
    (lowest NDVI, highest Ts) assumed at ~zero ET (dT = Rn-G converted via
    rah estimate)."""
    if cold_idx is None:
        cold_idx = int(df["NDVI"].idxmax())
    if hot_idx is None:
        dry_candidates = df[df["NDVI"] < df["NDVI"].quantile(0.35)]
        hot_idx = int((dry_candidates["Ts_C"].idxmax()) if not dry_candidates.empty else df["Ts_C"].idxmax())

    cold = df.loc[cold_idx]
    hot = df.loc[hot_idx]

    dT_cold = 0.0  # cold pixel: all available energy goes to ET, H ~ 0
    # Hot pixel: assume ET ~ 0, so H_hot ~= Rn_hot - G_hot; invert H = rho*cp*dT/rah
    # using a neutral-stability first-guess aerodynamic resistance from the hot
    # pixel's own roughness length and wind speed (not a fixed constant), so the
    # calibration stays physically consistent across very different datasets.
    if "zom_m" in df.columns and "Wind_ms" in df.columns:
        zom_hot = max(float(hot["zom_m"]), 0.001)
        u_hot = max(float(hot["Wind_ms"]), 0.1)
        u200_hot = _wind_to_blending_height(u_hot, WIND_MEASUREMENT_HEIGHT_M, zom_hot)
        ustar_hot = max(VON_KARMAN * u200_hot / math.log(BLENDING_HEIGHT_M / zom_hot), 0.01)
        zoh_hot = zom_hot / 7.0
        rah_est = max(math.log(BLENDING_HEIGHT_M / zoh_hot) / (VON_KARMAN * ustar_hot), 1.0)
    else:
        rah_est = 40.0  # typical neutral-stability order-of-magnitude fallback (s/m)
    h_hot_target = max(hot["Rn_Wm2"] - hot["G_Wm2"], 1.0)
    dT_hot = h_hot_target * rah_est / (AIR_DENSITY_SEA_LEVEL * SPECIFIC_HEAT_AIR)
    dT_hot = min(dT_hot, 20.0)  # cap to the physically-typical SEBAL dT_hot range

    ts_cold, ts_hot = float(cold["Ts_C"]), float(hot["Ts_C"])
    if abs(ts_hot - ts_cold) < 0.5:
        ts_hot = ts_cold + 0.5  # avoid divide-by-zero on a degenerate dataset

    b = (dT_hot - dT_cold) / (ts_hot - ts_cold)
    a = dT_cold - b * ts_cold

    return {
        "cold_pixel_index": cold_idx, "hot_pixel_index": hot_idx,
        "cold_pixel_name": str(cold["Name"]), "hot_pixel_name": str(hot["Name"]),
        "Ts_cold_C": ts_cold, "Ts_hot_C": ts_hot,
        "dT_cold_K": dT_cold, "dT_hot_K": dT_hot,
        "a": a, "b": b,
    }


# ---------------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------------
def run_sebal(
    df: pd.DataFrame,
    hot_idx: int = None,
    cold_idx: int = None,
    atm_emissivity: float = 0.85,
    wind_height_m: float = WIND_MEASUREMENT_HEIGHT_M,
    default_day_of_year: int = 180,
    default_elevation_m: float = 200.0,
) -> tuple[pd.DataFrame, dict]:
    """Run the full SEBAL pipeline on a standardized zone/pixel table and
    return (results_dataframe, calibration_info)."""
    work = standardize_columns(df)
    work = compute_net_radiation(work, atm_emissivity=atm_emissivity)
    work = compute_soil_heat_flux(work)

    zom = roughness_length_momentum(
        work["Crop_Height_m"].to_numpy(float) if "Crop_Height_m" in work.columns
        else np.full(len(work), np.nan),
        work["NDVI"].to_numpy(float),
    )
    work["zom_m"] = zom

    calib = calibrate_hot_cold_pixels(work, hot_idx=hot_idx, cold_idx=cold_idx)
    a, b = calib["a"], calib["b"]

    h_vals, rah_vals, ustar_vals, u200_vals = [], [], [], []
    for i, row in work.iterrows():
        dT = a + b * row["Ts_C"]
        ts_k = row["Ts_C"] + 273.15
        res = _solve_sensible_heat_one_pixel(
            rn=row["Rn_Wm2"], g=row["G_Wm2"], dT=dT,
            u_z=max(row["Wind_ms"], 0.1), zom=row["zom_m"], ts_k=ts_k,
            z_wind=wind_height_m,
        )
        h_vals.append(res["H_Wm2"])
        rah_vals.append(res["rah_s_per_m"])
        ustar_vals.append(res["u_star"])
        u200_vals.append(res["u200_ms"])

    work["dT_K"] = a + b * work["Ts_C"]
    work["H_Wm2"] = h_vals
    work["rah_s_per_m"] = rah_vals
    work["u_star_ms"] = ustar_vals
    work["u200_ms"] = u200_vals

    # Energy balance residual -> latent heat flux, clipped to physical bounds
    le = work["Rn_Wm2"] - work["G_Wm2"] - work["H_Wm2"]
    available_energy = work["Rn_Wm2"] - work["G_Wm2"]
    le = np.clip(le, 0.0, np.maximum(available_energy, 0.0))
    work["LE_Wm2"] = le

    # Instantaneous ET (mm/hr)
    work["ET_inst_mm_hr"] = (work["LE_Wm2"] / LATENT_HEAT_VAPORIZATION) * 3600.0

    # Evaporative fraction and daily ET24 upscaling
    denom = np.maximum(available_energy, 1.0)
    ef = np.clip(work["LE_Wm2"] / denom, 0.0, 1.3)
    work["Evaporative_Fraction"] = ef

    daily_rn = []
    for i, row in work.iterrows():
        lat = row["Latitude"] if "Latitude" in work.columns and not pd.isna(row.get("Latitude", np.nan)) else 30.0
        doy = int(row["Day_of_Year"]) if "Day_of_Year" in work.columns and not pd.isna(row.get("Day_of_Year", np.nan)) else default_day_of_year
        elev = row["Elevation_m"] if "Elevation_m" in work.columns and not pd.isna(row.get("Elevation_m", np.nan)) else default_elevation_m
        ra = extraterrestrial_radiation(lat, doy)
        rso = clear_sky_radiation(ra, elev)
        tau = row["Transmissivity"] if "Transmissivity" in work.columns and not pd.isna(row.get("Transmissivity", np.nan)) else 0.75
        rs24 = tau * ra
        rns24 = (1 - row["Albedo"]) * rs24
        rnl24 = max(0.1 * rns24, 0.0)  # simplified net-longwave-at-day fraction (illustrative)
        rn24 = max(rns24 - rnl24, rso * 0.1)
        daily_rn.append(rn24)
    work["Rn24_Wm2_est"] = daily_rn
    work["ET24_mm_day"] = ef * np.maximum(work["Rn24_Wm2_est"], 0.0) * 86400.0 / LATENT_HEAT_VAPORIZATION

    return work, calib
