"""
army_role.py
Pakistan Army's role across this dashboard's sectors (water, dams, floods,
disaster response, canals/agriculture, mountains & connectivity, project
security, geo-politics, socio-economy).

Every entry carries an evidence tag:
  "Source-backed"      - stated on a page the author read while compiling this module
  "Reported - verify"  - taken from a headline/search result or widely reported
                         background; confirm against the cited source before formal use

Contested items (e.g. the Cholistan canals) are shown as each side's reported
position, not as settled fact. This is an explanatory summary, not an official
or legal statement.
"""

FRAMING_NOTE = (
    "The Pakistan Army acts in this project's sectors in three distinct capacities: "
    "(1) **aid to civil authority** — flood/disaster rescue and relief under civil "
    "coordination (NDMA, PDMAs, provincial governments); (2) **engineering and "
    "construction** — via the Army Corps of Engineers and its affiliate organisations "
    "such as the Frontier Works Organization (FWO); and (3) **security and economic "
    "initiatives** — protection of major projects and army-linked agricultural/commercial "
    "ventures. Items in the third group are politically debated; they are presented here "
    "as reported facts and stated positions, not as a verdict."
)

EVIDENCE_NOTE = (
    "Evidence tags: **Source-backed** = stated on a page read while compiling this page. "
    "**Reported - verify** = from a headline/search result or widely reported background — "
    "confirm against the linked source before citing in a formal context."
)

