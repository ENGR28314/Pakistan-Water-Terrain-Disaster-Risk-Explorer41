"""
energy_minerals.py
Solar-energy sectors and mining sectors of Pakistan, linked to this dashboard's
water / terrain / disaster-risk themes.

Evidence tags (same convention as army_role.py):
  "Source-backed"     - stated on a page read while compiling this module
  "Reported - verify" - widely reported background or headline-level information;
                        confirm against the linked source before formal use
Coordinates are APPROXIMATE (for orientation on the map only). Capacities,
reserves and ownership change often - treat as indicative, not official.
"""

SB, RV = "Source-backed", "Reported - verify"
SUP = "Supplied reference - verify"

NOTE = (
    "Evidence tags: **Source-backed** = stated on a page read while compiling this page. "
    "**Supplied reference - verify** = text supplied by the project owner (Oct 2026) with its own cited links; not independently checked. "
    "**Reported - verify** = widely reported background / headline-level information — confirm "
    "against the linked source before citing formally. Map coordinates are approximate and "
    "capacities/reserves are indicative, not official."
)

# ------------------------------------------------------------------ SOLAR
SOLAR = {
    "Overview & Market": {
        "points": [
            ("Pakistan's total installed generation capacity was reported around 46,605 MW (2025), with solar contributing more than 25% of electricity production in 2025.", SB),
            ("Roughly 17 GW of solar panels were reported imported in 2024, driving a boom in rooftop/behind-the-meter solar; a Jan 2026 pv-magazine headline put installed PV above 27 GW (estimates differ by source and method).", RV),
            ("Net-metering capacity was reported at ~2,813 MW (Mar 2025) and ~5.3 GW (Apr 2025); another source gave ~4.03 GW — figures conflict, so treat as a range.", SB),
            ("Policy changes since 2024–25 (net-metering buy-back rate revisions, a tax on imported panels) have been widely debated; check current NEPRA/Finance Act notifications.", RV),
        ]},
    "Utility-Scale Solar Parks": {
        "points": [
            ("Quaid-e-Azam Solar Park (Bahawalpur, Punjab, Cholistan edge) — Pakistan's flagship utility-scale PV park; first 100 MW phase commissioned ~2015 with further IPP phases.", SB),
            ("Jhimpir / Thatta–Sindh corridor — mainly wind, with several solar IPPs (e.g. Zorlu-linked projects) reported in the same Sindh grid zone.", RV),
            ("Layyah (Punjab) 1,200 MW solar project — reported as proposed/under development.", SB),
            ("Oracle Power's Thar-region Green Hydrogen Solar Park — reported as a large proposed project (Sindh).", SB),
            ("Sindh Solar Energy Project — provincial programme for solar mini-grids/household systems in off-grid areas.", SB),
        ],
        "table_name": "Utility-scale & large projects",
        "sites": [
            {"Name": "Quaid-e-Azam Solar Park", "Province": "Punjab", "Type": "Utility PV", "Latitude": 29.33, "Longitude": 71.75, "Note": "Bahawalpur; 100 MW first phase (~2015) + IPP phases"},
            {"Name": "Layyah Solar (proposed)", "Province": "Punjab", "Type": "Utility PV", "Latitude": 30.96, "Longitude": 70.94, "Note": "Reported 1,200 MW proposal"},
            {"Name": "Thar Green-Hydrogen Solar Park (proposed)", "Province": "Sindh", "Type": "Solar + H2", "Latitude": 24.75, "Longitude": 70.0, "Note": "Oracle Power proposal; location approximate"},
            {"Name": "Jhimpir–Gharo Corridor", "Province": "Sindh", "Type": "Wind/Solar zone", "Latitude": 25.0, "Longitude": 68.0, "Note": "Grid zone with wind & solar IPPs"},
        ]},
    "Rooftop & Net-Metering": {
        "points": [
            ("Net-metering lets consumers export surplus to the grid (DISCOs), credited against their import; most growth is residential/commercial rooftop.", SB),
            ("Rooftop solar reduces peak daytime grid demand but shifts load to evenings; grid-planning and capacity-payment debates followed in 2025.", RV),
            ("Industrial/captive solar (textile, cement, steel) is growing as an alternative to expensive grid and captive-gas tariffs.", RV),
        ]},
    "Off-Grid, Solar Home Systems & Mini-Grids": {
        "points": [
            ("Large rural/remote populations (Balochistan, Thar, northern valleys) rely on solar home systems, lanterns and mini-grids where the grid is absent.", RV),
            ("Sindh Solar Energy Project and similar provincial/donor programmes target off-grid household solarization.", SB),
            ("Mountain communities (Gilgit-Baltistan, Chitral) also combine micro-hydel with solar for winter/summer balance — links to the Rivers and Mountain Ranges pages.", RV),
        ]},
    "Solar Tube Wells & Agriculture (Water–Energy Nexus)": {
        "points": [
            ("Balochistan: a programme to convert ~29,000 agricultural tube wells from diesel/grid to solar was reported (PV Tech, 2019); Punjab announced tube-well solarization in Feb 2025.", SB),
            ("Solar pumping cuts diesel cost but can accelerate groundwater depletion if unmetered — a key issue for Balochistan and Indus-basin aquifers (see SEBAL ET and Indus Delta pages).", RV),
            ("Solar-powered drip/sprinkler irrigation, cold storage and agro-processing are emerging use cases.", RV),
            ("Army/SIFC-linked 'solar tube well' initiatives are covered on the Pakistan Army's Role page.", RV),
        ]},
    "Floating & Canal-Top Solar": {
        "points": [
            ("Floating PV proposals reported for Tarbela, Mangla, Ghazi Barotha and Khanpur reservoirs (PV Tech, 2019) — would pair with existing hydropower grid connections.", SB),
            ("Canal-top solar (shading canals to cut evaporation and generate power) is discussed regionally; Pakistan pilot/proposals exist but scale is limited — verify current status.", RV),
            ("Water-surface PV reduces evaporation but must be assessed for sediment, drawdown range and flood risk (dam reservoirs fluctuate widely).", RV),
        ]},
    "Hydro–Solar Hybrids & Green Hydrogen": {
        "points": [
            ("Solar complements run-of-river and storage hydropower seasonally (peak flows in summer, low flows in winter) — hybrid dispatch planning is an active topic.", RV),
            ("Green-hydrogen concepts (Thar/Sindh) combine solar/wind with electrolysis; commercial scale is not yet proven in Pakistan.", SB),
            ("Battery storage is rapidly growing alongside rooftop solar as households and businesses hedge against outages and tariffs.", RV),
        ]},
    "Manufacturing, Imports & Supply Chain": {
        "points": [
            ("Pakistan is overwhelmingly an importer of PV modules, mainly from China; local assembly exists but cell/wafer manufacturing is minimal.", RV),
            ("Inverters, batteries and mounting structures are also imported; end-of-life panel/battery recycling is an unresolved issue.", RV),
        ]},
}

