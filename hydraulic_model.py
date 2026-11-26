"""
hydraulic_model.py
Simplified, transparent illustrative models — NOT a validated hydrological
or hydraulic simulator. Intended to give dashboard users an interactive
feel for how storage, canal offtake and shortage-sharing work in the
Indus Basin system, and a basic composite disaster-risk-index calculator.

All coefficients are illustrative approximations for teaching/dashboard
purposes and should not be used for engineering or policy decisions.
"""

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# 1. RESERVOIR MASS-BALANCE MODEL (Tarbela / Mangla style)
# ---------------------------------------------------------------------------
# Period-by-period water balance with evaporation, demand-driven release,
# shortage and spill accounting against a live-storage capacity and a
# target (operating) storage level. The exact balance logic below was
# cross-checked period-by-period against an independently-produced 12-period
# reservoir mass-balance sample run (same Inflow/Demand/Evaporation inputs
# reproduce the sample's Release/Shortage/Spill/End storage/Deviation
# columns exactly), so this replaces the earlier simplified cusec-based
# model with one validated against that reference trace.
@dataclass
class ReservoirState:
    name: str
    capacity_maf: float          # live storage capacity (any consistent volume unit)
    current_storage_maf: float   # starting storage, same unit as capacity
    inflow_cusecs: float         # constant per-period inflow, same unit as capacity
    outflow_demand_cusecs: float  # constant per-period demand, same unit as capacity
    evaporation_maf: float = 0.0  # constant per-period evaporation/seepage loss
    target_storage_maf: float = None  # operating target; defaults to capacity * 0.6


def simulate_reservoir(state: ReservoirState, days: int = 30):
    """
    Period-by-period mass balance:
        available      = storage + inflow - evaporation
        release        = min(demand, max(available, 0))
        shortage        = max(0, demand - available)
        spill           = max(0, (available - release) - capacity)
        end_storage     = clamp(available - release, 0, capacity)
    `days` here means "periods" (the model is period-generic — daily,
    weekly or monthly, depending on what the inflow/demand figures represent).
    Returns a list of per-period dicts including Shortage/Spill/Deviation —
    kept as an alias list of dicts for backward compatibility with the
    original day/storage_maf/spilling trace, with the richer fields added.
    """
    target = state.target_storage_maf
    if target is None:
        target = state.capacity_maf * 0.6

    storage = state.current_storage_maf
    trace = []
    for day in range(1, days + 1):
        available = storage + state.inflow_cusecs - state.evaporation_maf
        release = min(state.outflow_demand_cusecs, max(available, 0.0))
        shortage = max(0.0, state.outflow_demand_cusecs - available)
        after_release = available - release
        spill = max(0.0, after_release - state.capacity_maf)
        end_storage = min(state.capacity_maf, max(after_release, 0.0))

        trace.append({
            "day": day,
            "storage_maf": round(end_storage, 3),
            "spilling": spill > 0,
            "inflow": round(state.inflow_cusecs, 3),
            "demand": round(state.outflow_demand_cusecs, 3),
            "evaporation": round(state.evaporation_maf, 3),
            "release": round(release, 3),
            "shortage": round(shortage, 3),
            "spill": round(spill, 3),
            "target_storage": round(target, 3),
            "storage_deviation": round(end_storage - target, 3),
        })
        storage = end_storage
    return trace


# ---------------------------------------------------------------------------
# 2. SHORTAGE-SHARING ALLOCATION (simplified 1991 Water Apportionment logic)
# ---------------------------------------------------------------------------
# Illustrative baseline shares, roughly reflecting historical Kharif/Rabi
# apportionment discussions (NOT the official IRSA formula, simplified for demo).
BASELINE_SHARE_PCT = {
    "Punjab": 0.53,
    "Sindh": 0.42,
    "KPK": 0.03,
    "Balochistan": 0.02,
}


def allocate_shortage(total_available_maf: float, shortage_pct: float = 0.0):
    """
    Distributes total_available_maf across provinces using baseline shares.
    shortage_pct (0-100) applies an equal percentage cut to all provinces,
    mirroring Pakistan's (contested) principle of equal-percentage shortage-sharing.
    """
    effective_total = total_available_maf * (1 - shortage_pct / 100.0)
    return {
        province: round(effective_total * share, 3)
        for province, share in BASELINE_SHARE_PCT.items()
    }


# ---------------------------------------------------------------------------
# 3. COMPOSITE DISASTER RISK INDEX (illustrative, 0-100 scale)
# ---------------------------------------------------------------------------
def composite_disaster_risk_index(
    flood_exposure: float,       # 0-10
    glof_susceptibility: float,  # 0-10
    drought_exposure: float,     # 0-10
    seismic_hazard: float,       # 0-10
    coastal_exposure: float,     # 0-10
    institutional_capacity: float,  # 0-10 (higher = better prepared, reduces risk)
):
    """
    Weighted composite index (illustrative only).
    Risk = weighted hazard sum, adjusted downward by institutional capacity.
    Returns a score 0-100 and a qualitative band.
    """
    hazard_score = (
        0.25 * flood_exposure
        + 0.20 * glof_susceptibility
        + 0.20 * drought_exposure
        + 0.15 * seismic_hazard
        + 0.20 * coastal_exposure
    )  # max 10
    capacity_adjustment = 1 - (institutional_capacity / 20.0)  # 0.5-1.0 multiplier
    raw_score = hazard_score * 10 * capacity_adjustment  # scale to 0-100
    raw_score = max(0, min(100, raw_score))

    if raw_score < 25:
        band = "Low"
    elif raw_score < 50:
        band = "Moderate"
    elif raw_score < 75:
        band = "High"
    else:
        band = "Severe"

    return round(raw_score, 1), band


# ---------------------------------------------------------------------------
# 4. LINK CANAL TRANSFER CALCULATOR
# ---------------------------------------------------------------------------
def link_canal_transfer(source_flow_cusecs: float, canal_capacity_cusecs: float, offtake_pct: float):
    """
    Simplified transfer through a link canal: transfer is capped by both
    the canal's design capacity and the requested offtake percentage of
    the source river's flow.
    """
    requested = source_flow_cusecs * (offtake_pct / 100.0)
    transferred = min(requested, canal_capacity_cusecs)
    remaining_in_river = source_flow_cusecs - transferred
    return {
        "requested_cusecs": round(requested, 1),
        "transferred_cusecs": round(transferred, 1),
        "remaining_in_source_river_cusecs": round(remaining_in_river, 1),
        "capacity_limited": requested > canal_capacity_cusecs,
    }