SECTORS = {
    "Dams & Hydropower": {
        "dashboard_section": "🚧 Dams & Barrages",
        "points": [
            ("The Frontier Works Organization (FWO) was created by the Pakistan Army Corps of Engineers in 1966 and remains an Army-affiliated command; water resources and dams/irrigation are among its listed areas of work.", "Source-backed"),
            ("Diamer-Bhasha Dam: the main civil-works contract was reported as awarded to a Power China–FWO joint venture.", "Reported - verify"),
            ("A 2005 rehabilitation project at Sukkur Barrage is credited to FWO in a reference cited on FWO's encyclopedia entry.", "Reported - verify"),
            ("Army security cover for large dam construction sites (e.g. in Gilgit-Baltistan/KPK) has been publicly pledged by the Army for worker protection.", "Reported - verify"),
        ],
    },
    "Rivers, Barrages & Flood Management": {
        "dashboard_section": "🌊 Rivers",
        "points": [
            ("Pre-flood: Army engineers check that flood-fighting equipment is serviceable, hold preparatory meetings at Corps and GHQ level, and inspect flood-protection structures (bunds, barrages, spurs) jointly with provincial irrigation departments, reporting deficiencies to them.", "Source-backed"),
            ("Flood-fighting material and explosives are pre-stocked at designated breaching sections, to be used only when required.", "Source-backed"),
            ("During floods: an officer from 4 Corps Engineers monitors the Flood Warning Centre in Lahore; forecasts and warnings pass up the engineering chain and units deploy to assigned areas, in coordination with local civil administrations.", "Source-backed"),
            ("Post-flood: the Engineer-in-Chief / DG Engineers chairs a coordination review of how all flood-management agencies performed.", "Source-backed"),
            ("Provincial governments, not the Army, supply logistics such as boats, life jackets, vehicles and tents.", "Source-backed"),
        ],
    },
    "Disaster Response (Floods, Earthquakes, GLOFs)": {
        "dashboard_section": "⚠️ Disaster Risk Context",
        "points": [
            ("2022 floods: the Army ran relief operations across the country alongside civil agencies.", "Reported - verify"),
            ("August 2025 floods (Punjab): troops were requisitioned for relief as India released water; ISPR reported engineer brigade, infantry and medical units deployed for rescue; the government said about 210,000 people were evacuated as Army operations expanded.", "Reported - verify"),
            ("The Army has also been a principal responder in other major national disasters (e.g. the 2005 Kashmir earthquake and the 2010 floods) — widely documented background.", "Reported - verify"),
            ("Army Aviation and mountain-trained units are commonly used for rescue in Gilgit-Baltistan and northern KPK, where roads are cut by floods, landslides and GLOF events.", "Reported - verify"),
        ],
    },
    "Irrigation, Canals & Agriculture (Green Pakistan Initiative)": {
        "dashboard_section": "🔀 Link Canals / 📈 Socio-Economic & Agro-Economic",
        "points": [
            ("The Green Pakistan Initiative (GPI), launched in July 2023, was co-launched by the Army chief and the Prime Minister; it is described as a ~$3.3bn (Rs 945bn) programme to build six canals to irrigate large areas of barren land.", "Source-backed"),
            ("The Cholistan Canal is the largest: about 176 km long, an estimated $783m, estimated capacity 4,120 cusecs, expected completion by mid-2030.", "Source-backed"),
            ("The Army-owned Green Corporate Initiative has been tasked with converting wastelands into farmland; a retired general heads the GPI.", "Source-backed"),
            ("Sindh's objection: protests in February and March 2025, a unanimous Sindh Assembly resolution demanding a halt, and a dissent by Sindh's IRSA representative against an IRSA certificate that found enough water available. An IRSA memo cited in the same reporting warned of shortages (Punjab ~20%, Sindh ~14%).", "Source-backed"),
            ("Supporters' position: the canals would bring wasteland under cultivation and improve food security; Sindh's position: they could divert Indus flows and worsen desertification and shortages downstream. Both are stated positions, not adjudicated fact.", "Source-backed"),
            ("Later developments (reported): the canal plan was subsequently put on hold after Council of Common Interests (CCI) discussions in April 2025 — this was NOT covered by the source above; verify before citing.", "Reported - verify"),
        ],
    },
    "Mountains, Connectivity & Telecom (Karakoram / Gilgit-Baltistan)": {
        "dashboard_section": "⛰️ Mountain Ranges / 📡 WAPDA Telemetry Network",
        "points": [
            ("FWO led the design and construction of the 805-km Karakoram Highway (KKH), working with Chinese military engineers.", "Source-backed"),
            ("The Special Communications Organization (SCO), an Army-run organisation, provides telecom services in Gilgit-Baltistan and Azad Kashmir; its legal basis for offering 4G in Gilgit-Baltistan has been publicly discussed.", "Reported - verify"),
            ("FWO is also reported to have worked on the 2010 Attabad landslide-dam emergency spillway and later Attabad tunnels in Hunza (see the Hunza River entry on the Rivers page).", "Reported - verify"),
            ("The WAPDA telemetry networks documented on this dashboard (Eastern wireless, Western HF radio, meteor-burst) are WAPDA systems; no Army operating role is documented in the supplied WAPDA materials.", "Source-backed"),
        ],
    },
    "Security of Major Projects (CPEC & Water Projects)": {
        "dashboard_section": "🇨🇳 China Hydropower (CPEC) / 🚧 Dams & Barrages",
        "points": [
            ("A dedicated Army Special Security Division (SSD) structure was raised around 2016 to protect CPEC projects and Chinese personnel — widely reported background.", "Reported - verify"),
            ("The Army has pledged to protect workers at mega-dam construction sites.", "Reported - verify"),
            ("May 2026 reporting: the government planned a dedicated WAPDA security force for major water projects, to relieve the burden of security duties on other forces. (The full article could not be read while compiling this page — treat as a reported plan.)", "Reported - verify"),
        ],
    },
    "Geo-Political & Strategic (Indus Waters Treaty)": {
        "dashboard_section": "🗺️ Geo-Political & Strategic / 🇮🇳 Chenab Projects & IWT",
        "points": [
            ("The Army leadership sits within Pakistan's national-security decision structures, where water security is treated as a national-security issue; public statements by the defence establishment on water have been reported in the media (check ISPR releases for exact wording).", "Reported - verify"),
            ("Formal IWT instruments on this dashboard (Permanent Indus Commission, Neutral Expert, Court of Arbitration) are civilian/legal mechanisms; the Army is not a party to them.", "Source-backed"),
            ("The August 2025 floods were accompanied by reporting on cross-border flood warnings and data-sharing; the Army's role was relief and evacuation, not data exchange (see 'Impact on Transboundary Water Cooperation' on the IWT page).", "Reported - verify"),
        ],
    },
    "Socio-Economic & Economic Role": {
        "dashboard_section": "📈 Socio-Economic & Agro-Economic",
        "points": [
            ("The military runs commercial entities in several sectors, as noted in international reporting on the GPI; Army-linked foundations are active in areas such as fertilizer and agriculture.", "Source-backed"),
            ("Army leadership participates in the government's investment-facilitation structures (e.g. the Special Investment Facilitation Council, established 2023), which promote agriculture and mining investment.", "Reported - verify"),
            ("Critics of corporate-farming plans (farmer groups, rights organisations) argue they risk dispossessing small farmers; supporters argue they raise productivity. Both are stated positions.", "Reported - verify"),
        ],
    },
    "Forests, Lakes, Deserts & National Parks": {
        "dashboard_section": "🌲 Forests / 🏞️ Lakes / 🏜️ Deserts / 🌳 National Parks",
        "points": [
            ("Deserts: the Cholistan desert is the target area of the Cholistan Canal and Army-linked corporate-farming plans described above; the Thar, Kharan and Thal desert entries have no Army-specific programme documented in this dashboard's sources.", "Source-backed"),
            ("Forests / national parks / lakes: no major Army-run conservation programme is documented in this dashboard's sources; the Army is commonly reported to take part in national tree-plantation drives and relief in park/lake areas after disasters.", "Reported - verify"),
        ],
    },
}