# ----------------------------------------------------------------- MINING
MINING = {
    "Overview & Regulation": {
        "points": [
            ("Mining is a provincial subject after the 18th Amendment (provincial mineral departments/ minerals acts); PMDC and provincial development corporations remain major operators.", RV),
            ("Pakistan has large mineral endowments (copper-gold, coal, salt, gypsum, limestone, chromite, marble/granite, gemstones, iron ore) but contributes a small share of GDP.", RV),
            ("Water, security, infrastructure and community consent are the key constraints — mining overlaps the Chagai/Balochistan arid zone and Thar desert (see Deserts and Disaster-Risk pages).", RV),
        ]},
    "Coal (Thar, Lakhra, Balochistan, Punjab, KP)": {
        "points": [
            ("Thar Coalfield (Sindh) holds Pakistan's largest lignite resource; Block II is developed by Sindh Engro Coal Mining Company feeding local power plants.", RV),
            ("Thar mining involves deep open-pit dewatering and brine disposal — a water-management issue linked to local aquifers (Gorano reservoir / Thar Canal discussions).", RV),
            ("Other coalfields: Lakhra and Sonda-Jherruck (Sindh), Duki/Sor Range/Harnai (Balochistan), Salt Range (Punjab) and Hangu/Kohat-Cherat (KP).", RV),
            ("Coal is also used in cement, brick kilns and industry; air quality and occupational safety (Balochistan mine accidents) are persistent concerns.", RV),
        ],
        "sites": [
            {"Name": "Thar Coalfield (Block II)", "Province": "Sindh", "Mineral": "Lignite coal", "Latitude": 24.7, "Longitude": 70.2, "Note": "Sindh Engro Coal Mining Co."},
            {"Name": "Lakhra Coalfield", "Province": "Sindh", "Mineral": "Coal", "Latitude": 25.6, "Longitude": 68.2, "Note": "Near Jamshoro; approximate"},
            {"Name": "Sonda-Jherruck", "Province": "Sindh", "Mineral": "Coal", "Latitude": 24.8, "Longitude": 68.0, "Note": "Approximate"},
            {"Name": "Duki Coalfield", "Province": "Balochistan", "Mineral": "Coal", "Latitude": 30.15, "Longitude": 68.57, "Note": "Approximate"},
            {"Name": "Salt Range / Makerwal", "Province": "Punjab", "Mineral": "Coal", "Latitude": 32.7, "Longitude": 71.6, "Note": "Approximate"},
        ]},
    "Copper, Gold & Rare Metals (Chagai)": {
        "points": [
            ("Reko Diq (Chagai, Balochistan) is one of the world's large copper–gold porphyry deposits; a long-running ownership/arbitration dispute preceded a renewed deal with Barrick Gold, with Pakistani public entities holding a share and the provincial government a stake (check current terms).", RV),
            ("Saindak (Chagai) copper-gold-silver — operated by China's MCC under a long-term lease since 2002.", RV),
            ("Duddar (Lasbela) lead-zinc is operated by a Chinese company under a lease; Chagai arc is also prospective for other metals.", RV),
            ("Reko Diq is located in an extremely arid, water-scarce zone — process water, power and transport (Gwadar/Karachi corridor) are core engineering questions.", RV),
        ],
        "sites": [
            {"Name": "Reko Diq", "Province": "Balochistan", "Mineral": "Copper-gold", "Latitude": 28.88, "Longitude": 62.45, "Note": "Chagai district"},
            {"Name": "Saindak", "Province": "Balochistan", "Mineral": "Copper-gold-silver", "Latitude": 29.13, "Longitude": 61.17, "Note": "MCC lease"},
            {"Name": "Duddar", "Province": "Balochistan", "Mineral": "Lead-zinc", "Latitude": 26.0, "Longitude": 66.6, "Note": "Lasbela; approximate"},
        ]},
    "Salt, Gypsum & Industrial Minerals": {
        "points": [
            ("Khewra Salt Mine (Salt Range, Punjab) is among the world's largest salt mines, operated by PMDC; Warcha, Bahadurkhel and Ghani are other salt mines in the region.", SB),
            ("Gypsum: Salt Range / Dera Ghazi Khan region; Pakistan is a notable producer with domestic cement/fertilizer use and exports.", RV),
            ("Other industrial minerals include fireclay, silica sand, barytes, soapstone/talc, sulphur and magnesite.", RV),
        ],
        "sites": [
            {"Name": "Khewra Salt Mine", "Province": "Punjab", "Mineral": "Rock salt", "Latitude": 32.65, "Longitude": 73.0, "Note": "PMDC"},
            {"Name": "Warcha Salt Mine", "Province": "Punjab", "Mineral": "Rock salt", "Latitude": 32.5, "Longitude": 72.1, "Note": "Approximate"},
            {"Name": "Bahadurkhel Salt Mine", "Province": "KP", "Mineral": "Rock salt", "Latitude": 33.2, "Longitude": 71.0, "Note": "Karak; approximate"},
        ]},
    "Limestone, Cement & Construction Materials": {
        "points": [
            ("Limestone and clay support Pakistan's cement industry (Salt Range/Chakwal, Hattar/Nizampur in KP, Hub/Lasbela, Khairpur).", RV),
            ("Aggregates, sand and gravel are extracted from river beds — a direct link to the Rivers page; unregulated extraction affects bridges, barrages and channel stability.", RV),
        ]},
    "Chromite & Iron Ore": {
        "points": [
            ("Chromite occurs in the Muslim Bagh–Zhob ophiolite belt (Balochistan) and has been mined for decades.", RV),
            ("Iron ore: Chiniot (Punjab) magnetite and Kalabagh/Chitral–Dilband occurrences are reported; development has been limited and has faced delays.", RV),
        ],
        "sites": [
            {"Name": "Muslim Bagh Chromite", "Province": "Balochistan", "Mineral": "Chromite", "Latitude": 30.8, "Longitude": 67.8, "Note": "Approximate"},
            {"Name": "Chiniot Iron Ore", "Province": "Punjab", "Mineral": "Magnetite", "Latitude": 31.7, "Longitude": 72.98, "Note": "Approximate"},
        ]},
    "Marble, Granite & Dimension Stone": {
        "points": [
            ("Marble: Mardan, Buner, Swat, Chitral (KP) and Balochistan (Zhob/Loralai); Pakistan exports onyx and marble mainly to Asia.", RV),
            ("Granite: Nagarparkar (Tharparkar, Sindh) pink/red granite; also Chiniot-area stone.", RV),
            ("Processing waste (slurry) pollutes soils and streams — a recognized environmental issue in KP marble clusters.", RV),
        ],
        "sites": [
            {"Name": "Nagarparkar Granite", "Province": "Sindh", "Mineral": "Granite", "Latitude": 24.35, "Longitude": 70.75, "Note": "Approximate"},
            {"Name": "Buner / Mardan Marble Belt", "Province": "KP", "Mineral": "Marble", "Latitude": 34.4, "Longitude": 72.5, "Note": "Approximate cluster"},
        ]},
    "Gemstones & Specialty Minerals": {
        "points": [
            ("Swat emeralds (Mingora/Shamozai), Hunza and Neelum-area rubies/spinel, Gilgit-Baltistan aquamarine/topaz/tourmaline are notable.", RV),
            ("Antimony (Chitral), copper-tungsten and other specialty minerals are reported in northern ranges; lithium and rare-earth exploration/MOUs were reported in 2025 — verify current status.", RV),
            ("Gemstone mining is largely artisanal/small-scale in remote high-altitude terrain (see Mountain Ranges page).", RV),
        ],
        "sites": [
            {"Name": "Swat Emerald (Mingora)", "Province": "KP", "Mineral": "Emerald", "Latitude": 34.8, "Longitude": 72.4, "Note": "Approximate"},
            {"Name": "Hunza Ruby Belt", "Province": "Gilgit-Baltistan", "Mineral": "Ruby/Spinel", "Latitude": 36.3, "Longitude": 74.7, "Note": "Approximate"},
            {"Name": "Skardu Gem Zone", "Province": "Gilgit-Baltistan", "Mineral": "Aquamarine/Topaz", "Latitude": 35.3, "Longitude": 75.6, "Note": "Approximate"},
        ]},
    "Mining–Water–Disaster Nexus": {
        "points": [
            ("Open-pit dewatering (Thar), tailings dams and acid drainage need engineered management; tailings failure and flash-flood risk apply in northern valleys.", RV),
            ("River-bed mining, quarrying and slope cuts destabilize terrain and amplify landslide/flood impacts (see Disaster Risk Context page).", RV),
            ("Water-scarce Chagai sites require desalination/brackish groundwater strategies and long-distance supply.", RV),
        ]},
}

