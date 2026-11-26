"""
coordinates.py
Static latitude/longitude reference data used across the app for mapping.
All coordinates are approximate (centroid / well-known point) and meant for
visualization purposes, not survey-grade GIS work.
"""

PROVINCE_COORDS = {
    "Gilgit-Baltistan": {"lat": 35.8, "lon": 75.0, "capital": "Gilgit"},
    "Khyber Pakhtunkhwa (KPK)": {"lat": 34.5, "lon": 72.0, "capital": "Peshawar"},
    "Punjab": {"lat": 31.5, "lon": 73.1, "capital": "Lahore"},
    "Sindh": {"lat": 25.9, "lon": 68.6, "capital": "Karachi"},
    "Balochistan": {"lat": 28.5, "lon": 65.0, "capital": "Quetta"},
    "Azad Jammu & Kashmir (AJK)": {"lat": 33.9, "lon": 73.8, "capital": "Muzaffarabad"},
    "Islamabad Capital Territory (ICT)": {"lat": 33.7, "lon": 73.1, "capital": "Islamabad"},
}

RIVER_COORDS = {
    "Indus River": [
        (35.30, 74.90), (34.15, 73.24), (32.65, 71.86), (31.20, 70.90),
        (28.42, 70.32), (25.40, 68.36), (24.10, 67.45),
    ],
    "Jhelum River": [(34.37, 74.47), (33.10, 73.73), (31.20, 72.10), (30.94, 72.35)],
    "Chenab River": [(32.95, 75.85), (32.30, 74.18), (30.16, 71.86)],
    "Ravi River": [(32.20, 75.90), (31.55, 74.35), (30.63, 71.96)],
    "Sutlej River": [(31.10, 77.16), (30.66, 74.35), (29.34, 71.68)],
    "Kabul River": [(34.42, 70.45), (33.99, 71.47), (33.90, 72.14)],
    "Swat River": [(35.22, 72.45), (34.75, 72.35), (34.18, 72.08)],
    "Gilgit River": [(36.20, 74.20), (35.92, 74.31)],
    "Hunza River": [(36.55, 74.90), (35.92, 74.31)],
    "Shyok River": [(35.30, 76.90), (35.10, 76.10)],
    "Zhob River": [(31.34, 69.45), (32.05, 69.75)],
    "Bolan River": [(29.05, 67.00), (28.70, 67.55)],
    "Hingol River": [(26.20, 65.85), (25.40, 65.45)],
    "Dasht River": [(26.10, 63.30), (25.10, 61.75)],
    "Shigar River": [(35.75, 76.05), (35.33, 75.68)],
    "Kurram River": [(33.70, 70.10), (33.00, 70.70), (32.58, 71.10)],
    "Gomal River": [(31.90, 69.30), (31.83, 70.90)],
    "Nelum River": [(34.80, 74.50), (34.45, 73.95), (34.37, 73.47)],
    "Poonch River": [(33.77, 74.10), (33.35, 73.75), (33.13, 73.64)],
    "Punjnad River": [(29.24, 71.07), (28.90, 70.42)],
    "Hub River": [(25.75, 67.20), (24.90, 66.90)],
    "Soan River": [(33.60, 73.25), (33.20, 72.70), (32.97, 71.55)],
    "Haro River": [(34.05, 72.90), (33.77, 72.24)],
    "Korang River": [(33.75, 73.15), (33.60, 73.25)],
    "Mula River": [(27.80, 66.65), (28.20, 67.40)],
    "Gaj River": [(26.60, 67.10), (26.85, 67.45)],
    "Kunhar River": [(34.90, 73.65), (34.55, 73.35), (34.37, 73.47)],
    "Tawi River": [(32.73, 74.87), (32.50, 74.53)],
    "Manawar Tawi River": [(32.60, 75.30), (32.28, 75.17)],
    "Tochi River (Gambila River)": [(33.10, 69.70), (32.98, 70.60)],
    "Chitral River (Kunar River)": [(36.00, 71.85), (35.85, 71.79), (34.88, 71.17)],
    "River Jindi (Kot & Manzari Baba)": [(34.35, 73.20), (34.25, 73.15)],
    "Panjkora River": [(35.40, 72.00), (34.68, 71.80)],
    "Bara River": [(33.95, 71.25), (34.02, 71.55)],
    "Lutkho River (Garam Chashma River)": [(35.95, 71.65), (35.85, 71.79)],
    "Siran River (Sirin River)": [(34.40, 73.30), (34.10, 72.85)],
    "Tangir River": [(35.50, 73.60), (35.42, 73.90)],
    "Astore River": [(35.10, 74.90), (35.57, 74.72)],
    "Rupal River": [(35.22, 74.65), (35.15, 74.80)],
    "Naltar River": [(36.20, 74.10), (36.05, 74.37)],
    "Hispar River": [(36.10, 75.15), (36.17, 74.80)],
    "Shimshal River (Shingshal River)": [(36.47, 75.50), (36.42, 74.90)],
    "Chapursan River": [(36.90, 74.15), (36.72, 74.65)],
    "Misga River": [(36.85, 74.70), (36.78, 74.68)],
    "Khunjerab River": [(36.85, 75.43), (36.72, 74.90)],
    "Ishkumhan River": [(36.45, 73.55), (36.17, 73.45)],
    "Yasin River": [(36.40, 73.10), (36.17, 73.45)],
    "Satpara Stream (Satpar Cho)": [(35.20, 75.65), (35.30, 75.63)],
    "Braldu River": [(35.73, 76.30), (35.75, 76.05)],
    "Saltoro River": [(35.45, 76.70), (35.30, 76.90)],
    "Hushe River": [(35.42, 76.45), (35.33, 76.33)],
    "Shingo River": [(34.95, 76.10), (35.10, 75.85)],
    "Rakshan River": [(28.40, 64.20), (28.10, 63.60)],
    "Beji River": [(27.95, 66.75), (27.60, 66.90)],
    "Anambar River": [(30.35, 68.65), (30.60, 69.45)],
    "Loralai River": [(30.37, 68.60), (30.35, 68.65)],
    "Loe Manda River": [(31.30, 69.30), (31.35, 69.50)],
    "Hakra River": [(29.20, 72.90), (28.60, 71.70)],
}