SOURCES = [
    ("Pakistan military eyes key role developing giant copper and gold mine (Mining.com, 2019)", "https://www.mining.com/web/pakistan-military-eyes-key-role-developing-giant-copper-gold-mine/"),
    ("PM Shehbaz okays 2000MW solar power projects in public sector (ARY)", "https://arynews.tv/pm-shehbaz-okays-2000mw-solar-power-projects-in-public-sector/"),
    ("Pakistan announces $197 million project to solarize 27,000 tubewells (Arab News)", "https://arab.news/nh9ug"),
    ("Frontier Works Organization — Wikipedia", "https://en.wikipedia.org/wiki/Frontier_Works_Organization"),
    ("Federal Flood Commission — Pak Army's role in flood management", "https://ffc.gov.pk/pak-army-2/"),
    ("Engineer brigade, infantry, medical units deployed for rescue during floods: ISPR (Aaj News)", "https://english.aaj.tv/news/amp/330431562"),
    ("Pakistan says 210,000 evacuated as army expands flood relief operations in Punjab (Arab News)", "https://www.arabnews.com/node/2613204/amp"),
    ("Pakistan Army troops requisitioned in Punjab for flood relief (ARY News)", "https://arynews.tv/pakistan-army-troops-requisitioned-in-punjab-for-flood-relief-activities"),
    ("Army continues flood relief operations across Pakistan (Express Tribune, 2022)", "https://tribune.com.pk/story/2372482/1"),
    ("Why is Pakistan's new canal project sparking water shortage fears? (Al Jazeera, Mar 2025)", "https://www.aljazeera.com/news/2025/3/27/why-is-pakistans-new-canal-project-sparking-water-shortage-fears"),
    ("The Green Pakistan Initiative — green capitalism and rural dispossession (TNI)", "https://www.tni.org/es/node/19075"),
    ("Diamer-Bhasha dam contract awarded to Power China-FWO (Profit)", "https://profit.pakistantoday.com.pk/?p=90375"),
    ("SCO claims its 4G services in Gilgit-Baltistan are legal (ProPakistani)", "https://propakistani.pk/2019/10/07/sco-claims-its-4g-services-in-gilgit-baltistan-are-legal/"),
    ("Pakistan army plans new unit to protect CPEC projects (Gulf News)", "https://gulfnews.com/world/asia/pakistan/pakistan-army-plans-new-unit-to-protect-cpec-projects-1.64050168"),
    ("Pakistan army vows to protect workers at mega dam construction site (Arab News)", "https://arab.news/gqbv9"),
    ("Govt plans dedicated WAPDA security force for major water projects (ProPakistani, May 2026)", "https://propakistani.pk/2026/05/25/govt-plans-dedicated-wapda-security-force-for-major-water-projects/amp/"),
]


# ===========================================================================
# Additions from a reference text supplied by the project owner (Oct 2026)
# ===========================================================================
# Everything below is taken from that supplied text. It was NOT independently
# checked against primary sources while compiling this page, and several items
# are allegations, unsourced figures or one-sided characterisations. They are
# tagged SUPPLIED and shown as the supplied text states them, with contested
# items presented as stated positions.
SUPPLIED = "Supplied reference - verify"