MINING["Overview & Regulation"]["points"] += [
    ("Supplied: Pakistan sits on the Tethyan metallogenic belt with an estimated $6–8 trillion in mineral wealth, yet mining contributes only ~2–3% of GDP and under 0.1% of global mineral exports.", SUP),
    ("Supplied: 92 known minerals, 52 commercially extracted; world's 2nd-largest rock-salt deposits (Himalayan pink salt, Punjab), massive Thar coal (Sindh), and chromite, iron-ore, copper and gold anomalies.", SUP),
    ("Supplied: the National Mineral Harmonization Framework and the SIFC are used to speed approvals and attract Saudi, US and UAE capital instead of slow local arbitration.", SUP),
]
MINING["Copper, Gold & Rare Metals (Chagai)"]["points"] += [
    ("Supplied: Reko Diq reconstituted as a joint venture — Barrick Gold (Canada) 50%, Pakistani state/provincial entities 50%; multi-billion-dollar foreign financing secured; first production slated late 2028, targeting ~240,000 t copper and ~300,000 oz gold per year.", SUP),
    ("Supplied: Chinese firms have dominated critical-mineral exports; Saindak has operated since 2002 with an active Phase 2 extension.", SUP),
]
MINING["Provincial Ownership Laws & Concessions"] = {
    "points": [
        ("Supplied: after the 18th Amendment, onshore minerals and mines vest in the provinces (Balochistan, Sindh, Punjab, KP), which grant and regulate leases, prospecting licences and concessions.", SUP),
        ("Supplied: the federal government keeps jurisdiction over minerals, oil and gas beyond territorial waters (continental shelf / deep sea).", SUP),
        ("Supplied: Article 172(3) joint 50:50 federal–provincial ownership applies to oil and natural gas; the supplied text extends it to 'specific strategic minerals' — verify that scope against the Constitution before relying on it.", SUP),
        ("Supplied: tension between SIFC-led federal frameworks and provincial autonomy, e.g. pushback on the proposed Khyber Pakhtunkhwa Mines and Minerals Act.", SUP),
    ]}