DAM_COORDS = {
    "Tarbela Dam": {"lat": 34.09, "lon": 72.70, "province": "KPK", "river": "Indus River"},
    "Mangla Dam": {"lat": 33.13, "lon": 73.64, "province": "AJK", "river": "Jhelum River"},
    "Diamer-Bhasha Dam": {"lat": 35.52, "lon": 73.80, "province": "GB/KPK border", "river": "Indus River"},
    "Warsak Dam": {"lat": 34.20, "lon": 71.35, "province": "KPK", "river": "Kabul River"},
    "Chashma Barrage": {"lat": 32.43, "lon": 71.37, "province": "Punjab", "river": "Indus River"},
    "Taunsa Barrage": {"lat": 30.70, "lon": 70.65, "province": "Punjab", "river": "Indus River"},
    "Guddu Barrage": {"lat": 28.40, "lon": 69.71, "province": "Sindh", "river": "Indus River"},
    "Sukkur Barrage": {"lat": 27.70, "lon": 68.85, "province": "Sindh", "river": "Indus River"},
    "Kotri Barrage": {"lat": 25.37, "lon": 68.31, "province": "Sindh", "river": "Indus River"},
    "Marala Headworks": {"lat": 32.68, "lon": 74.46, "province": "Punjab", "river": "Chenab River"},
    "Rasul Barrage": {"lat": 32.68, "lon": 73.53, "province": "Punjab", "river": "Jhelum River"},
    "Trimmu Barrage": {"lat": 31.00, "lon": 72.15, "province": "Punjab", "river": "Chenab River"},
    "Panjnad Barrage": {"lat": 29.35, "lon": 70.90, "province": "Punjab", "river": "Panjnad River"},
    "Karot Hydropower Project": {"lat": 33.45, "lon": 73.47, "province": "Punjab/AJK", "river": "Jhelum River"},
    "Suki Kinari Hydropower Station": {"lat": 34.90, "lon": 73.50, "province": "KPK", "river": "Kunhar River"},
    "Kohala Hydropower Project": {"lat": 34.28, "lon": 73.43, "province": "KPK/AJK", "river": "Jhelum River"},
    "Azad Pattan Hydropower Project": {"lat": 33.90, "lon": 73.57, "province": "AJK", "river": "Jhelum River"},
    "Dasu Hydropower Project": {"lat": 35.30, "lon": 73.20, "province": "KPK", "river": "Indus River"},
    "Mohmand Dam": {"lat": 34.67, "lon": 71.73, "province": "KPK", "river": "Swat River"},
    "Kurram Tangi Dam Project": {"lat": 32.95, "lon": 70.10, "province": "KPK", "river": "Kurram River"},
    "Nai Gaj Dam": {"lat": 26.85, "lon": 67.45, "province": "Sindh", "river": "Gaj River"},
    "Naulong Storage Dam": {"lat": 28.35, "lon": 67.55, "province": "Balochistan", "river": "Mula River"},
    "Sabak Zai Dam": {"lat": 31.35, "lon": 69.50, "province": "Balochistan", "river": "Zhob River"},
    "Punjnad Barrage": {"lat": 29.35, "lon": 70.90, "province": "Punjab", "river": "Panjnad River"},
    "Islam Barrage": {"lat": 29.83, "lon": 72.55, "province": "Punjab", "river": "Sutlej River"},
    "Sulemanki Barrage": {"lat": 30.53, "lon": 73.88, "province": "Punjab", "river": "Sutlej River"},
    "Sidhnai Barrage": {"lat": 30.65, "lon": 72.13, "province": "Punjab", "river": "Ravi River"},
    "Balloki Barrage/Headworks": {"lat": 31.20, "lon": 73.85, "province": "Punjab", "river": "Ravi River"},
    "Qadirabad Barrage": {"lat": 32.36, "lon": 73.68, "province": "Punjab", "river": "Chenab River"},
    "Khanki Barrage": {"lat": 32.58, "lon": 74.13, "province": "Punjab", "river": "Chenab River"},
    "Marala Barrage/Headworks": {"lat": 32.68, "lon": 74.46, "province": "Punjab", "river": "Chenab River"},
    "Jinnah Barrage": {"lat": 32.97, "lon": 71.55, "province": "Punjab", "river": "Indus River"},
    "Nowshera Headworks": {"lat": 34.02, "lon": 71.98, "province": "KPK", "river": "Kabul River"},
}