EVIDENCE_NOTE = (
    "Evidence tags: ✅ **Source-backed** = stated on a page read while compiling this page. "
    "🔎 **Reported - verify** = from a headline/search result or widely reported background. "
    "📄 **Supplied reference - verify** = taken from reference text supplied by the project "
    "owner and not independently checked — figures, quotations and allegations in these items "
    "should be confirmed against primary sources (ISPR releases, court judgments, SIFC/WAPDA "
    "documents) before formal use."
)

# --- Extend existing tabs -------------------------------------------------
SECTORS["Rivers, Barrages & Flood Management"]["points"] += [
    ("Three-phase flood engineering model: PRE-FLOOD (structural audits of barrages, spurs and bunds; breaching-section preparation) → ACTIVE RESCUE (amphibious evacuations, aerial food drops) → POST-FLOOD (temporary Bailey bridges, breach sealing and drainage).", SUPPLIED),
    ("Pre-flood: months before the monsoon the Engineer-in-Chief branch works with the Federal Flood Commission; explosive charges and technical teams are pre-positioned at designated controlled breaching sections — areas intentionally breached in historic surges to divert water from urban centres and protect reservoir structures.", SUPPLIED),
    ("Post-flood recovery: Bailey (rapid-assembly steel panel) bridges to reconnect valleys and villages when concrete infrastructure collapses; heavy earth-moving machinery to close unplanned dyke failures, pump out stagnant floodwater from agricultural lowlands and clear mountain landslides.", SUPPLIED),
]
SECTORS["Disaster Response (Floods, Earthquakes, GLOFs)"]["points"] += [
    ("During the 2010 and 2022 floods the military deployed tens of thousands of troops to evacuate stranded citizens, distribute food and clear blocked waterways.", SUPPLIED),
    ("Active rescue phase: specialised amphibious boats, aviation wings and thousands of troops to reach isolated populations; field medical clinics, water-purification plants and large logistics hubs for food and shelter.", SUPPLIED),
]
SECTORS["Irrigation, Canals & Agriculture (Green Pakistan Initiative)"]["points"] += [
    ("The Cholistan Canal is described as a 176 km canal branching from the Sutlej at Sulemanki Headworks, intended to bring ~450,000 acre-feet to a Cholistan command area.", SUPPLIED),
    ("Sindh characterises the six new canals on the Indus system as a violation of the 1991 Water Apportionment Accord; the Sindh Assembly passed resolutions demanding a halt, and the Sindh High Court is stated to have issued a stay order against IRSA's water-availability certificate; Sindh's leadership said the project would face cancellation before the provincial budget.", SUPPLIED),
]
SECTORS["Geo-Political & Strategic (Indus Waters Treaty)"]["points"] += [
    ("Stance (A): under National Security Committee (NSC) directives the military leadership vowed to take all necessary measures to protect Pakistan's rightful share under the 1960 Indus Waters Treaty; top officials are described as declaring that any unilateral attempt to stop or divert allocated river flows would be treated as a grave national-security threat.", SUPPLIED),
    ("Stance (B): the military is described as viewing unhindered flow of the Western Rivers (Indus, Jhelum, Chenab) as a non-negotiable red line tied to national survival, hardening after India's move to hold the treaty in abeyance, halt data sharing and build upstream infrastructure.", SUPPLIED),
    ("Deterrence: any unilateral upstream attempt to block, divert or drastically alter Western River flows is described as an act of aggression, with the Army said to have warned that it would take necessary countermeasures to guarantee downstream water security for ~240 million citizens. (Exact wording and source not cited in the supplied text — check ISPR/NSC statements; the Indian side disputes the framing, and the treaty's own legal mechanisms are the PIC, Neutral Expert and Court of Arbitration.)", SUPPLIED),
    ("National narrative: because over 80% of Pakistan's agricultural economy depends on the Indus Basin, the supplied text says the military steers national communication strategy and, citing 'leaked strategic directives', commands media operations to frame treaty modifications or upstream dams (Kishanganga, Ratle) as violations of international law. ⚠️ This is an unsourced allegation in the supplied text — no document is cited and it has not been verified.", SUPPLIED),
    ("Domestic response: the military-backed SIFC is described as pushing fast-tracked mega-dams (Diamer-Bhasha, Mohmand), expansion of strategic storage from 13.5 to 23.5 MAF and automated flow monitoring via telemetry (see the WAPDA Telemetry Network page).", SUPPLIED),
]