MINING["Pakistan Minerals Investment Forum (PMIF)"] = {
    "points": [
        ("Supplied: PMIF is the flagship platform to showcase ~$8 trillion mineral potential and an $8 billion mineral-export target.", SUP),
        ("Supplied: PMIF 2026 scheduled 12–13 November 2026, Jinnah Convention Center, Islamabad, under the Petroleum Division and SIFC; 5,000+ investors from 50+ countries expected.", SUP),
        ("Supplied: policy pivot to prohibit export of unrefined raw minerals, requiring investors to build domestic processing, smelting and value-addition plants.", SUP),
        ("Supplied: a Strategic Conference (investment security, sovereign guarantees) and a Technical Conference (new exploration blocks: copper, lithium, rare earths, gemstones).", SUP),
    ]}

DRYFRUIT = {
    "Overview & Production Hubs": {
        "points": [
            ("Supplied: annual production exceeds ~5.3 million tonnes, though a large share is fresh fruit later preserved by traditional drying.", SUP),
            ("Supplied: Balochistan (Quetta, Pishin, Kalat) — almonds, pistachios, raisins; Gilgit-Baltistan (Hunza, Skardu) — apricots, walnuts, pine nuts; KP (Swat, Chitral); Sindh — the largest share of date cultivation.", SUP),
            ("The sector depends strongly on regional climate and irrigation (karez/spring/river water) — see Climatic Regions, Mountain Ranges and Rivers pages.", RV),
        ],
        "sites": [
            {"Name": "Quetta", "Province": "Balochistan", "Product": "Almonds, raisins", "Latitude": 30.18, "Longitude": 66.99, "Note": "Approximate"},
            {"Name": "Pishin", "Province": "Balochistan", "Product": "Almonds, grapes/raisins", "Latitude": 30.58, "Longitude": 66.99, "Note": "Approximate"},
            {"Name": "Kalat", "Province": "Balochistan", "Product": "Almonds, pistachio", "Latitude": 29.03, "Longitude": 66.59, "Note": "Approximate"},
            {"Name": "Hunza", "Province": "Gilgit-Baltistan", "Product": "Apricots, walnuts", "Latitude": 36.32, "Longitude": 74.65, "Note": "Approximate"},
            {"Name": "Skardu", "Province": "Gilgit-Baltistan", "Product": "Apricots, walnuts, pine nuts", "Latitude": 35.3, "Longitude": 75.63, "Note": "Approximate"},
            {"Name": "Swat", "Province": "KP", "Product": "Walnuts, dried fruit", "Latitude": 34.8, "Longitude": 72.4, "Note": "Approximate"},
            {"Name": "Chitral", "Province": "KP", "Product": "Walnuts, dried fruit", "Latitude": 35.85, "Longitude": 71.79, "Note": "Approximate"},
            {"Name": "Khairpur (dates)", "Province": "Sindh", "Product": "Dates", "Latitude": 27.53, "Longitude": 68.76, "Note": "Approximate representative date hub"},
        ]},
    "Exports & Economics": {
        "points": [
            ("Supplied: 2024 dried-fruit exports ~US$5.94 million (to Maldives, UK, USA and others), separate from dates.", SUP),
            ("Supplied: dates exports ~US$53 million, led by Aseel and Dhakki varieties.", SUP),
        ]},
    "Constraints & Post-Harvest Losses": {
        "points": [
            ("Supplied: losses of up to 30–40% from primitive processing — fruit dried on rooftops or open rocks, exposed to weather and contamination.", SUP),
            ("Supplied: only ~16% of processing facilities have adequate lab-testing capacity; frequent rejections due to aflatoxin from open-air drying.", SUP),
            ("Solar dryers, covered drying yards, cold storage and grading lines are the engineering responses (links to the Solar page).", RV),
        ]},
    "Export Regulations & Tariffs": {
        "points": [
            ("Supplied: governed by the Pakistan Export Strategy for Fruits and Vegetables (Strategic Trade Policy Framework).", SUP),
            ("Supplied: per the FBR, no export duty is imposed on goods exported from Pakistan.", SUP),
            ("Supplied: imported dried fruits/nuts for blending or re-export face ~20% customs duty, 20% regulatory duty and 25% sales tax (Customs Tariff 2025-26) — verify current rates.", SUP),
            ("Supplied: phased tariff reforms are gradually cutting maximum customs-duty bands.", SUP),
            ("Supplied: key barriers are SPS standards and maximum residue limits (MRL) for EU/US markets.", SUP),
        ]},
}