MOUNTAIN_PEAK_COORDS = {
    "K2 (Karakoram)": {"lat": 35.8825, "lon": 76.5133, "elevation_m": 8611},
    "Nanga Parbat (Himalaya)": {"lat": 35.2372, "lon": 74.5892, "elevation_m": 8126},
    "Tirich Mir (Hindu Kush)": {"lat": 36.2531, "lon": 71.8372, "elevation_m": 7708},
    "Koh-e-Bandaka (Hindu Raj)": {"lat": 36.14, "lon": 72.60, "elevation_m": 6812},
    "Sikaram (Spin Ghar)": {"lat": 33.92, "lon": 69.98, "elevation_m": 4761},
    "Takht-e-Sulaiman": {"lat": 31.75, "lon": 70.06, "elevation_m": 3487},
    "Zardak (Kirthar Range)": {"lat": 26.90, "lon": 67.10, "elevation_m": 2168},
    "Khalifat Peak (Toba Kakar)": {"lat": 30.60, "lon": 67.60, "elevation_m": 3487},
    "Sakesar (Salt Range)": {"lat": 32.68, "lon": 71.93, "elevation_m": 1522},
}

LAKE_COORDS = {
    "Attabad Lake": {"lat": 36.34, "lon": 74.87, "province": "Gilgit-Baltistan"},
    "Satpara Lake": {"lat": 35.20, "lon": 75.62, "province": "Gilgit-Baltistan"},
    "Rush Lake": {"lat": 36.05, "lon": 74.65, "province": "Gilgit-Baltistan"},
    "Ghizer Lake (Taalidass)": {"lat": 36.15, "lon": 73.55, "province": "Gilgit-Baltistan"},
    "Saif-ul-Malook Lake": {"lat": 34.88, "lon": 73.69, "province": "KPK"},
    "Kachura Lake": {"lat": 35.47, "lon": 75.42, "province": "Gilgit-Baltistan"},
    "Manchar Lake": {"lat": 26.40, "lon": 67.65, "province": "Sindh"},
    "Keenjhar Lake": {"lat": 24.96, "lon": 68.10, "province": "Sindh"},
    "Hanna Lake": {"lat": 30.28, "lon": 67.05, "province": "Balochistan"},
    "Hub Dam Lake": {"lat": 25.20, "lon": 67.30, "province": "Sindh/Balochistan"},
    "Khanpur Lake": {"lat": 33.82, "lon": 72.98, "province": "ICT/KPK"},
    "Banjosa Lake": {"lat": 33.71, "lon": 73.75, "province": "AJK"},
}

