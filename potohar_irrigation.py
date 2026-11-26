"""
potohar_irrigation.py
Section: Potohar small dams, irrigation water budget (CWR / NIR / GIR), field-flooding
and soil-test guidance by region, and CHIRPS rainfall data.

All figures were supplied by the project owner as design / reference material and are
indicative only - verify against Punjab Irrigation Department, Small Dams Organization,
PARC and PMD sources before formal use.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

NOTE = ("Reference material supplied by the project owner. Figures are indicative design "
        "values - verify against Punjab Irrigation Department, Small Dams Organization (SDO), "
        "PARC and PMD records before using in formal reports.")

# ---------------------------------------------------------------- 1. worked example
EXAMPLE_ROWS = [
    ("Irrigated area (CCA x intensity)", "600 acres", "400 acres"),
    ("Duty  D = 1.98 x B / Δ", "190.1 acres/cusec", "132.0 acres/cusec"),
    ("Required discharge  Q = Area / D", "3.16 cusecs", "3.03 cusecs"),
    ("Net crop water volume (Area x Δ)", "750 acre-feet", "600 acre-feet"),
]

# ---------------------------------------------------------------- 2. CCA data
DISTRICT_SUMMARY = [
    ("Attock", "15 completed small dams", "18,629 acres", "45,401 AF live storage"),
    ("Rawalpindi & ICT", "10 completed small dams", "9,108 acres",
     "59,745 AF combined storage (heavily weighted to municipal drinking water)"),
    ("Mianwali", "Mianwali Canal Division (Thal Canal / Dullewala system fed via Jinnah Barrage) "
                 "plus localized hill-torrent dams", "434,000 acres (4.34 lac) CCA of 504,000 acres GCA",
     "n/a"),
]

DAMS = [
    ("Channi Bor Dam", "Attock (Fateh Jang)", 1173, "1,500", "Operational small dam"),
    ("Shahpur Dam", "Attock (Fateh Jang)", 14285, "~3,500-4,000", "Major Attock storage dam"),
    ("Kanjoor Dam", "Attock", 2835, "~1,100", "Completed 1975"),
    ("Jawa Dam", "Rawalpindi", 900, "800", "80,032 acres GCA (as supplied)"),
    ("Rawal Dam", "Rawalpindi / ICT", 37500, "500", "Primarily urban water supply (23 MGD)"),
    ("Misriot Dam", "Rawalpindi", 241, "100", "Oldest Potohar small dam (1963)"),
    ("Namal Dam (Lake)", "Mianwali", 14460, "~3,000-4,000", "Built 1913; feeds Namal Canal toward Mianwali (avg storage)"),
]


# ---------------------------------------------------------------- 2b. Punjab dams / command-area formulas (supplied)
JHELUM_DAMS = [
    ("Tainpura Dam I", "6,986 (I+II)", "34.0", "3,410"),
    ("Domeli Dam", "3,735", "30.0", "3,000"),
    ("Lehri (Baral) Dam", "-", "-", "2,200"),
    ("Gurha Utam Singh Dam", "-", "12.25", "1,500"),
    ("Jammergal Dam", "930", "7.25", "660"),
    ("Garat Dam", "1,763", "-", "638"),
    ("Shah Habib Dam", "-", "3.0", "450"),
    ("Fatehpur Dam", "441", "3.0", "314"),
]
JHELUM_COLS = ["Dam", "Live storage (AF)", "Channel capacity (cusecs)", "CCA (acres)"]

# ---------------------------------------------------------------- 3. CWR / NIR / GIR
CWR_TABLE = [
    ("CWR", "Crop Water Requirement",
     "Total depth of water a crop needs to grow optimally without stress (evaporation + transpiration).",
     "CWR = ETc = Kc × ET0"),
    ("NIR", "Net Irrigation Requirement",
     "Part of CWR that must come from irrigation after effective rainfall and soil moisture.",
     "NIR = CWR − Peff − ΔS"),
    ("GIR", "Gross Irrigation Requirement",
     "Total water to release from the dam outlet, after field-application and canal-conveyance losses.",
     "GIR = NIR / (Ea × Ec)"),
]

CWR_TERMS = [
    "**ET0 and Kc:** reference evapotranspiration (ET0) multiplied by the crop coefficient (Kc).",
    "**Peff and ΔS:** effective rainfall absorbed by the root zone, and usable stored soil moisture.",
    "**Ea and Ec:** field application efficiency (typically 60-75% for surface irrigation) and canal "
    "conveyance efficiency (typically 75-90% depending on canal lining).",
]

# ---------------------------------------------------------------- 4. water budget (1,000-acre Potohar dam)
# (season, crop, % of CCA, area acres, CWR mm, Peff mm, NIR mm, GIR mm, GIR ft, release AF)
BUDGET = [
    ("Rabi (Nov-Apr)", "Wheat", 50, 500, 415, 75, 340, 472, 1.55, 774.6),
    ("Rabi (Nov-Apr)", "Gram / Pulses", 15, 150, 250, 65, 185, 257, 0.84, 126.4),
    ("Rabi (Nov-Apr)", "Mustard / Canola", 10, 100, 290, 65, 225, 313, 1.03, 102.5),
    ("Rabi (Nov-Apr)", "Berseem (Fodder)", 5, 50, 700, 95, 605, 840, 2.76, 137.8),
    ("Kharif (May-Oct)", "Maize", 25, 250, 500, 215, 285, 396, 1.30, 324.7),
    ("Kharif (May-Oct)", "Groundnut", 20, 200, 485, 300, 185, 257, 0.84, 168.6),
    ("Kharif (May-Oct)", "Sorghum / Millet", 15, 150, 385, 210, 175, 243, 0.80, 119.6),
    ("Perennial (year-round)", "Citrus / Olive orchards", 5, 50, 1125, 300, 825, 1146, 3.76, 188.0),
]
BUDGET_COLS = ["Season", "Crop", "% of CCA", "Area (acres)", "CWR (mm)", "Peff (mm)",
               "NIR (mm)", "GIR (mm)", "GIR (ft)", "Dam release (AF)"]

SYSTEM_SCENARIOS = [
    ("Unlined earth channels", 60, 2331, "+389 AF extra storage needed"),
    ("Lined canals & watercourses (baseline)", 72, 1942, "Baseline"),
    ("Drip / sprinkler", 85, 1645, "Saves 297 AF/yr; can extend the CCA by ~180 acres with the same dam"),
]

# ---------------------------------------------------------------- 5. flooding / salinity
FLOOD_REGIONS = [
    ("Punjab (Upper Indus Basin)", "Basmati & coarse rice (Kallar tract)",
     "Very high: continuous flooding of paddy in hot monsoon summers drives heavy methane output.",
     "Moderate-to-high: canal seepage and flood irrigation cause localized waterlogging; heavy pumping of "
     "brackish groundwater induces secondary salinization.",
     "Alternate Wetting and Drying (AWD) and laser land levelling cut methane ~30-40% and protect groundwater."),
    ("Sindh (Lower Indus Basin)", "IRRI rice, sugarcane",
     "High: prolonged standing water in flat, poorly drained alluvial plains sustains anaerobic conditions.",
     "Severe: flat topography, unlined canals and poor natural drainage raise water tables and cause "
     "capillary salt build-up under extreme heat.",
     "Subsurface tile drainage, bio-drainage (e.g. Eucalyptus), and controlled leaching only where drainage "
     "outlets (LBOD/RBOD) exist."),
    ("Khyber Pakhtunkhwa", "Rice (Swat, Dir, D.I. Khan)",
     "Moderate: cooler northern valleys slow methane production; D.I. Khan remains high.",
     "Low-to-moderate: sloped northern terrain drains naturally; D.I. Khan's canal plains face waterlogging "
     "and sodicity.",
     "Intermittent irrigation in southern plains (D.I. Khan) and gypsum against soil sodicity."),
    ("Balochistan", "Rice (Nasirabad, Jaffarabad)",
     "High (localized): concentrated in Pat Feeder and Kirthar canal commands in summer heat.",
     "High: heavy clay restricts downward movement; standing water evaporates and leaves dense surface salt "
     "crusts.",
     "Raised-bed planting and gypsum to improve clay infiltration before applying leaching water."),
]

FLOOD_TAKEAWAYS = [
    "**Drainage bottleneck in Sindh & Balochistan:** flooding to flush salts only works if the salty water "
    "has an exit. On the flat Lower Indus Basin, un-drained floodwater raises the water table and turns "
    "temporary flooding into permanent waterlogging and salinity (Thur).",
    "**Groundwater quality in Punjab:** in the rice-wheat zone farmers supplement canal water with tube wells. "
    "Flooding with marginally brackish tube-well water deposits dissolved salts in the topsoil and reduces "
    "the following winter wheat yield.",
    "**Methane reduction:** AWD (letting paddy water subside 15 cm below the soil surface before re-irrigating) "
    "is promoted by PARC and provincial extension departments - it cuts methane, saves 15-30% irrigation "
    "water and strengthens rice roots against lodging.",
]

DOAB_COLS = ["Doab & geography", "Normal soil (ECe < 4, pH < 8.5, SAR < 13)",
             "Saline soil / White Thur (ECe > 4, pH < 8.5, SAR < 13)",
             "Sodic / saline-sodic / Black Kallar (pH > 8.5, SAR > 13)"]
DOAB = [
    ("Bari Doab (Ravi-Sutlej): hot, arid south; severe groundwater depletion in upper parts; brackish water in lower parts.",
     "Avoid continuous flooding: use AWD in rice (Kasur/Okara) and raised-bed planting in cotton/maize "
     "(Sahiwal/Multan) to cut methane and save declining groundwater.",
     "Targeted canal leaching: laser-level the field and apply heavy pre-sowing flood irrigation (Rauni) with "
     "fresh canal water only. Do not leach with local brackish tube wells.",
     "Gypsum + deep chiseling: broadcast gypsum per soil test, chisel-plow dense hardpans, then 2-3 controlled "
     "canal floodings to flush displaced sodium."),
    ("Rachna Doab (Ravi-Chenab): core rice-wheat belt; dense canal network mixed with heavy tube-well pumping.",
     "Safe AWD (15 cm rule): install a perforated Pani Pipe; re-irrigate paddy only when water subsides 15 cm "
     "below the surface. Cuts methane 30-40% without yield loss.",
     "Pre-monsoon flushing: flood with canal water before monsoon so rain pushes soluble salts below the 1.5 m "
     "root zone.",
     "Gypsum + rice-wheat rotation: apply gypsum before transplanting rice; roots of flooded paddy under "
     "intermittent drainage help open pores to leach sodium."),
    ("Chaj Doab (Chenab-Jhelum): high canal seepage (Upper/Lower Jhelum); prone to shallow water tables and waterlogging.",
     "Strict intermittent irrigation: never hold deep standing water; shallow water tables mean continuous "
     "flooding quickly causes waterlogging and methane spikes.",
     "Drainage first, leaching second: do not flood to leach if the water table is within 1.5 m. Clear surface "
     "drains or use bio-drainage (Eucalyptus) first.",
     "Gypsum + raised beds: apply gypsum to restore permeability, then plant on raised beds so roots stay "
     "above the wet, oxygen-deprived zone."),
    ("Sindh Sagar Doab (Jhelum-Indus / Thal): arid, sandy to sandy-loam; canal-irrigated pockets (Thal Canal) vs desert.",
     "No flood irrigation: sandy soils drain too fast, wasting water and nutrients. Use sprinkler, drip or "
     "small-basin irrigation.",
     "Light, frequent flushing: sandy soils hold few salts, so large flood volumes are unnecessary; light canal "
     "irrigations wash salts past the root zone.",
     "Organic matter + gypsum: low clay limits sodium lock-up, but sodic patches need gypsum with farmyard "
     "manure (FYM) or green manure (Jantar)."),
]

DOAB_RULES = [
    "**Check tube-well water before flooding:** across all Doabs, flooding with poor-quality groundwater "
    "(ECw > 1.5 dS/m or RSC > 2.5 meq/L) creates secondary salinity faster than canal water can wash it away. "
    "Mix marginal tube-well water with canal water, or add gypsum to the irrigation channel (stone gypsum).",
    "**Mid-season drainage for methane:** in rice areas of Rachna, Bari and Chaj Doabs, drain standing water for "
    "5-7 days at maximum tillering (about 35-40 days after transplanting). This oxidizes the soil, cuts "
    "seasonal methane by up to 40-50% and prevents root rot.",
]

# (zone, districts, action plan bullets)
ZONES = [
    ("1. Punjab - Upper & Central Doab (rice-wheat & mixed cropping)",
     ["**Rachna Doab:** Sialkot, Narowal, Gujranwala, Wazirabad, Hafizabad, Sheikhupura, Nankana Sahib, Faisalabad, "
      "Chiniot, Toba Tek Singh, Jhang.",
      "**Bari Doab:** Lahore, Kasur, Okara, Pakpattan, Sahiwal, Khanewal, Vehari, Multan, Lodhran.",
      "**Chaj Doab:** Gujrat, Mandi Bahauddin, Sargodha, Khushab (riverine belt)."],
     ["**Normal (ECe < 4, pH < 8.5):** replace continuous flooding with AWD using a 15 cm Pani Pipe to cut methane "
      "30-40% and prevent shallow water tables (especially Mandi Bahauddin, Hafizabad, Gujrat).",
      "**Saline (ECe > 4, pH < 8.5):** heavy pre-sowing canal irrigation (Rauni) after laser levelling. Never leach "
      "with brackish tube-well water (ECw > 1.5 dS/m).",
      "**Sodic / Black Kallar (pH > 8.5, SAR > 13):** gypsum per soil test, chisel-plow hardpans, 2-3 controlled "
      "canal floodings."]),
    ("2. Punjab - Arid, Sandy & Pothohar",
     ["**Sindh Sagar Doab (Thal):** Bhakkar, Layyah, Mianwali, Muzaffargarh, Kot Addu, Khushab (arid zone).",
      "**Cholistan / southern irrigated:** Bahawalpur, Bahawalnagar, Rahim Yar Khan.",
      "**Pothohar rainfed (barani):** Rawalpindi, Attock, Chakwal, Talagang, Jhelum, Murree."],
     ["**Thal & Cholistan:** avoid heavy flooding on sandy soils (wastes water, deep percolation). Use sprinkler, drip or "
      "small basins. In canal-irrigated Rahim Yar Khan and Bahawalnagar, use gypsum + canal leaching on dense sodic patches.",
      "**Pothohar (barani):** fields are rainfed and sloped; waterlogging and methane are minimal. Focus on check dams, "
      "contour bunding and gypsum for moisture retention, not flood leaching."]),
    ("3. Sindh - Left & Right Bank Indus (flat alluvial plains)",
     ["**Right bank (rice belt):** Jacobabad, Kashmore, Shikarpur, Larkana, Qambar Shahdadkot, Dadu, Jamshoro.",
      "**Left bank & lower delta:** Ghotki, Sukkur, Khairpur, Naushahro Feroze, Shaheed Benazirabad, Sanghar, Mirpurkhas, "
      "Umerkot, Tharparkar (irrigated edge), Matiari, Tando Allahyar, Tando Muhammad Khan, Hyderabad, Badin, Sujawal, Thatta.",
      "**Urban / coastal:** Karachi (Malir / Gadap agricultural pockets)."],
     ["**Critical constraint:** Sindh is very flat with a high water table. Do not flood to leach salts unless a working "
      "drainage outlet (LBOD/RBOD or tile drain) exists - otherwise flooding worsens waterlogging and pulls salts up.",
      "**Normal (ECe < 4):** intermittent drying in Larkana, Qambar Shahdadkot and Badin paddy to cut methane and keep roots oxygenated.",
      "**Saline / waterlogged (ECe > 4, high water table):** install subsurface tile drainage or bio-drainage belts "
      "(Eucalyptus) first; raised beds for cotton/vegetables.",
      "**Sodic (pH > 8.5, SAR > 13):** gypsum + organic matter (Jantar green manure) before controlled flushing into surface drains."]),
    ("4. Khyber Pakhtunkhwa - irrigated plains vs mountain valleys",
     ["**Southern & central canal plains:** Dera Ismail Khan, Tank, Bannu, Lakki Marwat, Peshawar, Charsadda, Mardan, "
      "Nowshera, Swabi, Kohat, Karak, Hangu.",
      "**Northern valleys & merged districts:** Swat, Dir (Upper/Lower), Malakand, Buner, Shangla, Chitral, Mansehra, "
      "Abbottabad, Haripur, Battagram, Kohistan, Torghar, Bajaur, Mohmand, Khyber, Orakzai, Kurram, North & South Waziristan."],
     ["**D.I. Khan & Chashma Right Bank (CRBC):** heavy canal seepage causes severe waterlogging and sodicity. Avoid "
      "continuous flooding; combine gypsum, surface drains and intermittent irrigation.",
      "**Peshawar-Mardan valley:** high water tables near Kabul/Swat rivers - raised beds for maize/sugarcane and periodic drainage.",
      "**Northern mountain districts (Swat, Dir, Mansehra):** cool temperatures suppress methane and terraces drain naturally. "
      "Avoid over-flooding terraces to prevent erosion and nutrient runoff."]),
    ("5. Balochistan - canal plains vs karez / upland basins",
     ["**Nasirabad Division (canal rice/wheat):** Nasirabad, Jaffarabad, Sohbatpur, Jhal Magsi, Kachhi (Bolan), Usta Muhammad.",
      "**Upland & coastal:** Quetta, Pishin, Killa Abdullah, Chaman, Zhob, Loralai, Sibi, Barkhan, Musakhel, Sherani, Kohlu, "
      "Dera Bugti, Ziarat, Harnai, Kalat, Mastung, Khuzdar, Awaran, Washuk, Kharan, Chagai, Nushki, Panjgur, Kech (Turbat), "
      "Gwadar, Lasbela, Hub."],
     ["**Nasirabad & Jaffarabad (Pat Feeder / Kirthar canals):** heavy impermeable clay traps standing water, causing "
      "evaporation, salt crusting and methane spikes. Gypsum + deep tillage before leaching; raised beds for non-rice crops.",
      "**Upland valleys & coast:** water scarcity is extreme - never flood. Drip/bubbler irrigation in orchards "
      "(Quetta, Pishin, Ziarat) and spate (Sailaba) bunds in Khuzdar, Lasbela and Kachhi."]),
    ("6. Gilgit-Baltistan & Azad Jammu & Kashmir",
     ["**GB:** Gilgit, Skardu, Hunza, Nagar, Ghizer, Diamer, Astore, Ghanche, Shigar, Kharmang.",
      "**AJK:** Muzaffarabad, Neelum, Jhelum Valley (Hattian), Bagh, Haveli, Poonch, Sudhnoti, Kotli, Mirpur, Bhimber."],
     ["**Strategy:** steep terrain and cold climate keep methane negligible and prevent waterlogging, except in flat valley "
      "bottoms (Bhimber, Mirpur in southern AJK, or glacial riverbeds in Skardu/Gilgit).",
      "**Action:** in Bhimber and Mirpur apply AWD and laser levelling on canal-irrigated fields. On mountain terraces use "
      "lined channels (Kuhls) and light, frequent irrigation to prevent erosion and nutrient leaching."]),
]

# ---------------------------------------------------------------- 6. CHIRPS
CHIRPS_INTRO = (
    "CHIRPS (Climate Hazards Group InfraRed Precipitation with Stations) is a quasi-global gridded rainfall dataset "
    "(0.05° resolution, 1981 to near-present) blending satellite infrared imagery, terrain precipitation models and "
    "rain-gauge observations. In Pakistan it is widely used for drought monitoring, hydrological modelling and rainfall "
    "anomaly tracking in gauge-sparse areas."
)
CHIRPS_POINTS = [
    "**Coverage:** 50°S-50°N at ~5 km (0.05°) from 1981 onward. CHIRPS v2 (active through December 2026) and CHIRPS v3 "
    "are available from the Climate Hazards Center.",
    "**Accuracy by terrain & season:** against surface gauges, monthly/seasonal correlation is strong (often CC > 0.70), "
    "capturing monsoon peaks in north-eastern Pakistan. It does better in low and medium elevations and plains (such as "
    "Sindh) and has larger biases in complex high-elevation northern terrain.",
    "**Mid-2000s inhomogeneity caveat:** research on CHIRPS v2.0 over Pakistan (Junaid & Sajid, 2026) found an abrupt "
    "upward shift around 2002-2006 (peaking near 2005) in wet-day totals and counts that is absent from gauge-only "
    "datasets. Check trends and dry-spell calculations for homogeneity; CHIRPS v3.0 shows a much smaller step.",
]
CHIRPS_WORKFLOWS = [
    "**Subnational indicators:** pre-computed 10-day, 1-month and 3-month totals, climatological averages and anomalies "
    "for Pakistan's administrative units are published on the Humanitarian Data Exchange (HDX) from CHIRPS v2 and CHIRPS-GEFS forecasts.",
    "**Cloud analysis:** daily grids can be queried in Google Earth Engine for regional anomaly and drought assessments.",
]
CHIRPS_REGIONS = [
    ("Lower Indus Basin & Sindh",
     "High accuracy (R ≈ 0.87, index of agreement d ≈ 0.93 against ground gauges).",
     "Reliable substitute for sparse rain gauges; captures the south-east to north-west coastal rainfall gradient well."),
    ("Punjab & sub-montane zones (e.g. Soan Basin)",
     "Strong monthly/seasonal skill (CC > 0.70); captures summer monsoon peaks in north-eastern Punjab.",
     "Good for agricultural drought monitoring and watershed runoff modelling; daily extremes may be slightly smoothed."),
    ("Balochistan",
     "Moderate-to-good skill in arid plains; localized bias near rugged ranges.",
     "Valuable given extreme station sparsity; use at dekadal (10-day) or monthly scale, not single-day storm totals."),
    ("Upper Indus Basin & Gilgit-Baltistan",
     "Lower skill; tends to overestimate precipitation in high mountains and underperforms in winter westerly snowfall.",
     "Do not use raw CHIRPS alone for high-altitude snowmelt/glacier runoff; apply elevation-dependent bias correction or pair with gauge/reanalysis data."),
]
CHIRPS_GOALS = [
    "**Drought & anomaly monitoring:** use dekadal, 1-month and 3-month aggregations; Standardized Precipitation Index (SPI) "
    "and percent-of-normal anomalies. Administrative-level tables are updated regularly on HDX.",
    "**Long-term trends (1981-present):** switch to CHIRPS v3 (v2 production ends after December 2026, and v2 has the artificial "
    "2002-2006 step that can inflate positive trends). Use Mann-Kendall (MK) or Modified Mann-Kendall (MMK) tests for serial correlation.",
    "**Hydrological modelling (SWAT, HEC-HMS):** CHIRPS drives monthly streamflow reliably in low and mid-elevation basins such as "
    "the Soan. For daily flood routing, bias-correct against Pakistan Meteorological Department (PMD) gauges with quantile mapping first. "
    "CHIRPS v3 includes gauge-undercatch corrections - account for this when benchmarking against raw PMD records in windy or high-altitude areas.",
]
SOURCES = [
    ("CHIRPS validation in Pakistan (Hydrological Sciences Journal)", "https://www.tandfonline.com/doi/full/10.1080/02626667.2021.1957476"),
    ("Climate Hazards Center - CHIRPS", "https://www.chc.ucsb.edu/data/chirps"),
    ("Google Earth Engine - CHIRPS Daily", "https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY"),
    ("CHIRPS over Pakistan (ScienceDirect, Atmospheric Research)", "https://www.sciencedirect.com/science/article/abs/pii/S0169809520312266"),
    ("HDX - Pakistan subnational rainfall indicators", "https://data.humdata.org/dataset/pak-rainfall-subnational"),
    ("Validation of CHIRPS over Pakistan (ResearchGate)", "https://www.researchgate.net/publication/348555964_Validation_of_CHIRPS_satellite-based_precipitation_dataset_over_Pakistan"),
    ("CHIRPS v3 (NCAR Climate Data Guide)", "https://climatedataguide.ucar.edu/climate-data/chirps-climate-hazards-infrared-precipitation-station-data-version-3"),
    ("Junaid & Sajid (2026) - CHIRPS v2.0 inhomogeneity (SSRN)", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7583884"),
]


# =============================================================================
def design_example(cca, rabi_pct, kharif_pct, b_r, d_r_in, b_k, d_k_in, eff):
    """Duty / discharge / volume / live storage for the worked canal-design example."""
    out = {}
    for name, pct, b, d_in in (("Rabi", rabi_pct, b_r, d_r_in), ("Kharif", kharif_pct, b_k, d_k_in)):
        area = cca * pct / 100.0
        delta_ft = d_in / 12.0
        duty = 1.98 * b / delta_ft if delta_ft else 0.0
        q = area / duty if duty else 0.0
        vol = area * delta_ft
        out[name] = {"area": area, "duty": duty, "q": q, "vol": vol}
    peak = max(out["Rabi"]["q"], out["Kharif"]["q"])
    net = out["Rabi"]["vol"] + out["Kharif"]["vol"]
    storage = net / (eff / 100.0) if eff else 0.0
    return out, peak, net, storage


def gir_calc(cwr_mm, peff_mm, ds_mm, ea, ec):
    nir = max(cwr_mm - peff_mm - ds_mm, 0.0)
    gir = nir / (ea * ec) if ea * ec else 0.0
    return nir, gir


def render():
    st.title("💧 Potohar Small Dams, Irrigation Water Budget & Field-Flooding Guide")
    st.caption(NOTE)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "1. Canal Discharge & Storage", "2. CCA Data (Rawalpindi · Attock · Mianwali)",
        "3. CWR · NIR · GIR", "4. 1,000-Acre Water Budget",
        "5. Field Flooding & Soil Tests", "6. CHIRPS Rainfall Data",
    ])

    # ---- 1
    with t1:
        st.subheader("Worked calculation: canal discharge & storage requirement")
        st.markdown(
            "To design a dam outlet and reservoir for a **1,000-acre CCA** in Punjab's barani belt, engineers compute the "
            "peak seasonal discharge **Q** and the total live storage volume (acre-feet, AF).\n\n"
            "**Assumptions:** 60% Rabi (wheat) + 40% Kharif (maize/fodder) = 100% annual intensity.  \n"
            "**Wheat (Rabi):** base period B = 120 days, delta Δ = 15 in (1.25 ft).  \n"
            "**Maize (Kharif):** B = 100 days, Δ = 18 in (1.50 ft)."
        )
        st.dataframe(pd.DataFrame(EXAMPLE_ROWS, columns=["Parameter", "Rabi (wheat)", "Kharif (maize)"]),
                     use_container_width=True, hide_index=True)
        st.markdown(
            "**Final design outputs**\n"
            "- **Design canal capacity:** governed by peak seasonal demand, **3.16 cusecs** (rounded up to 3.5-4.0 cusecs at the "
            "head regulator for seepage losses).\n"
            "- **Net annual water requirement:** 750 + 600 = **1,350 AF**.\n"
            "- **Required live storage:** 1,350 / 0.70 (typical overall conveyance & field efficiency) ≈ **1,930 AF**.\n\n"
            "_To scale for another CCA, multiply discharge and storage proportionally (a 2,500-acre CCA needs 2.5× the capacity)._"
        )
        st.markdown("---")
        st.subheader("🧮 Try your own CCA")
        c1, c2, c3, c4 = st.columns(4)
        cca = c1.number_input("CCA (acres)", 50.0, 500000.0, 1000.0, 50.0, key="pi_cca")
        rp = c2.slider("Rabi intensity (%)", 0, 100, 60, key="pi_rp")
        kp = c3.slider("Kharif intensity (%)", 0, 100, 40, key="pi_kp")
        eff = c4.slider("Overall efficiency (%)", 30, 95, 70, key="pi_eff")
        d1, d2, d3, d4 = st.columns(4)
        b_r = d1.number_input("Rabi base period B (days)", 30, 250, 120, key="pi_br")
        dl_r = d2.number_input("Rabi delta Δ (inches)", 3.0, 60.0, 15.0, 0.5, key="pi_dr")
        b_k = d3.number_input("Kharif base period B (days)", 30, 250, 100, key="pi_bk")
        dl_k = d4.number_input("Kharif delta Δ (inches)", 3.0, 60.0, 18.0, 0.5, key="pi_dk")
        res, peak, net, storage = design_example(cca, rp, kp, b_r, dl_r, b_k, dl_k, eff)
        rows = [{"Season": s, "Area (acres)": round(v["area"], 1), "Duty (acres/cusec)": round(v["duty"], 1),
                 "Q (cusecs)": round(v["q"], 2), "Net volume (AF)": round(v["vol"], 1)} for s, v in res.items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Peak design discharge", f"{peak:.2f} cusecs")
        m2.metric("Net annual water", f"{net:,.0f} AF")
        m3.metric("Required live storage", f"{storage:,.0f} AF")
        st.caption("Duty D = 1.98 × B / Δ (Δ in feet); Q = Area / D; storage = net volume / efficiency. "
                   "Add seepage allowance at the head regulator (the example rounds up from 3.16 to 3.5-4.0 cusecs).")

        st.markdown("---")
        st.subheader("CCA formulas & engineering calculations")
        st.markdown(
            "Command areas are broken into three tiers, which are then used to size canal capacity and dam storage:\n"
            "- **Gross Command Area (GCA):** total land bounded by the dam's irrigation network, including villages, roads, ponds and barren land.\n"
            "- **Culturable Command Area (CCA):** the part of the GCA physically fit for farming.\n"
            "- **Net Command Area (NCA):** the exact farmed field area after subtracting internal field channels and bunds."
        )
        st.latex(r"\text{CCA}=\text{GCA}-\text{Uncultivable area (barren land, forests, habitats, roads)}")
        st.latex(r"\text{NCA}=\text{CCA}-\text{Area occupied by canals, ditches and bunds}")
        st.markdown("**Key water & irrigation formulas** (used once the CCA is established):")
        st.markdown("1. **Annual intensity of irrigation (I)** - how much of the CCA is irrigated across Rabi and Kharif (often above 100% if double-cropped):")
        st.latex(r"I=\left(\frac{\text{Total area irrigated in a year}}{\text{CCA}}\right)\times 100\%")
        st.markdown("2. **Delta (Δ) and Duty (D):** Δ is the total depth of water a crop needs over its base period B (days); D is the area "
                    "1 cusec (or 1 cumec) of continuous water can irrigate.")
        st.latex(r"D=\frac{864\,B}{\Delta}\quad(\text{hectares/cumec, }\Delta\text{ in cm})")
        st.markdown("In Pakistani FPS units: D ≈ 1.98 × B / Δ, with D in acres/cusec and Δ in feet.")
        st.markdown("3. **Design outlet discharge (Q)** - how much water the dam must release into the main channel:")
        st.latex(r"Q\,(\text{cusecs})=\frac{\text{Area to be irrigated (acres)}}{\text{Duty (acres/cusec)}}")
        st.markdown("4. **Water allowance (Punjab standard)** - canals are often designed on a fixed allowance of cusecs per 1,000 acres of CCA: "
                    "typically **3.0-3.6 cusecs per 1,000 acres** for perennial systems and **5.5+ cusecs** for non-perennial / barani systems.")

    # ---- 2
    with t2:
        st.subheader("CCA data: Rawalpindi, Attock & Mianwali districts")
        st.caption("Per Punjab Irrigation Department Potohar Irrigation Zone records and Small Dams Organization data (as supplied).")
        st.markdown("**District-wide summary**")
        st.dataframe(pd.DataFrame(DISTRICT_SUMMARY, columns=["District", "Scheme", "Combined CCA", "Storage"]),
                     use_container_width=True, hide_index=True)
        st.markdown("**Individual dam CCA figures**")
        dams = pd.DataFrame(DAMS, columns=["Dam", "District", "Live storage (AF)", "CCA (acres)", "Notes"])
        st.dataframe(dams, use_container_width=True, hide_index=True)
        fig = px.bar(dams, x="Dam", y="Live storage (AF)", color="District",
                     title="Live storage by dam (acre-feet)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Under Punjab's 2025-2026 barani development initiatives, 1,500+ private/subsidized mini dams — each holding up to "
                   "100 AF and irrigating 15-50 acres — have also been built across Attock, Rawalpindi and Mianwali.")
        st.info("Storage and CCA values are quoted as supplied (several are approximate, e.g. “~3,500-4,000”). Verify against SDO/PID records.")

        st.markdown("---")
        st.subheader("CCA of dams in Punjab")
        st.markdown(
            "According to the Punjab Irrigation Department, the **Potohar Irrigation Zone** (Jhelum, Chakwal, Rawalpindi and Attock) manages "
            "**57 completed small dams serving a combined CCA of 66,804 acres**, with ongoing projects set to add another **69,800 acres**."
        )
        st.markdown("**District Jhelum small dams** (per the Jhelum district small-dams portal)")
        st.dataframe(pd.DataFrame(JHELUM_DAMS, columns=JHELUM_COLS), use_container_width=True, hide_index=True)
        st.markdown("**Other regional & major systems**")
        st.markdown(
            "- **Chakwal district:** 13 operational small dams (including Khokher Zer, Dhrabi, Surlah, Dhok Talian, Nikka and Walana) serve a combined CCA of **11,089 acres**.\n"
            "- **Large Indus Basin dams (Mangla & Tarbela):** unlike small dams that serve localized command areas directly, they feed the Indus Basin "
            "Irrigation System, which commands roughly **20.78 to 21.71 million acres of CCA** across Punjab via 13 barrages and 25 main canal systems.\n"
            "- **Mini dams (ABAD):** built by the Agency for Barani Areas Development for individual or small-group farms; typically 40-100 AF "
            "and serving localized CCAs of **15 to 50 acres** each."
        )
        st.caption("Sources as supplied: irrigation.punjab.gov.pk, jhelum.punjab.gov.pk/small_dams, chakwal.punjab.gov.pk/small-dams, "
                   "agripunjab.gov.pk/abad-whatwedo, pecongress.org.pk (Paper 806).")

    # ---- 3
    with t3:
        st.subheader("CWR, NIR and GIR")
        st.markdown("In irrigation and dam engineering these are the three sequential steps used to calculate how much water a dam must "
                    "release to meet crop needs.")
        st.dataframe(pd.DataFrame(CWR_TABLE, columns=["Abbreviation", "Full form", "Definition", "Formula"]),
                     use_container_width=True, hide_index=True)
        st.markdown("**Key terms**")
        for t in CWR_TERMS:
            st.markdown(f"- {t}")
        st.markdown("**Quick example (Punjab wheat)**\n"
                    "1. **CWR:** wheat needs 400 mm over the season.\n"
                    "2. **NIR:** minus 80 mm winter (Rabi) rain = 320 mm at the root zone.\n"
                    "3. **GIR:** at 65% overall efficiency (Ea × Ec = 0.65), release 320 / 0.65 ≈ **492 mm** (≈ 1.61 ft) per acre of CCA.")
        st.markdown("---")
        st.subheader("🧮 CWR → NIR → GIR calculator")
        a1, a2, a3 = st.columns(3)
        mode = a1.radio("CWR input", ["Enter CWR (mm)", "Kc × ET0"], key="pi_mode")
        if mode == "Enter CWR (mm)":
            cwr = a2.number_input("CWR (mm)", 0.0, 3000.0, 400.0, 5.0, key="pi_cwr")
        else:
            kc = a2.number_input("Kc", 0.1, 1.5, 0.9, 0.05, key="pi_kc")
            et0 = a3.number_input("ET0 over season (mm)", 0.0, 3000.0, 450.0, 5.0, key="pi_et0")
            cwr = kc * et0
            a2.caption(f"CWR = Kc × ET0 = {cwr:.0f} mm")
        b1, b2, b3, b4, b5 = st.columns(5)
        peff = b1.number_input("Effective rain Peff (mm)", 0.0, 1500.0, 80.0, 5.0, key="pi_peff")
        ds = b2.number_input("Soil moisture ΔS (mm)", 0.0, 500.0, 0.0, 5.0, key="pi_ds")
        ea = b3.slider("Field efficiency Ea (%)", 30, 95, 75, key="pi_ea") / 100
        ec = b4.slider("Conveyance efficiency Ec (%)", 30, 95, 87, key="pi_ec") / 100
        area = b5.number_input("Area (acres)", 1.0, 500000.0, 1000.0, 50.0, key="pi_area")
        nir, gir = gir_calc(cwr, peff, ds, ea, ec)
        gft = gir / 304.8
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("NIR", f"{nir:.0f} mm")
        g2.metric("GIR", f"{gir:.0f} mm", f"{gft:.2f} ft")
        g3.metric("Overall efficiency", f"{ea * ec * 100:.0f}%")
        g4.metric("Dam release", f"{gft * area:,.0f} AF")
        st.caption("1 ft = 304.8 mm; dam release (AF) = GIR (ft) × area (acres).")

    # ---- 4
    with t4:
        st.subheader("Seasonal & annual water budget: representative 1,000-acre Potohar small dam")
        st.markdown(
            "**Baseline:** CCA 1,000 acres; lined main/distributary canals with improved watercourses (Ec = 85%, Ea = 85% → 72% overall, "
            "reflecting modern Small Dams Organization and On-Farm Water Management standards); GIR = NIR / 0.72; 1 ft = 304.8 mm."
        )
        bdf = pd.DataFrame(BUDGET, columns=BUDGET_COLS)
        st.dataframe(bdf, use_container_width=True, hide_index=True)
        rabi = bdf[bdf["Season"].str.startswith("Rabi")]["Dam release (AF)"].sum()
        kharif = bdf[bdf["Season"].str.startswith("Kharif")]["Dam release (AF)"].sum()
        peren = bdf[bdf["Season"].str.startswith("Perennial")]["Dam release (AF)"].sum()
        total = rabi + kharif + peren
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rabi release", f"{rabi:,.1f} AF")
        m2.metric("Kharif release", f"{kharif:,.1f} AF")
        m3.metric("Perennial (orchard)", f"{peren:,.1f} AF")
        m4.metric("Total annual", f"{total:,.1f} AF")
        st.warning(f"Check: the listed crop shares add up to {bdf['% of CCA'].sum()}% of CCA "
                   f"(80% Rabi + 60% Kharif + 5% perennial), while the source text labels the cropping intensity as 150% "
                   f"(1,500 gross acres). Table totals above are computed from the rows.")
        fig = px.bar(bdf, x="Crop", y="Dam release (AF)", color="Season", title="Annual dam release by crop (acre-feet)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "**Key dam & canal sizing outputs**\n"
            "- **Required live storage:** ~1,945 AF, plus ~15-20% dead-storage allowance for Potohar sediment load → total gross reservoir "
            "capacity ~2,300-2,400 AF.\n"
            "- **Seasonal split (orchard shared 50/50):** Rabi 1,235.5 AF (63.6% of annual water, driven by low winter rain); "
            "Kharif 706.9 AF (36.4%, subsidized by July-September monsoon rain).\n"
            "- **Peak canal head discharge:** governed by peak Rabi wheat watering (Feb-Mar, ~28% of seasonal demand) → "
            "**~5.8-6.0 cusecs** at the outlet (≈ 6.0 cusecs per 1,000 acres)."
        )
        st.markdown("**Impact of changing the irrigation system** (same 1,000-acre crop mix)")
        sdf = pd.DataFrame(SYSTEM_SCENARIOS, columns=["System", "Efficiency (%)", "Annual GIR (AF)", "Effect"])
        st.dataframe(sdf, use_container_width=True, hide_index=True)
        st.plotly_chart(px.bar(sdf, x="System", y="Annual GIR (AF)", text="Annual GIR (AF)",
                               title="Annual gross irrigation requirement by system"), use_container_width=True)

    # ---- 5
    with t5:
        st.subheader("Impact of field flooding across Pakistan")
        st.markdown("The impact of flooding varies by climate, soil drainage and water availability. Punjab's rice-wheat belt struggles mainly "
                    "with methane and groundwater depletion; Sindh and Balochistan face waterlogging and salt crusting from poor natural "
                    "drainage and high evaporation.")
        st.dataframe(pd.DataFrame(FLOOD_REGIONS, columns=["Region", "Flooded crops", "Methane (CH₄) impact",
                                                           "Waterlogging & salinity", "Recommended management"]),
                     use_container_width=True, hide_index=True)
        st.markdown("**Key takeaways for the Indus Basin**")
        for t in FLOOD_TAKEAWAYS:
            st.markdown(f"- {t}")
        st.markdown("---")
        st.subheader("Soil-test action plan across Punjab's four Doabs")
        st.dataframe(pd.DataFrame(DOAB, columns=DOAB_COLS), use_container_width=True, hide_index=True)
        st.markdown("**Universal Doab rules for tube-well water & methane control**")
        for t in DOAB_RULES:
            st.markdown(f"- {t}")
        st.markdown("---")
        st.subheader("District guide: six agro-ecological & drainage zones")
        st.caption("Pakistan has over 160 districts, so they are grouped into six zones. Find your district, then match your soil-test "
                   "readings (ECe, pH, SAR) to the strategy.")
        q = st.text_input("🔎 Find a district", key="pi_dq", placeholder="e.g. Sialkot, Larkana, Swat").strip().lower()
        shown = 0
        for title, districts, plan in ZONES:
            if q and not any(q in d.lower() for d in districts):
                continue
            shown += 1
            with st.expander(title, expanded=bool(q)):
                st.markdown("**Districts covered**")
                for d in districts:
                    st.markdown(f"- {d}")
                st.markdown("**Field-flooding & soil-test action plan**")
                for p in plan:
                    st.markdown(f"- {p}")
        if q and not shown:
            st.warning("No district matches. Try a shorter spelling.")

    # ---- 6
    with t6:
        st.subheader("CHIRPS rainfall dataset for Pakistan")
        st.markdown(CHIRPS_INTRO)
        st.markdown("**Key characteristics & performance**")
        for t in CHIRPS_POINTS:
            st.markdown(f"- {t}")
        st.markdown("**Practical datasets & workflows**")
        for t in CHIRPS_WORKFLOWS:
            st.markdown(f"- {t}")
        st.markdown("**Regional & basin performance**")
        st.dataframe(pd.DataFrame(CHIRPS_REGIONS, columns=["Region / basin", "Validation performance", "Operational guidance"]),
                     use_container_width=True, hide_index=True)
        st.markdown("**Guidance by application goal**")
        for t in CHIRPS_GOALS:
            st.markdown(f"- {t}")
        with st.expander("📚 Sources for this tab"):
            for label, url in SOURCES:
                st.markdown(f"- [{label}]({url})")
