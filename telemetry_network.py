"""
telemetry_network.py
WAPDA flood-forecasting telemetry network reference data — the real station
lists behind the "Meteor Burst Telecommunication System of WAPDA" and
"HF Radio maintained by WAPDA" network diagrams, split by network area:

- EASTERN_RIVERS_WIRELESS_STATIONS: the Wireless Network (Eastern Rivers) —
  headworks, barrages, syphons, bridges and nullah gauging sites on the
  Ravi/Chenab/Sutlej system, WITH surveyed latitude/longitude.
- WESTERN_RIVERS_HF_RADIO_STATIONS: the High-Frequency (HF) Radio Network
  (Western Rivers) — dams, barrages and flood-forecasting offices on the
  Indus/Jhelum system. Coordinates were not published in the source
  deployment list, so only the station/facility name and network area are
  recorded; map rendering falls back to an approximate location (nearest
  known town/city) where one is available via coordinates.TELEMETRY_FALLBACK_COORDS.

Both lists are the stations WAPDA uses to collect/relay river, canal and
rainfall telemetry for flood forecasting and Indus Waters Treaty Permanent
Indus Commission (PIC) data exchange — NOT the readings themselves (no
live or historical discharge values are published here).
"""

# ---------------------------------------------------------------------------
# Eastern Rivers — Wireless Network (coordinates supplied in source data)
# ---------------------------------------------------------------------------
EASTERN_RIVERS_WIRELESS_STATIONS = [
    {"location": "Kot Naina", "lat": 32.18000, "lon": 74.92000},
    {"location": "Jassar", "lat": 32.09058, "lon": 74.94270},
    {"location": "Ravi Syphon", "lat": 31.72200, "lon": 74.46800},
    {"location": "Shahdara", "lat": 31.60657, "lon": 74.29650},
    {"location": "Balloki", "lat": 31.21920, "lon": 73.85890},
    {"location": "Sidhnai", "lat": 30.69000, "lon": 72.46000},
    {"location": "Bein Nullah at Chak Amru", "lat": 32.36670, "lon": 74.96670},
    {"location": "Bein Nullah at Shakargarh", "lat": 32.26300, "lon": 75.16000},
    {"location": "Deg Nullah at Q.S. Singh", "lat": 32.10000, "lon": 74.65000},
    {"location": "Bassantar Nullah", "lat": 32.15000, "lon": 74.95000},
    {"location": "G.S. Wala", "lat": 31.03835, "lon": 74.51836},
    {"location": "Bakarke", "lat": 30.93000, "lon": 74.32000},
    {"location": "Sulemanki", "lat": 30.38194, "lon": 73.86194},
    {"location": "Islam", "lat": 29.82639, "lon": 72.54861},
    {"location": "Melsi Syphon", "lat": 29.72816, "lon": 72.25317},
    {"location": "Marala", "lat": 32.67600, "lon": 74.46800},
    {"location": "Khanki", "lat": 32.45000, "lon": 74.12500},
    {"location": "Qadirabad", "lat": 32.32180, "lon": 73.68505},
    {"location": "Chinot Bridge", "lat": 31.75264, "lon": 72.94794},
    {"location": "Trimmu", "lat": 31.14506, "lon": 72.14492},
    {"location": "Rawaz Bridge", "lat": 31.40706, "lon": 72.29046},
    {"location": "Punjnad", "lat": 29.34329, "lon": 71.02370},
    {"location": "Aik Nullah at Ura", "lat": 32.49167, "lon": 74.50694},
    {"location": "Palku Nullah", "lat": 32.44944, "lon": 74.13333},
    {"location": "New Rasul", "lat": 32.70500, "lon": 73.65600},
    {"location": "Khushab Bridge", "lat": 32.29500, "lon": 72.35000},
    {"location": "Kalabagh", "lat": 32.96200, "lon": 71.54600},
    {"location": "Taunsa", "lat": 30.70500, "lon": 70.65000},
    {"location": "Mithankot", "lat": 28.92000, "lon": 70.34000},
    {"location": "Ghazighat", "lat": 30.05000, "lon": 71.15000},
    {"location": "Chachran Sharif", "lat": 28.87214, "lon": 70.45679},
]

# ---------------------------------------------------------------------------
# Western Rivers — HF Radio Network (no coordinates in the source deployment
# list; name + network area only)
# ---------------------------------------------------------------------------
WESTERN_RIVERS_HF_RADIO_STATIONS = [
    {"network_area": "Western Rivers", "facility": "Mangla Dam"},
    {"network_area": "Western Rivers", "facility": "Tarbela Dam"},
    {"network_area": "Western Rivers", "facility": "Besham"},
    {"network_area": "Western Rivers", "facility": "Jaglot"},
    {"network_area": "Western Rivers", "facility": "Skardu"},
    {"network_area": "Western Rivers", "facility": "Daggar"},
    {"network_area": "Western Rivers", "facility": "Phulra"},
    {"network_area": "Western Rivers", "facility": "Oghi"},
    {"network_area": "Western Rivers", "facility": "Shinkiari"},
    {"network_area": "Western Rivers", "facility": "Khairabad"},
    {"network_area": "Western Rivers", "facility": "Nowshera"},
    {"network_area": "Western Rivers", "facility": "Kallar"},
    {"network_area": "Western Rivers", "facility": "G. Habibullah"},
    {"network_area": "Western Rivers", "facility": "Muzaffarabad"},
    {"network_area": "Western Rivers", "facility": "Domel"},
    {"network_area": "Western Rivers", "facility": "Kotli"},
    {"network_area": "Western Rivers", "facility": "Kohala"},
    {"network_area": "Western Rivers", "facility": "Plandri"},
    {"network_area": "Western Rivers", "facility": "Azadpatan"},
    {"network_area": "Western Rivers", "facility": "Chashma Barrage"},
    {"network_area": "Western Rivers", "facility": "Water Resource Management Directorate"},
    {"network_area": "Western Rivers", "facility": "Central Flood Forecasting Division"},
]

NETWORK_NOTE = (
    "These are the station/facility lists behind WAPDA's two flood-forecasting "
    "telemetry systems — the Meteor Burst Telecommunication System and the "
    "High-Frequency (HF) Radio Network. They record *where* WAPDA collects and "
    "relays river, canal and rainfall telemetry for flood forecasting and Indus "
    "Waters Treaty PIC data exchange; the live/historical readings themselves "
    "are not publicly published, so no discharge values are shown here. Eastern "
    "Rivers (wireless) station coordinates were supplied in the source "
    "deployment data; Western Rivers (HF radio) station coordinates were not, "
    "so those sites are listed by name only."
)

SOURCE_NOTE = (
    "WAPDA — 'Meteor Burst Telecommunication System of WAPDA' and "
    "'High Frequency Radio maintained by WAPDA' network reference material."
)


def all_eastern_station_names():
    return [s["location"] for s in EASTERN_RIVERS_WIRELESS_STATIONS]


def all_western_station_names():
    return [s["facility"] for s in WESTERN_RIVERS_HF_RADIO_STATIONS]