# Rough boundary centroids used for simple choropleth-style bubble maps
PROVINCE_CENTROIDS = {k: (v["lat"], v["lon"]) for k, v in PROVINCE_COORDS.items()}

# ---------------------------------------------------------------------------
# Deserts: representative centroid points, plus a rough multi-point outline
# per desert so it can be drawn as a shaded extent on the map.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Indus Delta soil-salinity survey sample sites (Thatta/Sujawal/Badin
# districts) — see data_loader.INDUS_DELTA_SAMPLE_SITES.
# ---------------------------------------------------------------------------
INDUS_DELTA_SITE_COORDS = {
    "Keti Bandar": {"lat": 24.1400, "lon": 67.4500},
    "Kharo Chan": {"lat": 24.0500, "lon": 67.3500},
    "Shah Bandar": {"lat": 24.1300, "lon": 67.9000},
    "Sujawal (town)": {"lat": 24.5300, "lon": 68.0800},
    "Jati": {"lat": 24.3500, "lon": 68.2700},
    "Thatta (town)": {"lat": 24.7500, "lon": 67.9200},
    "Badin": {"lat": 24.6500, "lon": 68.8400},
}

DESERT_COORDS = {
    "Thar Desert (Great Indian Desert)": {"lat": 25.00, "lon": 70.20, "province": "Sindh"},
    "Cholistan Desert (Rohi)": {"lat": 29.10, "lon": 71.90, "province": "Punjab"},
    "Kharan Desert": {"lat": 28.58, "lon": 65.42, "province": "Balochistan"},
    "Thal Desert": {"lat": 31.20, "lon": 71.50, "province": "Punjab"},
    "Katpana Cold Desert": {"lat": 35.28, "lon": 75.60, "province": "Gilgit-Baltistan"},
}

# Rough bounding outlines (lat, lon) for shading each desert's approximate
# extent on the map — illustrative polygons, not survey boundaries.
DESERT_OUTLINES = {
    "Thar Desert (Great Indian Desert)": [
        (25.90, 69.00), (25.90, 71.10), (24.10, 71.10), (24.10, 69.00), (25.90, 69.00),
    ],
    "Cholistan Desert (Rohi)": [
        (29.90, 70.80), (29.90, 73.00), (28.20, 73.00), (28.20, 70.80), (29.90, 70.80),
    ],
    "Kharan Desert": [
        (29.60, 63.80), (29.60, 66.80), (27.30, 66.80), (27.30, 63.80), (29.60, 63.80),
    ],
    "Thal Desert": [
        (32.20, 70.70), (32.20, 72.10), (30.30, 72.10), (30.30, 70.70), (32.20, 70.70),
    ],
}