# --- New tabs -------------------------------------------------------------
SECTORS["Drinking Water & Local Supply (Balochistan, Chagai)"] = {
    "dashboard_section": "🏜️ Deserts / ⚠️ Disaster Risk Context",
    "points": [
        ("Through the Frontier Corps and local engineering units, the Army is described as installing solar-powered water-supply schemes and clean-drinking-water filtration plants in remote, drought-prone areas such as Balochistan and Chagai.", SUPPLIED),
    ],
}

SECTORS["SIFC Water Technology (LIMS, HEIS, Solar Tube Wells)"] = {
    "dashboard_section": "📈 Socio-Economic & Agro-Economic / 🛰️ SEBAL Evapotranspiration Engine",
    "points": [
        ("Context: ~93% of Pakistan's water is used in agriculture and over 60% of it is described as lost to flood irrigation and poorly maintained channels; the military-backed Special Investment Facilitation Council (SIFC) pursues a high-tech approach through the Green Pakistan Initiative (GPI).", SUPPLIED),
        ("LIMS-COE (Land Information and Management System): operated with heavy technical input from the military's geographic and IT wings; uses satellite remote sensing, AI and mathematical modelling to monitor land and water stress in real time.", SUPPLIED),
        ("Precision irrigation advisories: automated, satellite-backed alerts sent to farmers via a digital platform and SMS saying how much water soil needs (the same remote-sensing idea as this dashboard's SEBAL evapotranspiration engine, which is an offline educational tool, not LIMS).", SUPPLIED),
        ("Canal rotation management: with Asian Development Bank assistance, mathematical modelling is used to manage canal distribution across Punjab and reduce tail-end waste.", SUPPLIED),
        ("High-Efficiency Irrigation Systems (HEIS): centre-pivot and sprinkler systems at large corporate farms (e.g. a 100,000-acre Cholistan project), stated to use ~25% less water; modular drip irrigation SIFC aims to scale across 4.4 million acres of barren or under-used state land.", SUPPLIED),
        ("Solarisation of tube wells: SIFC is stated to have facilitated a $197+ million project to solarise 27,000 agricultural tube wells in Balochistan, with smart pumping to help provincial authorities monitor and cap groundwater extraction.", SUPPLIED),
        ("Stated water-saving mandates: 25% lower consumption via centre-pivot benchmarks in arid areas such as Cholistan (Bahawalpur); alternate-mode irrigation (smart drip, recycled water) required of joint-venture allottees (e.g. the 52,000+ acre Sindh allotment) rather than public canals; and a crop-specific Abyana (water-pricing) framework targeting Rs 300–325 billion to fund canal lining and dams.", SUPPLIED),
    ],
}