SOURCES = [
    ("Solar power in Pakistan — Wikipedia", "https://en.wikipedia.org/wiki/Solar_power_in_Pakistan"),
    ("PV Tech — Pakistan floating solar / solar tube wells (2019)", "https://www.pv-tech.org/"),
    ("pv magazine — Pakistan's installed PV capacity above 27 GW (Jan 2026)", "http://www.pv-magazine.com/2026/01/20/pakistans-installed-pv-capacity-estimated-above-27-gw/"),
    ("List of mines in Pakistan — Wikipedia", "https://en.wikipedia.org/wiki/List_of_mines_in_Pakistan"),
    ("Geological Survey of Pakistan — mineral resources overview", "https://www.gsp.gov.pk/"),
    ("Supplied reference links (owner-provided, Oct 2026) — TDAP gypsum analysis", "https://tdap.gov.pk/wp-content/uploads/2022/03/Analysis-of-Minerals-and-Metals-Sector-of-Pakistan-A-Case-of-Gypsum.pdf"),
    ("Supplied — CSIS: Minerals diplomacy meets market reality (Pakistan)", "https://www.csis.org/analysis/minerals-diplomacy-meets-market-reality-case-pakistan"),
    ("Supplied — CLAS: 18th Amendment and mining governance", "https://clas.org.pk/the-impact-of-the-18th-amendment-on-mining-governance-in-pakistan/"),
    ("Supplied — Dawn on provincial mining pushback", "https://www.dawn.com/news/1904452"),
]
DRY_SOURCES = [
    ("Supplied — TDAP: Pakistan Dry Fruits", "https://tdap.gov.pk/wp-content/uploads/2023/02/Pakistan-Dry-Fruits.pdf"),
    ("Supplied — TDAP: Dates production, consumption, exports", "https://tdap.gov.pk/wp-content/uploads/2025/01/Dates-Production-Consumption-Exports-Potential.pdf"),
    ("Supplied — OEC: dried fruits, Pakistan", "https://oec.world/en/profile/bilateral-product/dried-fruits/reporter/pak"),
    ("Supplied — Pakistan Export Strategy for Fruits and Vegetables", "https://www.commerce.gov.pk/wp-content/uploads/2024/05/Fruits_and_Vegetable_sector_strategy-Pakistan-3_web.pdf"),
    ("Supplied — Pakistan Customs Tariff 2025-26 (FBR)", "https://download1.fbr.gov.pk/Docs/20258111683941732Tariff-2025-26.pdf"),
]