# ---------------------------------------------------------------------------
# Additional headworks (not already in DAM_COORDS) needed for link-canal lines
# ---------------------------------------------------------------------------
HEADWORKS_COORDS = {
    "Sidhnai Barrage": {"lat": 30.65, "lon": 72.13, "province": "Punjab", "river": "Ravi River"},
    "Balloki Headworks": {"lat": 31.20, "lon": 73.85, "province": "Punjab", "river": "Ravi River"},
    "Sulemanki Headworks": {"lat": 30.53, "lon": 73.88, "province": "Punjab", "river": "Sutlej River"},
    "Islam Headworks": {"lat": 29.83, "lon": 72.55, "province": "Punjab", "river": "Sutlej River"},
    "Qadirabad Barrage": {"lat": 32.36, "lon": 73.68, "province": "Punjab", "river": "Chenab River"},
    "Bahawal (Mailsi) Link Node": {"lat": 29.80, "lon": 72.18, "province": "Punjab", "river": "Sutlej River"},
}

# ---------------------------------------------------------------------------
# Link canals: approximate start/end coordinates (source barrage -> destination
# barrage/headworks) for drawing them as connecting lines on a real map.
# ---------------------------------------------------------------------------
LINK_CANAL_LINES = {
    "Chashma-Jhelum (C-J) Link Canal": [(32.43, 71.37), (31.00, 72.15)],       # Chashma -> Trimmu (Jhelum arm)
    "Taunsa-Panjnad (T-P) Link Canal": [(30.70, 70.65), (29.35, 70.90)],       # Taunsa -> Panjnad
    "Trimmu-Sidhnai (T-S) Link Canal": [(31.00, 72.15), (30.65, 72.13)],       # Trimmu -> Sidhnai
    "Sidhnai-Mailsi-Bahawal (SMB) Link Canal": [(30.65, 72.13), (29.80, 72.18)],  # Sidhnai -> Bahawal node
    "Mailsi-Bahawal (MB) Link Canal": [(29.80, 72.18), (29.35, 70.90)],        # Bahawal node -> Panjnad zone
    "Rasul-Qadirabad (R-Q) Link Canal": [(32.68, 73.53), (32.36, 73.68)],      # Rasul -> Qadirabad
    "Qadirabad-Balloki (Q-B) Link Canal": [(32.36, 73.68), (31.20, 73.85)],    # Qadirabad -> Balloki
    "Balloki-Sulemanki (B-S) Link Canal": [(31.20, 73.85), (30.53, 73.88)],    # Balloki -> Sulemanki
}

# ---------------------------------------------------------------------------
# Climatic regions: representative points drawn from CLIMATIC_REGIONS["areas"]
# ---------------------------------------------------------------------------
CLIMATE_REGION_POINTS = {
    "Temperate": [
        {"label": "Northern KPK valleys (Swat/Kaghan)", "lat": 34.90, "lon": 72.45},
        {"label": "Islamabad / Margalla foothills", "lat": 33.70, "lon": 73.10},
        {"label": "AJK mid-elevations (Muzaffarabad)", "lat": 34.37, "lon": 73.47},
    ],
    "Tropical": [
        {"label": "Karachi coastal belt", "lat": 24.86, "lon": 67.01},
        {"label": "Thatta coastal zone", "lat": 24.75, "lon": 67.92},
    ],
    "Polar": [
        {"label": "Karakoram glaciated zone (Baltoro/Siachen area)", "lat": 35.70, "lon": 76.30},
        {"label": "Himalaya glaciated zone (Nanga Parbat massif)", "lat": 35.24, "lon": 74.59},
    ],
    "Arid": [
        {"label": "Central Balochistan (Quetta plains)", "lat": 29.50, "lon": 66.50},
        {"label": "Southern Punjab (Bahawalpur/Multan)", "lat": 29.95, "lon": 71.75},
        {"label": "Sindh interior / Thar Desert", "lat": 25.70, "lon": 70.10},
    ],
    "Highland": [
        {"label": "Gilgit-Baltistan valleys (Gilgit/Skardu)", "lat": 35.60, "lon": 74.60},
        {"label": "Quetta plateau", "lat": 30.18, "lon": 66.99},
        {"label": "Northern KPK mountains (Chitral)", "lat": 35.85, "lon": 71.79},
    ],
}