SECTORS["SIFC Corporate Farming, Gulf Investment & Criticism"] = {
    "dashboard_section": "📈 Socio-Economic & Agro-Economic",
    "points": [
        ("Land bank: SIFC has identified millions of acres of barren state land for reclamation — e.g. 52,000+ acres in Sindh and 50,000 acres in Cholistan earmarked for tech-driven corporate farming.", SUPPLIED),
        ("Joint-venture vehicle: land is not sold; provincial governments sign long-term (typically 30–50 year) lease joint ventures with a corporate intermediary such as Green Corporate Initiative (Pvt) Ltd — described as heavily Army-backed and managed — which sub-allocates parcels to corporate and international investors.", SUPPLIED),
        ("Profit sharing (Sindh agreement): 40% to the provincial treasury, 40% spent locally on socio-economic infrastructure (solar water schemes, schools, hospitals), 20% ring-fenced for agricultural research and development.", SUPPLIED),
        ("Gulf finance: SIFC is positioned as a single-window portal to secure up to $6 billion of agricultural FDI from the GCC, framed as a loop where Gulf capital modernises Pakistan's water technology and yields support Gulf food security. The state describes these projects as boosting agricultural exports by 37%.", SUPPLIED),
        ("Criticism — water squeeze: environmental groups say irrigating arid zones such as Cholistan means diverting water from an over-allocated, climate-stressed Indus Basin, which could hurt downstream small farmers.", SUPPLIED),
        ("Criticism — 'locals out': peasant organisations such as the Pakistan Kissan Rabta Committee (PKRC) and Awami Tahreek argue that dedicating state land to foreign-facing corporates shuts out landless local farmers, and that food security needs land reform instead.", SUPPLIED),
        ("Criticism — inter-provincial risk: activists warn that allocating river water to military-run corporate entities could inflame Punjab–Sindh water-sharing disputes under IRSA and the historic accords.", SUPPLIED),
    ],
    "tables": [
        ("Gulf investment interests named in the supplied text", [
            {"Country": "Saudi Arabia", "Entities / areas": "SALIC, PIF", "Stated focus": "Funding including an initial $500 million linked to the LIMS Centre of Excellence; corporate grain, fodder and livestock."},
            {"Country": "UAE", "Entities / areas": "ADQ, Al Dahra, AD Ports Group", "Stated focus": "Automated agribusiness supply chains linked to logistics infrastructure (e.g. port terminal leases)."},
            {"Country": "Kuwait & Qatar", "Entities / areas": "Kuwait Investment Authority, sovereign funds", "Stated focus": "Multi-billion MoUs under SIFC for mechanised irrigation pipelines, smart water storage and deep-well drilling."},
        ]),
        ("Sindh agreement profit split (40-40-20)", [
            {"Share": "40%", "Goes to": "Provincial government treasury"},
            {"Share": "40%", "Goes to": "Local socio-economic infrastructure (solar water schemes, schools, hospitals)"},
            {"Share": "20%", "Goes to": "Regional agricultural research & development"},
        ]),
    ],
}

SECTORS["Courts, Legal Review & Cholistan Ground Realities"] = {
    "dashboard_section": "🏜️ Deserts / 🔀 Link Canals",
    "points": [
        ("March 2023: the Public Interest Law Association of Pakistan (PILAP) petitioned the Lahore High Court (LHC) against the caretaker Punjab government's lease of 45,000+ acres of state land to the military.", SUPPLIED),
        ("LHC single bench (Justice Abid Hussain Chattha, 134-page judgment): ruled the transfer illegal — the caretaker government lacked the constitutional mandate to allot public land, and the Armed Forces have no legal mandate to engage in corporate farming outside their constitutional scope.", SUPPLIED),
        ("July 2023: the Punjab government appealed; a two-member LHC bench (headed by Justice Ali Baqar Najafi) suspended the restriction, accepting the argument that courts should not regulate agricultural policy or executive economic decisions — allowing SIFC-backed corporate farming to proceed and scale to other provinces (stated target: over 4.8 million acres).", SUPPLIED),
        ("Later: in proceedings by 100+ Cholistan residents against displacement, the LHC Bahawalpur bench is stated to have pushed the Punjab government to hold in abeyance two caretaker-era land-transfer agreements (with Green Corporate Initiatives and the Military Family Rehabilitation Organisation, MFRO) and directed the provincial cabinet, within 8 weeks, to re-examine their legality against 11 court-framed questions on the limits of caretaker powers; the state assured the court no adverse displacement of locals would occur meanwhile.", SUPPLIED),
        ("Farmer alliances (Awami Tahreek, PKRC) have held street protests against the 'strategic canals' to irrigate ~6.6 million acres of corporate land in Cholistan.", SUPPLIED),
        ("On the ground — salinity: some leased areas are reported to have groundwater too saline for crops; the Army-run FWO and joint ventures reportedly had to drill tube wells and pump water from 10–14 km away.", SUPPLIED),
        ("On the ground — climate: desert heat reportedly caused geo-membrane and concrete-lined channels to fail or clog with sand; corporate farms (e.g. backed by Terra Crop Innovation and SinoPak Guangdong) reportedly lost hundreds of acres of newly planted cotton to sandstorms.", SUPPLIED),
        ("Note: the supplied text's dates/outcomes for these proceedings are not individually sourced; confirm against the court orders before citing.", SUPPLIED),
    ],
    "diagram": (
        "[LHC Single Bench, Mar 2023]  ──►  [LHC Double Bench, Jul 2023]  ──►  [Later LHC Bahawalpur review]\n"
        "Allotment ruled ILLEGAL;            Ruling SUSPENDED on appeal;          Two transfer agreements held in abeyance;\n"
        "Army has no business mandate.      govt: policy is executive.           cabinet re-examines (8 weeks, 11 questions)."
    ),
}

