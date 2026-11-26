"""
india_hydropower_cea.py
India's own Central Electricity Authority (CEA) / NHPC-listed inventory of
Indus-basin hydropower projects in Jammu & Kashmir — transcribed from CEA's
"Profile on Hydro Development for U.T. of Jammu & Kashmir" (15 Jun 2026) and
NHPC project pages, as summarized in a published infographic citing those
two sources.

This is deliberately kept as its OWN dataset, separate from
data_loader.INDIA_WESTERN_RIVER_PROJECTS-style figures sourced from
Pakistani political statements elsewhere in this dashboard (e.g. the
Chenab Projects / "Indian Atrocities" page) — the two lists are compiled
from different sources and may not agree on scope or count; see the
Chenab Projects page, where both are shown side by side with a note on
where they diverge, rather than merged into one "true" list here.

CEA's own count is 10 operational + 7 under-construction = 17 projects;
CEA-concurred projects Sawalkote and Kirthai-II are explicitly NOT counted
in this 17, per the source infographic.
"""

# District-centroid coordinates (approximate — for visualization only, not
# the individual dam-site coordinates).
_DISTRICT_COORDS = {
    "Baramulla": {"lat": 34.2096, "lon": 74.3436},
    "Bandipora": {"lat": 34.4175, "lon": 74.6400},
    "Ganderbal": {"lat": 34.2300, "lon": 74.7700},
    "Kishtwar": {"lat": 33.3119, "lon": 75.7675},
    "Reasi/Udhampur": {"lat": 33.0000, "lon": 74.9800},
    "Ramban": {"lat": 33.2500, "lon": 75.2333},
    "Kathua": {"lat": 32.3700, "lon": 75.5300},
    "Poonch": {"lat": 33.7700, "lon": 74.0900},
}

PROJECTS = [
    {"rank": 1, "name": "Uri-I", "river": "Jhelum", "district": "Baramulla", "capacity_MW": 480, "status": "Operational"},
    {"rank": 2, "name": "Uri-II", "river": "Jhelum", "district": "Baramulla", "capacity_MW": 240, "status": "Operational"},
    {"rank": 3, "name": "Lower Jhelum", "river": "Jhelum", "district": "Baramulla", "capacity_MW": 105, "status": "Operational"},
    {"rank": 4, "name": "Upper Sindh-II & Ext.", "river": "Sindh Nallah", "district": "Ganderbal", "capacity_MW": 105, "status": "Operational"},
    {"rank": 5, "name": "Kishanganga", "river": "Kishanganga", "district": "Bandipora", "capacity_MW": 330, "status": "Operational"},
    {"rank": 6, "name": "Dulhasti", "river": "Chenab", "district": "Kishtwar", "capacity_MW": 390, "status": "Operational"},
    {"rank": 7, "name": "Salal I & II", "river": "Chenab", "district": "Reasi/Udhampur", "capacity_MW": 690, "status": "Operational"},
    {"rank": 8, "name": "Baglihar-I", "river": "Chenab", "district": "Ramban", "capacity_MW": 450, "status": "Operational"},
    {"rank": 9, "name": "Baglihar-II", "river": "Chenab", "district": "Ramban", "capacity_MW": 450, "status": "Operational"},
    {"rank": 10, "name": "Sewa-II", "river": "Sewa", "district": "Kathua", "capacity_MW": 120, "status": "Operational"},
    {"rank": 11, "name": "Pakal Dul", "river": "Marusudar", "district": "Kishtwar", "capacity_MW": 1000, "status": "Under Construction"},
    {"rank": 12, "name": "Parnai", "river": "Suran", "district": "Poonch", "capacity_MW": 37.5, "status": "Under Construction"},
    {"rank": 13, "name": "Kiru", "river": "Chenab", "district": "Kishtwar", "capacity_MW": 624, "status": "Under Construction"},
    {"rank": 14, "name": "Ratle", "river": "Chenab", "district": "Kishtwar", "capacity_MW": 850, "status": "Under Construction"},
    {"rank": 15, "name": "Kwar", "river": "Chenab", "district": "Kishtwar", "capacity_MW": 540, "status": "Under Construction"},
    {"rank": 16, "name": "Uri-I Stage-II", "river": "Jhelum", "district": "Baramulla", "capacity_MW": 240, "status": "Under Construction"},
    {"rank": 17, "name": "Dulhasti Stage-II", "river": "Chenab", "district": "Kishtwar", "capacity_MW": 260, "status": "Under Construction"},
]

# Attach approximate district-centroid coordinates for mapping.
for _p in PROJECTS:
    _coord = _DISTRICT_COORDS.get(_p["district"])
    _p["lat"] = _coord["lat"] if _coord else None
    _p["lon"] = _coord["lon"] if _coord else None

OPERATIONAL_COUNT = sum(1 for p in PROJECTS if p["status"] == "Operational")
UNDER_CONSTRUCTION_COUNT = sum(1 for p in PROJECTS if p["status"] == "Under Construction")
TOTAL_CAPACITY_MW = sum(p["capacity_MW"] for p in PROJECTS)
OPERATIONAL_CAPACITY_MW = sum(p["capacity_MW"] for p in PROJECTS if p["status"] == "Operational")
UNDER_CONSTRUCTION_CAPACITY_MW = sum(p["capacity_MW"] for p in PROJECTS if p["status"] == "Under Construction")

EXCLUDED_PROJECTS_NOTE = (
    "Separate CEA-concurred projects not counted in this 17-project list: "
    "Sawalkote and Kirthai-II."
)

SOURCE_NOTE = (
    "Central Electricity Authority (CEA), 'Profile on Hydro Development for U.T. of "
    "Jammu & Kashmir' (15 Jun 2026); NHPC project pages. District coordinates used "
    "for mapping are approximate centroids, not individual dam-site coordinates."
)

MAP_NOTE = (
    "This is India's own CEA/NHPC-sourced count (10 operational + 7 under construction). "
    "It is compiled independently of the Pakistan-statement-sourced 'India's western-river "
    "projects' list elsewhere in this dashboard (Chenab Projects page) — see that page for "
    "both lists side by side and where they diverge."
)