# ---------------------------------------------------------------------------
# Geo-political & strategic domain reference points
# ---------------------------------------------------------------------------
GEOPOLITICAL_COORDS = {
    "Kishenganga Dam (India, upstream of Neelum-Jhelum)": {"lat": 34.36, "lon": 74.85, "type": "Indian upstream project"},
    "Baglihar Dam (India, Chenab)": {"lat": 33.20, "lon": 75.13, "type": "Indian upstream project"},
    "Marala Headworks (Pakistan, Chenab entry point)": {"lat": 32.68, "lon": 74.46, "type": "Pakistan headworks"},
    "Neelum-Jhelum Hydropower Project (Pakistan, AJK)": {"lat": 34.28, "lon": 73.68, "type": "Pakistan hydropower"},
    "Karachi Port": {"lat": 24.82, "lon": 66.98, "type": "Maritime trade infrastructure"},
    "Port Qasim": {"lat": 24.75, "lon": 67.35, "type": "Maritime trade infrastructure"},
    "Gwadar Port (CPEC)": {"lat": 25.13, "lon": 62.33, "type": "Maritime trade infrastructure"},
    "Srinagar (Kashmir Valley, upstream context)": {"lat": 34.08, "lon": 74.80, "type": "Regional context"},
}

# ---------------------------------------------------------------------------
# India's upstream dam-design dispute projects (Chenab tributaries, J&K)
# ---------------------------------------------------------------------------
INDIA_DISPUTED_DAM_COORDS = {
    "Pakal Dul Dam (India)": {"lat": 33.36, "lon": 75.77, "river": "Marusudar River (Chenab tributary)", "capacity_MW": 1000},
    "Ratle Dam (India)": {"lat": 33.15, "lon": 75.75, "river": "Chenab River", "capacity_MW": 850},
}

# ---------------------------------------------------------------------------
# China / CPEC hydropower portfolio — subset of DAM_COORDS for a dedicated map
# ---------------------------------------------------------------------------
CPEC_HYDROPOWER_NAMES = [
    "Karot Hydropower Project",
    "Suki Kinari Hydropower Station",
    "Kohala Hydropower Project",
    "Azad Pattan Hydropower Project",
]

# ---------------------------------------------------------------------------
# Historical disaster events — approximate epicenter / worst-affected point
# ---------------------------------------------------------------------------
HISTORICAL_EVENT_COORDS = {
    "Quetta Earthquake": {"lat": 30.18, "lon": 66.99, "year": 1935},
    "Makran Tsunami": {"lat": 24.80, "lon": 63.40, "year": 1945},
    "Kashmir Earthquake": {"lat": 34.36, "lon": 73.47, "year": 2005},
    "Attabad Lake Landslide & Outburst Risk": {"lat": 36.34, "lon": 74.87, "year": 2010},
    "2010 Pakistan Floods": {"lat": 29.50, "lon": 68.50, "year": 2010},
    "2022 Pakistan Floods": {"lat": 27.50, "lon": 68.20, "year": 2022},
    "Taalidass / Ghizer Lake Event": {"lat": 36.15, "lon": 73.55, "year": 2025},
}

# ---------------------------------------------------------------------------
# River confluence points — approximate lat/lon where named confluences occur
# ---------------------------------------------------------------------------
CONFLUENCE_COORDS = {
    "Kabul River \u2192 Indus River (near Attock)": {"lat": 33.88, "lon": 72.24},
    "Panjnad confluence (Jhelum+Chenab+Ravi+Sutlej \u2192 Indus, near Mithankot)": {"lat": 28.98, "lon": 70.45},
    "Gilgit & Hunza rivers \u2192 Indus (near Bunji)": {"lat": 35.66, "lon": 74.63},
    "Jhelum \u2192 Chenab (near Trimmu)": {"lat": 31.00, "lon": 72.15},
    "Ravi \u2192 Chenab (Ahmadpur Sial)": {"lat": 30.90, "lon": 71.90},
    "Swat \u2192 Kabul River (Charsadda)": {"lat": 34.15, "lon": 71.74},
    "Hunza \u2192 Gilgit River (near Gilgit town)": {"lat": 35.92, "lon": 74.31},
}