SUPPLIED_SOURCE_NOTE = (
    "Items tagged 'Supplied reference - verify' come from reference text provided by the "
    "project owner (October 2026), which cites no individual sources. Check them against "
    "ISPR/NSC statements, SIFC and WAPDA documents, Lahore High Court and Sindh High Court "
    "orders, and the 1991 Water Apportionment Accord before formal use."
)

# Preferred tab order
SECTORS["Mining & Minerals"] = {
    "dashboard_section": "⛏️ Mining Sectors",
    "points": [
        ("A March 2019 headline (Profit/Arab News/Mining.com/RFE-RL) reported that the Pakistan military was seeking a key role in developing the Reko Diq copper-gold mine (Chagai, Balochistan) — the headline is cited here; read the articles for the exact role described.", "Reported - verify"),
        ("The Army's Frontier Works Organization (FWO) and National Logistics Corporation (NLC) are engineering/logistics organisations widely reported to build roads, tunnels and transport links that serve remote mineral areas; confirm project-by-project.", "Reported - verify"),
        ("Security of mining areas and corridors in Balochistan (Chagai, Saindak, Duddar) is handled by security forces alongside provincial and federal agencies; this is part of the 'Security of Major Projects' role.", "Reported - verify"),
        ("The SIFC (Special Investment Facilitation Council), in which the Army has a stated facilitation role, lists minerals and mining among its priority sectors; the 2025 minerals-investment forum and rare-earth/critical-mineral MOUs were reported — verify current status.", "Reported - verify"),
        ("Debate: supporters cite security and speed of delivery; critics (including provincial voices in Balochistan) raise concerns about local consent, benefit-sharing and the 18th Amendment (minerals are a provincial subject). Both positions are reported, not adjudicated here.", "Reported - verify"),
    ],
}

SECTORS["Solar Energy"] = {
    "dashboard_section": "☀️ Solar Energy Sectors",
    "points": [
        ("The federal government approved ~2,000 MW of public-sector solar projects (ARY News headline); any Army-linked executing role should be confirmed from the project documents.", "Reported - verify"),
        ("ECNEC approved solarization of agricultural tube wells, including a reported ~$197 million programme to solarize ~27,000 tube wells in Balochistan (Arab News / APP headlines). The Army's role in SIFC-linked 'solar tube well' initiatives is covered under 'SIFC Water Technology'.", "Reported - verify"),
        ("FWO/NLC-type engineering organisations and Army Corps of Engineers units are reported to build solar plants and solar water-supply schemes in remote areas (e.g. Balochistan, border and mountain posts); confirm each scheme.", "Reported - verify"),
        ("Military installations and cantonments also adopt rooftop/captive solar to reduce power cost — a general trend; no specific figures are asserted here.", "Reported - verify"),
        ("Debate: faster delivery and remote-area reach versus transparency, competitive-bidding and civilian-oversight questions; both views are reported, not adjudicated.", "Reported - verify"),
    ],
}

_ORDER = [
    "Dams & Hydropower",
    "Rivers, Barrages & Flood Management",
    "Disaster Response (Floods, Earthquakes, GLOFs)",
    "Drinking Water & Local Supply (Balochistan, Chagai)",
    "Irrigation, Canals & Agriculture (Green Pakistan Initiative)",
    "SIFC Water Technology (LIMS, HEIS, Solar Tube Wells)",
    "SIFC Corporate Farming, Gulf Investment & Criticism",
    "Courts, Legal Review & Cholistan Ground Realities",
    "Mountains, Connectivity & Telecom (Karakoram / Gilgit-Baltistan)",
    "Security of Major Projects (CPEC & Water Projects)",
    "Geo-Political & Strategic (Indus Waters Treaty)",
    "Socio-Economic & Economic Role",
    "Forests, Lakes, Deserts & National Parks",
    "Mining & Minerals",
    "Solar Energy",
]
SECTORS = {k: SECTORS[k] for k in _ORDER}
