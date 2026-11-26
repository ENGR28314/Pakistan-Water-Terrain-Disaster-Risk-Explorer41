"""
irrigation_shortfall.py
Section: Causes of irrigation water shortfall in Pakistan, provincial breakdown, governance /
policy / climate pressures, practical solutions and current government initiatives.

The text and figures were supplied by the project owner as reference material and are
indicative only - verify against WAPDA, IRSA, the Ministry of Water Resources, provincial
Irrigation / Agriculture Departments and the World Bank before formal use.
"""

import pandas as pd
import streamlit as st

NOTE = ("Reference material supplied by the project owner. Figures are indicative and vary by "
        "source (for example conveyance losses are quoted as 'over 60%' in one source and "
        "'50-60%' in another) - verify before using in formal reports.")

SUMMARY = ("Irrigation water shortfall in Pakistan stems from aging infrastructure, inefficient "
           "farming practices, climate variability, limited storage capacity and rising competing "
           "demand. Across the country it is driven by severe conveyance losses, minimal water "
           "storage, climate-driven river fluctuations, groundwater depletion and policy "
           "inefficiencies that affect both major crop seasons.")

KEY_CAUSES = [
    ("Conveyance & field losses",
     "50-60% (some sources: over 60%) of diverted water is lost before reaching crop roots, through "
     "seepage, unlined canals and watercourses, silt build-up, evaporation and traditional flood irrigation."),
    ("Limited storage & siltation",
     "Only about 30 days of carry-over storage (global average 120+ days). Tarbela and Mangla have lost "
     "over 30% of original capacity to sediment, and new major storage dams face prolonged delays."),
    ("Climate change & erratic rainfall",
     "Shifting monsoon patterns, seasonal droughts and accelerated glacial melt disrupt river flows and "
     "seasonal water availability."),
    ("Groundwater over-extraction",
     "Heavy tubewell pumping to offset canal shortages depletes aquifers, degrades water quality and "
     "causes land subsidence in over-extracted zones."),
    ("Water-intensive crops",
     "High-water crops such as sugarcane and rice in water-stressed regions, including parts of Punjab, "
     "strain seasonal supplies."),
    ("Rising demand & governance gaps",
     "Population growth, urbanisation and municipal / industrial needs raise competition for water, while "
     "weak enforcement and inter-provincial distribution disputes complicate management."),
]

STRUCTURAL = [
    ("Aging canal network",
     "Pakistan operates the world's largest contiguous irrigation system (the Indus Basin Irrigation "
     "System), but decades of deferred maintenance have left embankments weak and outlets deteriorated."),
    ("Conveyance & seepage losses",
     "Roughly 50-60% of diverted river water is lost before reaching crop roots (unlined watercourses, "
     "silt build-up, evaporation)."),
    ("Low storage capacity & siltation",
     "About 30 days of supply can be stored, against a global average of 120+ days. Tarbela and Mangla "
     "have lost over 30% of original storage to sediment while new mega-dams face delays."),
]

ON_FARM = [
    ("Flood irrigation",
     "Over 90% of farmland relies on traditional basin flooding instead of high-efficiency systems (drip "
     "or sprinkler), causing massive waterlogging and evaporation."),
    ("Water-intensive cropping patterns",
     "Subsidies and market incentives encourage thirsty cash crops, particularly sugarcane and rice, even "
     "in arid or semi-arid zones."),
    ("Uneven field levelling",
     "Without precision laser land levelling, water pools unevenly and farmers over-irrigate to reach "
     "the higher patches."),
]

SEASONAL = [
    ("Kharif (April-September)",
     "Heavy reliance on glacial melt and monsoon rain creates extreme volatility. Delayed monsoons cause "
     "severe early-season shortages for cotton, rice and sugarcane, while sudden cloudbursts cause "
     "destructive floods that cannot be stored."),
    ("Rabi (October-March)",
     "River flows drop sharply once glacial melt stops. Wheat and winter crops depend heavily on stored "
     "reservoir water, which frequently falls short by 15-35%, forcing farmers onto groundwater."),
]

PROVINCES = [
    ("Punjab", "Groundwater depletion: heavy reliance on pumping (over 1.2 million tubewells) is driving "
               "rapid water-table drops.",
     "Canal shortages: tail-end areas in southern Punjab face recurring irrigation deficits."),
    ("Sindh", "Tail-end vulnerability: lowest end of the Indus system, so highly sensitive to upstream "
              "distribution and conveyance losses.",
     "Water-quality limits: seawater intrusion in the Indus Delta and widespread brackish groundwater "
     "restrict usable supply."),
    ("Khyber Pakhtunkhwa", "Topographic constraints: steep terrain limits large-scale canal expansion.",
     "Weather dependence: agriculture relies heavily on rain-fed (barani) farming and seasonal hill "
     "torrents (rod-kohi)."),
    ("Balochistan", "Aridity and runoff loss: extreme aridity and flash floods cause substantial water "
                    "wastage where check dams are lacking.",
     "Aquifer exhaustion: subsidised electric tubewells accelerate severe groundwater depletion."),
]

GOVERNANCE = [
    ("Underpriced water (abiana)",
     "Extremely low water-tax rates fail to cover canal maintenance costs and give farmers no financial "
     "incentive to conserve water."),
    ("Inter-provincial distribution disputes",
     "Disagreements over the 1991 Water Apportionment Accord and telemetry monitoring complicate fair "
     "sharing between upstream and downstream provinces."),
    ("Population & urban competition",
     "Rapid population growth and industrial expansion divert water from agriculture and push per-capita "
     "availability below the 1,000 cubic metre scarcity threshold."),
]