# ---------------------------------------------------------------------------
# Notable forests — representative point locations
# ---------------------------------------------------------------------------
NOTABLE_FOREST_COORDS = {
    "Changa Manga Forest": {"lat": 31.083, "lon": 73.967, "province": "Punjab"},
    "Ziarat Juniper Forest": {"lat": 30.363, "lon": 68.158, "province": "Balochistan"},
    "Ushu Forest": {"lat": 35.62, "lon": 72.62, "province": "Khyber Pakhtunkhwa"},
    "Dir Forest (Kumrat Valley)": {"lat": 35.34, "lon": 72.02, "province": "Khyber Pakhtunkhwa"},
    "Soon Valley Forest": {"lat": 32.50, "lon": 71.90, "province": "Punjab"},
    "Mukshpuri Forest": {"lat": 34.08, "lon": 73.40, "province": "Khyber Pakhtunkhwa"},
    "Rama Meadows Forest": {"lat": 35.35, "lon": 74.65, "province": "Gilgit-Baltistan"},
    "Kalam Forest": {"lat": 35.486, "lon": 72.579, "province": "Khyber Pakhtunkhwa"},
    "Chitral Forests": {"lat": 35.933, "lon": 71.667, "province": "Khyber Pakhtunkhwa"},
    "Margalla Hills Scrub Forests": {"lat": 33.731, "lon": 72.937, "province": "Islamabad Capital Territory"},
}

# ---------------------------------------------------------------------------
# National parks & major recreational parks — representative point locations
# ---------------------------------------------------------------------------
NATIONAL_PARK_COORDS = {
    "Ayub National Park": {"lat": 33.60, "lon": 73.07, "province": "Punjab"},
    "Jallo Park, Lahore": {"lat": 31.5725, "lon": 74.47722, "province": "Punjab"},
    "Lulusar-Dudipatsar National Park": {"lat": 34.90, "lon": 73.85, "province": "Khyber Pakhtunkhwa"},
    "Lal Suhanra National Park": {"lat": 29.317, "lon": 71.917, "province": "Punjab"},
    "Kirthar National Park": {"lat": 25.700, "lon": 67.583, "province": "Sindh"},
    "Khunjerab National Park": {"lat": 36.40, "lon": 75.40, "province": "Gilgit-Baltistan"},
    "City Park, Multan": {"lat": 30.1575, "lon": 71.5249, "province": "Punjab"},
    "Kashmir Park, DHA Multan": {"lat": 30.20, "lon": 71.48, "province": "Punjab"},
    "Chitral Gol National Park": {"lat": 35.933, "lon": 71.667, "province": "Khyber Pakhtunkhwa"},
    "Chaman Zar-e-Askari Park, Multan": {"lat": 30.1978, "lon": 71.4696, "province": "Punjab"},
    "Jinnah Park": {"lat": 33.71, "lon": 73.05, "province": "Islamabad Capital Territory"},
    "Hingol National Park": {"lat": 25.50, "lon": 65.40, "province": "Balochistan"},
    "Shakarparian National Park": {"lat": 33.696, "lon": 73.076, "province": "Islamabad Capital Territory"},
    "Faisal Park, Mumtazabad": {"lat": 30.15, "lon": 71.52, "province": "Punjab"},
    "Pir Lasura National Park": {"lat": 33.28, "lon": 74.06, "province": "Azad Jammu & Kashmir"},
    "Hazarganji-Chiltan National Park": {"lat": 30.22, "lon": 66.73, "province": "Balochistan"},
    "Pakistan Park": {"lat": 31.52, "lon": 74.36, "province": "Punjab"},
    "Machiara National Park": {"lat": 34.53, "lon": 73.63, "province": "Azad Jammu & Kashmir"},
    "Rajana Forest / Bhagat Wildlife Park": {"lat": 30.87, "lon": 72.53, "province": "Punjab"},
    "Margalla Hills National Park": {"lat": 33.731, "lon": 72.937, "province": "Islamabad Capital Territory"},
}