SOLUTIONS = [
    ("High-efficiency irrigation systems (HEIS)",
     "Replace flood irrigation with drip, sprinkler and subsurface systems; cuts water use by up to 50% "
     "while raising yields."),
    ("Precision laser land levelling",
     "Even grading removes pooling and runoff and reduces water application time by 20-30%."),
    ("Watercourse & canal lining",
     "Concrete or parabolic lining of earthen channels stops seepage before water reaches the farm gate."),
    ("Crop diversification & zoning",
     "Shift from thirsty crops (sugarcane, rice) in arid zones to drought-tolerant, high-value crops "
     "such as pulses, oilseeds and orchards."),
    ("Groundwater regulation & aquifer recharge",
     "Map aquifers, license tubewells in over-exploited zones, and build recharge wells or retention "
     "ponds to refill water tables during monsoon floods."),
    ("Pricing & telemetry reform",
     "Move abiana towards volumetric pricing to fund canal maintenance, with real-time telemetry for "
     "transparent inter-provincial sharing."),
]

FEDERAL = [
    ("Diamer-Bhasha Dam (hydroelectric)",
     "Under construction on the Indus River (target completion around 2029-2030); designed to add 8.1 MAF "
     "of storage and irrigate over 1.2 million additional acres."),
    ("Mohmand Dam",
     "Funded under federal development budgets to add storage, generate hydropower and mitigate flash "
     "floods in Khyber Pakhtunkhwa."),
    ("Indus Basin telemetry & governance",
     "Federal planning focuses on real-time telemetry, satellite water accounting and a national "
     "Groundwater Governance Framework to end provincial distribution disputes."),
]

PROVINCIAL = [
    ("Punjab", "Punjab Resilient and Inclusive Agriculture Transformation (PRIAT)",
     "Funds watercourse lining, 40,000 acres of subsidised HEIS (drip / sprinkler), solarisation of "
     "irrigation systems and 1,700 on-farm storage ponds."),
    ("Punjab", "CM's Program for Water Efficient Agriculture (2025-2028)",
     "Targets lining 1,400 partially improved watercourses and distributing 1,000 laser land-levelling "
     "units to improve tail-end water equity."),
    ("Sindh", "Sindh Water and Agriculture Transformation (SWAT)",
     "World Bank-backed; co-funds watercourse lining (80% grant), on-farm water storage tanks, GIS-based "
     "water monitoring and institutional reforms to modernise water pricing."),
    ("KP & Balochistan", "Small dams & hill-torrent management",
     "Provincial and climate-resilience projects build check dams, delay-action dams and spate "
     "(rod-kohi) irrigation structures to capture flash floods and recharge depleted aquifers."),
]


def _storage_chart():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    labels = ["Pakistan", "Global average"]
    vals = [30, 120]
    bars = ax.barh(labels, vals, color=["#c0562b", "#4a8fd6"])
    ax.bar_label(bars, labels=["~30 days", "120+ days"], padding=4)
    ax.set_xlim(0, 150)
    ax.set_xlabel("Days of water supply that can be stored (indicative)")
    ax.set_title("Carry-over storage capacity", fontsize=11)
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def _two_col(rows, c1, c2):
    return pd.DataFrame(rows, columns=[c1, c2])


def render():
    st.title("🚰 Causes of Irrigation Water Shortfall in Pakistan")
    st.caption(NOTE)
    st.info(SUMMARY)

    t1, t2, t3, t4 = st.tabs([
        "1. Key Causes", "2. Provincial Breakdown", "3. Governance, Policy & Climate",
        "4. Solutions & Government Initiatives",
    ])

    with t1:
        st.subheader("Key causes of irrigation water shortfall")
        st.dataframe(_two_col(KEY_CAUSES, "Cause", "Detail"), use_container_width=True, hide_index=True)
        st.pyplot(_storage_chart(), clear_figure=True)
        st.markdown("#### 1. Structural & infrastructural causes")
        st.dataframe(_two_col(STRUCTURAL, "Cause", "Detail"), use_container_width=True, hide_index=True)
        st.markdown("#### 2. On-farm & agricultural practices")
        st.dataframe(_two_col(ON_FARM, "Practice", "Detail"), use_container_width=True, hide_index=True)
        st.markdown("#### 3. Seasonal dynamics (Kharif vs Rabi)")
        st.dataframe(_two_col(SEASONAL, "Season", "Detail"), use_container_width=True, hide_index=True)

    with t2:
        st.subheader("Primary water-shortfall drivers by province")
        st.dataframe(pd.DataFrame(PROVINCES, columns=["Province", "Driver 1", "Driver 2"]),
                     use_container_width=True, hide_index=True)

    with t3:
        st.subheader("Governance, policy & climate pressures")
        st.dataframe(_two_col(GOVERNANCE, "Pressure", "Detail"), use_container_width=True, hide_index=True)

    with t4:
        st.subheader("Part 1 - Practical & policy solutions")
        st.markdown("Addressing the shortfall requires on-farm water conservation, modern engineering, "
                    "pricing and governance reforms and major storage infrastructure, many of which are "
                    "under way through federal and provincial programmes.")
        st.dataframe(_two_col(SOLUTIONS, "Solution", "What it does"), use_container_width=True,
                     hide_index=True)
        st.subheader("Part 2 - Current government initiatives")
        st.markdown("**Federal mega-storage & telemetry projects**")
        st.dataframe(_two_col(FEDERAL, "Project / initiative", "Detail"), use_container_width=True,
                     hide_index=True)
        st.markdown("**Provincial agricultural & water programmes**")
        st.dataframe(pd.DataFrame(PROVINCIAL, columns=["Province", "Programme", "Focus"]),
                     use_container_width=True, hide_index=True)