# ---------------------------------------------------------------------------
# WAPDA telemetry network — Western Rivers (HF Radio) fallback coordinates
# ---------------------------------------------------------------------------
# The source deployment list for the HF Radio Network (Western Rivers) gives
# facility names only, with no surveyed lat/lon. These are approximate
# nearest-town/city coordinates for visualization purposes only — NOT
# surveyed station coordinates. Two entries are administrative offices
# rather than field stations and are approximated to WAPDA's Lahore HQ area;
# they are flagged accordingly in telemetry_network.py / the app UI.
TELEMETRY_FALLBACK_COORDS = {
    "Mangla Dam": {"lat": 33.13, "lon": 73.64},
    "Tarbela Dam": {"lat": 34.09, "lon": 72.70},
    "Besham": {"lat": 34.92, "lon": 72.87},
    "Jaglot": {"lat": 35.80, "lon": 74.55},
    "Skardu": {"lat": 35.30, "lon": 75.63},
    "Daggar": {"lat": 34.52, "lon": 72.43},
    "Phulra": {"lat": 34.75, "lon": 73.10},
    "Oghi": {"lat": 34.58, "lon": 73.05},
    "Shinkiari": {"lat": 34.47, "lon": 73.28},
    "Khairabad": {"lat": 33.90, "lon": 72.17},
    "Nowshera": {"lat": 34.02, "lon": 71.98},
    "Kallar": {"lat": 33.84, "lon": 73.86},
    "G. Habibullah": {"lat": 34.17, "lon": 73.57},
    "Muzaffarabad": {"lat": 34.37, "lon": 73.47},
    "Domel": {"lat": 34.37, "lon": 73.46},
    "Kotli": {"lat": 33.52, "lon": 73.90},
    "Kohala": {"lat": 34.17, "lon": 73.44},
    "Plandri": {"lat": 33.72, "lon": 73.68},
    "Azadpatan": {"lat": 34.00, "lon": 73.47},
    "Chashma Barrage": {"lat": 32.43, "lon": 71.37},
    "Water Resource Management Directorate": {"lat": 31.56, "lon": 74.33},
    "Central Flood Forecasting Division": {"lat": 31.56, "lon": 74.33},
}
TELEMETRY_FALLBACK_NOTE = (
    "Western Rivers (HF Radio) station coordinates are approximate "
    "nearest-town/city positions, not surveyed coordinates — the source "
    "deployment list gives facility names only. 'Water Resource Management "
    "Directorate' and 'Central Flood Forecasting Division' are administrative "
    "offices, approximated to the Lahore area, not field gauging sites."
)

CONFLUENCE_COORDS = {
    "Trimmu Confluence (Jhelum & Chenab)": {"lat": 31.00, "lon": 72.15},
    "Ahmedpur Sial Confluence (Ravi & Chenab)": {"lat": 30.65, "lon": 71.88},
    "Uch Sharif / Panjnad Confluence (Sutlej & Chenab)": {"lat": 29.24, "lon": 71.07},
    "Mithankot Confluence (Panjnad & Indus)": {"lat": 28.90, "lon": 70.42},
    "Attock Confluence (Kabul & Indus)": {"lat": 33.77, "lon": 72.24},
    "Jaglot / Bunji Confluence (Gilgit & Indus)": {"lat": 35.65, "lon": 74.58},
    "Muzaffarabad Confluence (Neelum & Jhelum)": {"lat": 34.37, "lon": 73.47},
    "Swat & Kabul River Confluence": {"lat": 34.17, "lon": 71.74},
    "Shyok & Indus River Confluence": {"lat": 35.28, "lon": 75.80},
    "Hunza & Gilgit River Confluence": {"lat": 35.92, "lon": 74.31},
}
