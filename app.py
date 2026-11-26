"""
app.py
Pakistan Water, Terrain & Disaster-Risk Explorer
A Streamlit dashboard covering provinces, rivers, dams/barrages, link canals,
climatic regions, mountain ranges, national disaster-risk context, lakes,
deserts, forests, national parks, socio-economic & agro-economic domains, and
the geo-political / strategic water dimension (Indus Waters Treaty,
inter-provincial disputes, CPEC hydropower investment, and India's upstream
dam-design disputes).

Created by Engr. Syed Hassan Iqbal Shah (ELECT/28314).

Run with:  streamlit run app.py
"""

import base64
import os

import streamlit as st
import pandas as pd
import plotly.express as px

import data_loader as data
import map_view
import network_view
import hydraulic_model as hm
import file_import
import telemetry_engine
import water_quality_engine
import telemetry_network as telnet
import coordinates as coords
import india_hydropower_cea as cea
import sebal_engine as sebal
import flag_assets
import army_role
import energy_minerals as em
import interactive_kit as kit
import crew_agents
import gov_logos
import army_emblems
import security_bodies
import agents_ui
import navy_role
import potohar_irrigation
import indus_plain
import sebal_validation
import irrigation_shortfall
import gov_logos

# Resolve asset paths relative to this file's own directory, not the process's
# current working directory — Streamlit Cloud (and some other hosts) don't
# guarantee cwd == the app's own folder, which silently breaks a bare
# "assets/..." relative path even when the file was committed correctly.
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def asset_path(*parts: str) -> str:
    """Build an absolute path to a bundled asset (e.g. an infographic PNG)."""
    return os.path.join(APP_DIR, *parts)


def render_interactive_image(path: str, title: str = "", height: int = 520):
    """Render a PNG as a Plotly figure with scroll-wheel/pinch zoom and
    drag-to-pan — the same 'Google-Earth-like' interaction used for every map
    in this app — instead of a static st.image. Raises if the file can't be
    opened, so callers can fall back to a clear 'not found' message."""
    from PIL import Image

    img = Image.open(path)
    fig = px.imshow(img)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_layout(
        title=title,
        margin=dict(l=0, r=0, t=36 if title else 0, b=0),
        height=height,
        dragmode="pan",
    )
    return fig


st.set_page_config(
    page_title="Pakistan Water & Terrain Explorer",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
SECTIONS = [
    "🏠 Overview",
    "🗺️ Provinces",
    "🌊 Rivers",
    "🌾 Indus Plain: Geography, Doabs, Salinity & Cropping",
    "🚧 Dams & Barrages",
    "💧 Potohar Dams, Irrigation Budget & Flooding Guide",
    "🚰 Causes of Irrigation Water Shortfall in Pakistan",
    "🔀 Link Canals",
    "📡 WAPDA Telemetry Network",
    "🌡️ Climatic Regions",
    "⛰️ Mountain Ranges",
    "🏞️ Lakes",
    "🏜️ Deserts",
    "🌲 Forests",
    "🌳 National Parks",
    "🧂 Indus Delta Soil Salinity (EMI Survey)",
    "⚠️ Disaster Risk Context",
    "📈 Socio-Economic & Agro-Economic",
    "🗺️ Geo-Political & Strategic",
    "🇨🇳 China Hydropower (CPEC)",
    "🇮🇳 Chenab Projects, Flow Concerns & Indus Waters Treaty",
    "🧮 Interactive Hydraulic Models",
    "🛰️ SEBAL Evapotranspiration Engine",
    "📤 Upload File → Map, Charts & Analytics",
    "🪖 Pakistan Army's Role Across Sectors",
    "⚓ Pakistan Navy's Role Across This Project's Sectors",
    "☀️ Solar Energy Sectors",
    "⛏️ Mining Sectors",
    "🥜 Dry Fruit Sector",
    "🤖 CrewAI Sector Agents",
    "🤖 AI Agents (CrewAI)",
    "🔎 Search Everything",
    "📚 Sources",
]

st.sidebar.title("🇵🇰 Navigation")
_find = st.sidebar.text_input("🔎 Find a section", value="", key="nav_find", placeholder="e.g. solar, dams, army…")
_nav = [s_ for s_ in SECTIONS if _find.strip().lower() in s_.lower()] if _find.strip() else SECTIONS
if not _nav:
    st.sidebar.caption("No section matches — showing all.")
    _nav = SECTIONS
choice = st.sidebar.radio("Go to section", _nav, label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption(
    "Educational dashboard. Figures are curated summaries — verify against "
    "WAPDA, IRSA, PMD, NDMA/PDMA and the Indus Waters Treaty text before "
    "using in formal reports."
)

if gov_logos.LOGOS:
    st.markdown(gov_logos.strip_html(), unsafe_allow_html=True)
st.caption(gov_logos.DISCLAIMER)



# Government / department logo strip: every image dropped into the logos/ folder
# is shown on every page (file name = caption). Empty folder -> nothing is shown.
def _logo_strip_html():
    folder = os.path.join(APP_DIR, "logos")
    try:
        names = sorted(f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    except Exception:
        return ""
    cells = []
    for f in names:
        try:
            with open(os.path.join(folder, f), "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode()
        except Exception:
            continue
        ext = f.rsplit(".", 1)[-1].lower()
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        cap = os.path.splitext(f)[0]
        cap = cap.split("_", 1)[1] if cap[:2].isdigit() and "_" in cap else cap
        cap = cap.replace("_", " ")
        cells.append(
            '<div style="text-align:center;width:92px;">'
            f'<img src="data:{mime};base64,{b64}" style="height:58px;width:auto;max-width:90px;object-fit:contain;" />'
            f'<div style="font-size:10px;line-height:1.1;margin-top:2px;">{cap}</div></div>'
        )
    if not cells:
        return ""
    return (
        '<div style="display:flex;flex-wrap:wrap;gap:10px;align-items:flex-start;margin:6px 0 2px 0;">'
        + "".join(cells) + "</div>"
        '<div style="font-size:11px;opacity:.7;">Educational project — not an official government '
        'publication; logos are shown for reference/dedication only.</div>'
    )

_strip = _logo_strip_html()
if _strip:
    st.markdown(_strip, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 🏠 OVERVIEW
# ---------------------------------------------------------------------------
if choice == "🏠 Overview":
    st.title("Pakistan Water, Terrain & Disaster-Risk Explorer")
    st.markdown("**Created by Engr. Syed Hassan Iqbal Shah** · PEC: ELECT/28314 · Dedicated to ISPR")
    st.markdown(
        "An interactive reference dashboard covering Pakistan's **provinces**, "
        "**river systems**, **dams/barrages/link canals**, **climatic regions**, "
        "**mountain ranges**, **national disaster-risk context**, **lakes**, and the "
        "**socio-economic, agro-economic and geo-political dimensions** of water "
        "management — including the Indus Waters Treaty, inter-provincial disputes, "
        "CPEC hydropower investment, and India's upstream dam-design disputes."
    )
    st.plotly_chart(map_view.combined_overview_map(), use_container_width=True, config={"scrollZoom": True})

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Provinces / Territories", len(data.PROVINCES))
    col2.metric("Major Rivers Tracked", len(data.RIVERS))
    col3.metric("Dams / Barrages / Hydropower", len(data.DAMS_BARRAGES))
    col4.metric("Link Canals", len(data.LINK_CANALS))

    st.markdown("### What's inside")
    st.markdown(
        "- **Provinces** — Gilgit-Baltistan, KPK, Punjab, Sindh, Balochistan, AJK, ICT\n"
        "- **Rivers** — source, upstream/downstream path, confluences, associated infrastructure\n"
        "- **Dams, Barrages & Link Canals** — the Indus Basin Irrigation System (IBIS)\n"
        "- **Climatic Regions** — Temperate, Tropical, Polar, Arid, Highland\n"
        "- **Mountain Ranges** — Karakoram, Himalayas, Hindu Kush, Hindu Raj, Spin Ghar, "
        "Sulaiman, Kirthar, Toba Kakar, Salt Range — peaks, geology, tourism, climbing\n"
        "- **Deserts** — Thar, Cholistan, Kharan, Thal and the Katpana cold desert, with "
        "approximate mapped extents\n"
        "- **Forests** — main forest types (coniferous, mangrove, riverain, scrub, planted) "
        "and notable forests with history, wildlife and attractions\n"
        "- **National Parks** — Pakistan's national parks and major recreational parks, "
        "with area, establishment and notes\n"
        "- **Indus Delta Soil Salinity** — EMI survey and soil-sampling methodology, FAO "
        "salinity/sodicity classification, and interpolated EC/pH/ESP sample sites\n"
        "- **National Disaster Risk Context** — hazard profile, exposure/vulnerability, "
        "emerging risks (GLOFs, monsoon variability, sea intrusion), risk scenarios\n"
        "- **Socio-Economic & Agro-Economic Domains** — food security, IBIS, GDP linkages, "
        "Rabi/Kharif crop calendar, apiculture and aquaculture\n"
        "- **Geo-Political & Strategic** — Kashmir hydro-politics, IWT, inter-provincial "
        "disputes (Punjab vs Sindh), IRSA/CCI legal mechanisms\n"
        "- **China's CPEC Hydropower Footprint** — Karot, Suki Kinari, Kohala, Azad Pattan\n"
        "- **Chenab Projects, Flow Concerns & Indus Waters Treaty** — Pakal Dul & Ratle "
        "technical contentions, the Head Marala flow issue, and the PCA arbitration timeline\n"
        "- **Interactive Hydraulic Models** — simplified reservoir, shortage-sharing, "
        "link-canal transfer and disaster-risk-index calculators\n"
        "- **Upload File → Map, Charts & Analytics** — bring your own CSV or PDF data and "
        "plot it as a map or a bar/pie/scatter/line chart, or run the built-in river-basin "
        "telemetry-variance and EC/pH/DO water-quality engines\n"
    )
    st.caption(
        "Geopolitical, CPEC and dam-governance content is backed by official sources — "
        "see the **📚 Sources** section in the sidebar."
    )

# ---------------------------------------------------------------------------
# 🗺️ PROVINCES
# ---------------------------------------------------------------------------
elif choice == "🗺️ Provinces":
    st.title("Provinces & Territories of Pakistan")
    st.plotly_chart(map_view.province_overview_map(), use_container_width=True, config={"scrollZoom": True})

    prov_name = st.selectbox("Select a province / territory", list(data.PROVINCES.keys()))
    p = data.PROVINCES[prov_name]
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader(prov_name)
        st.write(p["overview"])
        st.markdown(f"**Major rivers:** {', '.join(p['major_rivers']) or '—'}")
        st.markdown(f"**Major dams / barrages:** {', '.join(p['major_dams_barrages']) or '—'}")
        st.markdown(f"**Climatic regions:** {', '.join(p['climate_regions'])}")
        st.markdown(f"**Mountain ranges:** {', '.join(p['mountain_ranges']) or '—'}")
        st.markdown(f"**Key lakes:** {', '.join(p['key_lakes']) or '—'}")
    with c2:
        st.metric("Capital", p["capital"])
        st.metric("Area (km²)", f"{p['area_km2']:,}")

    st.markdown("### All provinces at a glance")
    df = pd.DataFrame([
        {
            "Province": k,
            "Capital": v["capital"],
            "Area (km²)": v["area_km2"],
            "Major Rivers": ", ".join(v["major_rivers"]),
            "Climatic Regions": ", ".join(v["climate_regions"]),
        }
        for k, v in data.PROVINCES.items()
    ])
    kit.explore(df, key="kit_1")

# ---------------------------------------------------------------------------
# 🌊 RIVERS
# ---------------------------------------------------------------------------
elif choice == "🌊 Rivers":
    st.title("Rivers of Pakistan")

    tab_overview, tab_confluences = st.tabs(["🗺️ Overview & River Details", "🔗 River Confluences"])

    with tab_overview:
        all_rivers = list(data.RIVERS.keys())
        selected = st.multiselect("Filter rivers on the map", all_rivers, default=all_rivers)
        st.plotly_chart(map_view.rivers_map(selected), use_container_width=True, config={"scrollZoom": True})

        river_name = st.selectbox("Select a river for details", all_rivers)
        r = data.RIVERS[river_name]
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(river_name)
            st.markdown(f"**Length:** {r['length_km']} km")
            st.markdown(f"**Source:** {r['source']}")
            st.markdown(f"**Upstream path:** {r['upstream']}")
            st.markdown(f"**Downstream path:** {r['downstream']}")
        with c2:
            st.markdown("**River confluences:**")
            for c in r["confluences"]:
                st.markdown(f"- {c}")
            st.markdown(f"**Provinces traversed:** {', '.join(r['provinces'])}")
            st.markdown(f"**Associated dams/barrages:** {', '.join(r['dams_barrages']) or '—'}")
            if r.get("notes"):
                st.info(r["notes"])

        st.markdown("### River confluence network (schematic)")
        st.plotly_chart(network_view.river_confluence_network(), use_container_width=True, config={"scrollZoom": True})

        st.markdown("### River confluence points (interactive map)")
        st.plotly_chart(map_view.river_confluence_geomap(), use_container_width=True, config={"scrollZoom": True})

    with tab_confluences:
        st.subheader("River Confluences of Pakistan")
        st.caption(
            "Where Pakistan's major rivers physically meet — grouped by the Punjab "
            "plain's \"five waters\" system, the Indus's western/northern tributary "
            "junctions, and smaller mountain confluences."
        )

        conf_points = []
        for group in data.RIVER_CONFLUENCES.values():
            for item in group["confluences"]:
                pt = coords.CONFLUENCE_COORDS.get(item["name"])
                if pt:
                    conf_points.append({
                        "Name": item["name"], "Latitude": pt["lat"], "Longitude": pt["lon"],
                    })
        if conf_points:
            st.plotly_chart(
                map_view.custom_points_map(pd.DataFrame(conf_points), title="River Confluence Points"),
                use_container_width=True, config={"scrollZoom": True}, key="river_confluences_map",
            )

        for group_key, group in data.RIVER_CONFLUENCES.items():
            st.markdown(f"#### {group['group_title']}")
            if group.get("intro"):
                st.markdown(group["intro"])
            for item in group["confluences"]:
                with st.expander(item["name"]):
                    st.markdown(item["description"])
            st.markdown("")

# ---------------------------------------------------------------------------
# 🚧 DAMS & BARRAGES
# ---------------------------------------------------------------------------
elif choice == "🚧 Dams & Barrages":
    st.title("Dams, Barrages & Hydropower Projects")
    all_names = list(data.DAMS_BARRAGES.keys())
    selected = st.multiselect("Filter on the map", all_names, default=all_names)
    st.plotly_chart(map_view.dams_barrages_map(selected), use_container_width=True, config={"scrollZoom": True})

    df = pd.DataFrame([
        {"Name": k, **v} for k, v in data.DAMS_BARRAGES.items()
    ]).rename(columns={
        "type": "Type", "river": "River", "province": "Province",
        "year_completed": "Year Completed", "capacity_MW": "Capacity (MW)", "purpose": "Purpose",
    })
    kit.explore(df, key="kit_2")

    st.markdown("### Irrigation & hydropower network (schematic)")
    st.plotly_chart(network_view.irrigation_network_diagram(), use_container_width=True, config={"scrollZoom": True})

    st.markdown("### Irrigation & hydropower network (interactive map)")
    st.plotly_chart(map_view.irrigation_network_geomap(), use_container_width=True, config={"scrollZoom": True})

    with st.expander("📚 Sources for this section"):
        for ref in data.SOURCES["Dams & Water Governance"] + data.SOURCES["Indus Basin Irrigation System"]:
            st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# 🔀 LINK CANALS
# ---------------------------------------------------------------------------
elif choice == "💧 Potohar Dams, Irrigation Budget & Flooding Guide":
    potohar_irrigation.render()

elif choice == "🌾 Indus Plain: Geography, Doabs, Salinity & Cropping":
    indus_plain.render()

elif choice == "🚰 Causes of Irrigation Water Shortfall in Pakistan":
    irrigation_shortfall.render()

elif choice == "🔀 Link Canals":
    st.title("Link Canals — Indus Basin Irrigation System (IBIS)")
    st.markdown(
        "Link canals move surplus water between rivers to compensate zones "
        "(especially the Ravi and Sutlej commands) whose natural flows were "
        "reduced after the eastern rivers were allocated to India under the "
        "1960 Indus Waters Treaty."
    )
    st.plotly_chart(map_view.link_canals_map(), use_container_width=True, config={"scrollZoom": True})

    for name, info in data.LINK_CANALS.items():
        with st.expander(name):
            st.markdown(f"**Connects:** {info['connects']}")
            st.markdown(f"**Province:** {info['province']}")
            st.markdown(f"**Purpose:** {info['purpose']}")

    with st.expander("📄 Cross-check — WAPDA's official 'Indus Water Treaty (Link Canals & Barrage)' map"):
        ref = data.IWT_MAP_REFERENCE
        st.markdown(f"**{ref['title']}** shows:")
        st.markdown("**Link canals:** " + "; ".join(ref["link_canals_shown"]))
        st.markdown("**Barrages:** " + ", ".join(ref["barrages_shown"]))
        st.markdown("**Rivers:** " + ", ".join(ref["rivers_shown"]))
        st.markdown("**Other features:** " + ", ".join(ref["other_features_shown"]))
        st.caption(ref["source_note"])

# ---------------------------------------------------------------------------
# 📡 WAPDA TELEMETRY NETWORK
# ---------------------------------------------------------------------------
elif choice == "📡 WAPDA Telemetry Network":
    st.title("WAPDA Flood-Forecasting Telemetry Network")
    st.caption(telnet.NETWORK_NOTE)

    st.plotly_chart(
        map_view.telemetry_network_map(
            telnet.EASTERN_RIVERS_WIRELESS_STATIONS, telnet.WESTERN_RIVERS_HF_RADIO_STATIONS
        ),
        use_container_width=True, config={"scrollZoom": True},
    )

    tab_e, tab_w = st.tabs(
        [f"🔵 Eastern Rivers — Wireless Network ({len(telnet.EASTERN_RIVERS_WIRELESS_STATIONS)} sites)",
         f"🔴 Western Rivers — HF Radio Network ({len(telnet.WESTERN_RIVERS_HF_RADIO_STATIONS)} sites)"]
    )
    with tab_e:
        st.markdown(
            "Headworks, barrages, syphons, bridges and nullah gauging sites on the "
            "Ravi/Chenab/Sutlej system — surveyed coordinates as supplied in the source data."
        )
        df_e = pd.DataFrame(telnet.EASTERN_RIVERS_WIRELESS_STATIONS).rename(
            columns={"location": "Location / Facility", "lat": "Latitude", "lon": "Longitude"}
        )
        kit.explore(df_e, key="kit_3")

    with tab_w:
        st.markdown(
            "Dams, barrages and flood-forecasting offices on the Indus/Jhelum system."
        )
        st.info(coords.TELEMETRY_FALLBACK_NOTE)
        df_w = pd.DataFrame(telnet.WESTERN_RIVERS_HF_RADIO_STATIONS).rename(
            columns={"network_area": "Network Area", "facility": "Location / Facility"}
        )
        kit.explore(df_w, key="kit_4")

    with st.expander("📚 Source"):
        st.markdown(f"- {telnet.SOURCE_NOTE}")

# ---------------------------------------------------------------------------
# 🌡️ CLIMATIC REGIONS
# ---------------------------------------------------------------------------
elif choice == "🌡️ Climatic Regions":
    st.title("Climatic Regions of Pakistan")
    st.plotly_chart(map_view.climatic_regions_map(), use_container_width=True, config={"scrollZoom": True})

    cols = st.columns(len(data.CLIMATIC_REGIONS))
    for col, (region, info) in zip(cols, data.CLIMATIC_REGIONS.items()):
        with col:
            st.subheader(region)
            st.markdown(f"**Areas:** {', '.join(info['areas'])}")
            st.caption(info["characteristics"])

    st.markdown("### Which provinces fall in which climatic region?")
    rows = []
    for prov, p in data.PROVINCES.items():
        for region in p["climate_regions"]:
            rows.append({"Province": prov, "Climatic Region": region})
    kit.explore(pd.DataFrame(rows), key="kit_5")

# ---------------------------------------------------------------------------
# ⛰️ MOUNTAIN RANGES
# ---------------------------------------------------------------------------
elif choice == "⛰️ Mountain Ranges":
    st.title("Mountain Ranges of Pakistan")
    st.plotly_chart(map_view.mountains_map(), use_container_width=True, config={"scrollZoom": True})

    for group_name, ranges in data.MOUNTAIN_RANGES.items():
        st.header(group_name)
        range_name = st.selectbox(
            f"Select a range in '{group_name}'", list(ranges.keys()), key=group_name
        )
        r = ranges[range_name]
        st.subheader(range_name)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Highest peak:** {r['highest_peak']}")
            if r.get("other_notable_peaks"):
                st.markdown("**Other notable peaks:**")
                peaks_df = pd.DataFrame(r["other_notable_peaks"]).rename(
                    columns={"name": "Peak", "elevation_m": "Elevation (m)"}
                )
                kit.explore(peaks_df, key=f"kit_6_{group_name}_{range_name}")
            st.markdown(f"**Surrounding areas:** {r['surrounding_areas']}")
            st.markdown(f"**Rivers flowing through / from this range:** {', '.join(r['rivers'])}")
            st.markdown(f"**Access towns:** {', '.join(r.get('access_towns', [])) or '—'}")
        with c2:
            st.markdown(f"**Climbing details:** {r['climbing_details']}")
            st.markdown(f"**Best climbing/trekking season:** {r.get('best_climbing_season', '—')}")
            st.markdown(f"**Permits required:** {r.get('permits_required', '—')}")
            if r.get("trekking_routes"):
                st.markdown("**Popular trekking routes:**")
                for route in r["trekking_routes"]:
                    st.markdown(f"- {route}")
            if r.get("hazards"):
                st.warning(f"**Hazards:** {r['hazards']}")

        st.markdown(f"**Geology:** {r['geology']}")
        st.markdown(f"**Tourist guide:** {r['tourist_guide']}")
        st.markdown("---")

# ---------------------------------------------------------------------------
# 🏞️ LAKES
# ---------------------------------------------------------------------------
elif choice == "🏞️ Lakes":
    st.title("Lakes of Pakistan")
    st.plotly_chart(map_view.lakes_map(), use_container_width=True, config={"scrollZoom": True})
    df = pd.DataFrame([{"Lake": k, **v} for k, v in data.LAKES.items()]).rename(
        columns={"province": "Province", "formation": "Formation", "type": "Type"}
    )
    kit.explore(df, key="kit_7")

# ---------------------------------------------------------------------------
# 🏜️ DESERTS
# ---------------------------------------------------------------------------
elif choice == "🏜️ Deserts":
    st.title("Deserts of Pakistan")
    st.plotly_chart(map_view.deserts_map(), use_container_width=True, config={"scrollZoom": True})

    df = pd.DataFrame([
        {
            "Desert": k,
            "Province": v["province"],
            "Area (km²)": v["area_km2"] if v["area_km2"] else "—",
            "Type": v["type"],
        }
        for k, v in data.DESERTS.items()
    ])
    kit.explore(df, key="kit_8")

    desert_name = st.selectbox("Select a desert for details", list(data.DESERTS.keys()))
    d = data.DESERTS[desert_name]
    st.subheader(desert_name)
    st.markdown(f"**Province:** {d['province']}")
    area_text = f"{d['area_km2']:,} km²" if d["area_km2"] else "Not well-documented (localized dune field)"
    st.markdown(f"**Approximate area:** {area_text}")
    st.markdown(f"**Type:** {d['type']}")
    st.write(d["characteristics"])

# ---------------------------------------------------------------------------
# 🌲 FORESTS
# ---------------------------------------------------------------------------
elif choice == "🌲 Forests":
    st.title("Forests of Pakistan")

    st.header("Main Forest Types")
    for name, info in data.FOREST_TYPES.items():
        with st.expander(name):
            st.markdown(f"**Regions:** {info['regions']}")
            st.markdown(f"**Altitude range:** {info['altitude']}")
            st.markdown(f"**Key species:** {info['species']}")
            st.write(info["notes"])

    st.header("Notable Forests — Map")
    st.plotly_chart(map_view.forests_map(), use_container_width=True, config={"scrollZoom": True})

    st.header("Notable Forests — Details")
    forest_name = st.selectbox("Select a forest for details", list(data.NOTABLE_FORESTS.keys()))
    f = data.NOTABLE_FORESTS[forest_name]
    st.subheader(forest_name)
    st.markdown(f"**Location:** {f['location']}")
    st.markdown(f"**Forest type:** {f['forest_type']}")
    st.markdown(f"**Covered area:** {f['covered_area']}")
    st.markdown("**History & Origin**")
    st.write(f["history_origin"])
    st.markdown("**Wildlife & Nature**")
    st.write(f["wildlife_nature"])
    st.markdown("**Attractions & Recreation**")
    st.write(f["attractions_recreation"])

    with st.expander("See all notable forests in a table"):
        df = pd.DataFrame([
            {"Forest": k, "Location": v["location"], "Type": v["forest_type"], "Covered Area": v["covered_area"]}
            for k, v in data.NOTABLE_FORESTS.items()
        ])
        kit.explore(df, key="kit_9")

# ---------------------------------------------------------------------------
# 🌳 NATIONAL PARKS
# ---------------------------------------------------------------------------
elif choice == "🌳 National Parks":
    st.title("National Parks & Major Recreational Parks of Pakistan")
    st.caption(
        "Not every entry below is an IUCN/provincially-notified national park — several are large municipal "
        "or cantonment recreational parks that are commonly called 'parks' locally. This is noted per entry."
    )
    st.plotly_chart(map_view.national_parks_map(), use_container_width=True, config={"scrollZoom": True})

    df = pd.DataFrame([
        {"Park": k, "Province": v["province"], "Type": v["type"], "Area": v["area"], "Established": v["established"]}
        for k, v in data.NATIONAL_PARKS.items()
    ])
    kit.explore(df, key="kit_10")

    park_name = st.selectbox("Select a park for details", list(data.NATIONAL_PARKS.keys()))
    p = data.NATIONAL_PARKS[park_name]
    st.subheader(park_name)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"**Province / Region:** {p['province']}")
        st.markdown(f"**Type:** {p['type']}")
        st.markdown(f"**Area:** {p['area']}")
        st.markdown(f"**Established:** {p['established']}")
        st.write(p["notes"])
    with c2:
        park_coord = coords.NATIONAL_PARK_COORDS.get(park_name)
        if park_coord:
            st.plotly_chart(
                map_view.single_park_map(park_name, park_coord["lat"], park_coord["lon"]),
                use_container_width=True, config={"scrollZoom": True},
            )
        else:
            st.info("No coordinates available for this park yet.")

# ---------------------------------------------------------------------------
# 🧂 INDUS DELTA SOIL SALINITY (EMI SURVEY)
# ---------------------------------------------------------------------------
elif choice == "🧂 Indus Delta Soil Salinity (EMI Survey)":
    st.title("Indus Delta Soil Salinity — EMI Survey & Soil Sampling")
    s = data.INDUS_DELTA_SOIL_SURVEY
    st.write(s["overview"])
    st.caption(f"Study reference: {s['study_reference']}")

    st.header("🔬 Methodology")
    for step, desc in s["methodology"].items():
        with st.expander(step):
            st.write(desc)

    st.header("📊 Depth-wise Findings — Samples Exceeding FAO Guidelines")
    depth_df = pd.DataFrame([
        {"Depth": depth, "EC exceeding FAO (%)": v["ec_exceeding_fao"], "ESP exceeding FAO (%)": v["esp_exceeding_fao"]}
        for depth, v in s["depth_wise_findings"].items()
    ])
    fig_depth = px.bar(
        depth_df, x="Depth", y=["EC exceeding FAO (%)", "ESP exceeding FAO (%)"],
        barmode="group", title="Share of samples exceeding FAO EC/ESP guidelines, by depth",
    )
    st.plotly_chart(fig_depth, use_container_width=True, config={"scrollZoom": True})
    st.info(s["key_findings"])

    st.header("📏 Salinity / Sodicity Classification (Richards / FAO thresholds)")
    for cls, threshold in s["salinity_sodicity_classification"].items():
        st.markdown(f"**{cls}:** {threshold}")

    st.header("🗺️ Interpolated Sample Sites — EC, pH & ESP")
    st.caption(
        "Illustrative representative sample points across Thatta, Sujawal and Badin districts — "
        "for demonstration, not the original study's raw per-site dataset."
    )
    st.plotly_chart(map_view.indus_delta_soil_map(data.INDUS_DELTA_SAMPLE_SITES), use_container_width=True, config={"scrollZoom": True})

    sites_df = pd.DataFrame(data.INDUS_DELTA_SAMPLE_SITES).rename(columns={
        "site": "Site", "district": "District", "EC_dS_per_m": "EC (dS/m)",
        "pH": "pH", "ESP_pct": "ESP (%)", "classification": "Classification",
    })
    kit.explore(sites_df, key="kit_11")

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(
            px.bar(sites_df, x="Site", y="EC (dS/m)", color="Classification", title="Electrical Conductivity by Site"),
            use_container_width=True, config={"scrollZoom": True},
        )
    with chart_col2:
        st.plotly_chart(
            px.scatter(
                sites_df, x="pH", y="ESP (%)", color="Classification", size="EC (dS/m)",
                hover_name="Site", title="ESP vs. pH (bubble size = EC)",
            ),
            use_container_width=True, config={"scrollZoom": True},
        )

    with st.expander("📚 Sources for this section"):
        for ref in data.SOURCES.get("Indus Delta Soil Salinity", []):
            st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# ⚠️ DISASTER RISK CONTEXT
# ---------------------------------------------------------------------------
elif choice == "⚠️ Disaster Risk Context":
    st.title("National Disaster Risk Context")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["1. Hazard Profile", "2. Exposure & Vulnerability", "3. Emerging Risks",
         "4. Risk Scenarios", "5. Historical Events & Hazard Map"]
    )

    with tab1:
        for category, hazards in data.DISASTER_HAZARD_PROFILE.items():
            st.subheader(category)
            for hazard, detail in hazards.items():
                if isinstance(detail, dict):
                    with st.expander(hazard):
                        for sub, subdetail in detail.items():
                            st.markdown(f"**{sub}:** {subdetail}")
                else:
                    st.markdown(f"**{hazard}:** {detail}")
            st.markdown("---")

    with tab2:
        for factor, detail in data.DISASTER_EXPOSURE_VULNERABILITY.items():
            st.subheader(factor)
            if isinstance(detail, dict):
                if "drivers" in detail:
                    st.markdown(", ".join(detail["drivers"]))
                    st.caption(detail["summary"])
                else:
                    for sub, subdetail in detail.items():
                        st.markdown(f"**{sub}:** {subdetail}")
            else:
                st.write(detail)

    with tab3:
        for topic, detail in data.DISASTER_EMERGING_RISKS.items():
            st.subheader(topic)
            st.write(detail)

    with tab4:
        cols = st.columns(3)
        for col, (scenario, info) in zip(cols, data.DISASTER_RISK_SCENARIOS.items()):
            with col:
                st.subheader(scenario)
                st.write(info["description"])
                for feat in info["features"]:
                    st.markdown(f"- {feat}")

    with tab5:
        st.subheader("Historical Disaster Timeline")
        st.plotly_chart(map_view.historical_events_map(), use_container_width=True, config={"scrollZoom": True})

        hist_df = pd.DataFrame(data.DISASTER_HISTORICAL_EVENTS)
        hist_df["provinces"] = hist_df["provinces"].apply(lambda x: ", ".join(x))
        hist_df = hist_df.rename(columns={
            "year": "Year", "name": "Event", "hazard_type": "Hazard Type",
            "provinces": "Provinces Affected", "summary": "Summary",
        })
        kit.explore(hist_df, key="kit_12")

        year_min, year_max = int(hist_df["Year"].min()), int(hist_df["Year"].max())
        year_range = st.slider("Filter by year", year_min, year_max, (year_min, year_max))
        filtered = hist_df[(hist_df["Year"] >= year_range[0]) & (hist_df["Year"] <= year_range[1])]
        for _, row in filtered.iterrows():
            with st.expander(f"{row['Year']} — {row['Event']} ({row['Hazard Type']})"):
                st.markdown(f"**Provinces affected:** {row['Provinces Affected']}")
                st.write(row["Summary"])

        st.markdown("---")
        st.subheader("Dominant Hazards by Province")
        prov_choice = st.selectbox("Select a province / territory", list(data.DISASTER_HAZARD_BY_PROVINCE.keys()))
        for hz in data.DISASTER_HAZARD_BY_PROVINCE[prov_choice]:
            st.markdown(f"- {hz}")

# ---------------------------------------------------------------------------
# 📈 SOCIO-ECONOMIC & AGRO-ECONOMIC
# ---------------------------------------------------------------------------
elif choice == "📈 Socio-Economic & Agro-Economic":
    st.title("Socio-Economic & Agro-Economic Domains")

    if "regional_agro_socio_df" not in st.session_state:
        st.session_state["regional_agro_socio_df"] = pd.DataFrame(data.REGIONAL_AGRO_SOCIO_DATA)

    def _render_regional_dataset(key_prefix: str):
        """Shared input-driven province/region socio-agro dataset + chart
        picker, rendered under both the Socio-Economic and Agro-Economic
        headers (same underlying editable table via session_state)."""
        st.caption(data.REGIONAL_AGRO_SOCIO_NOTE)
        edited = st.data_editor(
            st.session_state["regional_agro_socio_df"],
            use_container_width=True, hide_index=True, num_rows="dynamic",
            key=f"{key_prefix}_editor",
        )
        st.session_state["regional_agro_socio_df"] = edited

        c1, c2 = st.columns(2)
        with c1:
            graph_type = st.selectbox(
                "Graph type", data.REGIONAL_AGRO_SOCIO_GRAPH_TYPES, key=f"{key_prefix}_graph_type"
            )
        with c2:
            metric = st.selectbox(
                "Metric", data.REGIONAL_AGRO_SOCIO_METRICS, key=f"{key_prefix}_metric"
            )

        if edited.empty or "Province/Region" not in edited.columns:
            st.info("Add at least one row with a Province/Region to chart.")
            return

        if graph_type == "Bar chart":
            fig = px.bar(edited, x="Province/Region", y=metric, title=f"{metric} by Province/Region")
        elif graph_type == "Pie chart":
            fig = px.pie(edited, names="Province/Region", values=metric, title=f"{metric} share by Province/Region")
        elif graph_type == "Scatter plot":
            fig = px.scatter(
                edited, x="Province/Region", y=metric, size=metric, color="Province/Region",
                title=f"{metric} by Province/Region",
            )
        else:  # Line chart
            fig = px.line(edited, x="Province/Region", y=metric, markers=True, title=f"{metric} by Province/Region")
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True}, key=f"{key_prefix}_chart")

    st.header("📈 Socio-Economic Domain")
    for k, v in data.SOCIO_ECONOMIC_DOMAIN.items():
        st.markdown(f"**{k}:** {v}")

    st.subheader("📊 Input-driven socio/agro data")
    _render_regional_dataset("socio")

    st.header("🌾 Agro-Economic Domain")
    for k, v in data.AGRO_ECONOMIC_DOMAIN.items():
        st.markdown(f"**{k}:** {v}")

    st.subheader("📊 Input-driven socio/agro data")
    st.caption("Same editable dataset as above — edits here and under Socio-Economic Domain stay in sync.")
    _render_regional_dataset("agro")

    st.header("🗓️ Major Crop Seasons — Rabi & Kharif")
    season_tabs = st.tabs(list(data.CROP_SEASONS.keys()))
    for tab, (season_name, season) in zip(season_tabs, data.CROP_SEASONS.items()):
        with tab:
            c1, c2 = st.columns(2)
            c1.metric("Sowing window", season["sowing_window"])
            c2.metric("Harvest window", season["harvest_window"])
            st.write(season["description"])
            st.markdown("**Major crops:**")
            crop_rows = [
                {"Season": season_name, "Crop": crop, "Typical window": info["typical_window"],
                 "Engineering/water note": info["engineering_water_note"]}
                for crop, info in season["major_crops"].items()
            ]
            kit.explore(pd.DataFrame(crop_rows), key=f"kit_13_{season_name}")
            for crop, info in season["major_crops"].items():
                with st.expander(crop):
                    st.write(info["description"])

    st.header("🐝🐟 Allied Agriculture Sectors")
    sector_cols = st.columns(2)
    for col, (sector_name, sector) in zip(sector_cols, data.ALLIED_AGRI_SECTORS.items()):
        with col:
            st.subheader(sector_name)
            st.write(sector["overview"])
            st.markdown(f"**Key regions:** {sector['key_regions']}")
            if "species" in sector:
                st.markdown(f"**Species:** {sector['species']}")
            st.markdown(f"**Economic role:** {sector['economic_role']}")
            st.markdown(f"**Challenges:** {sector['challenges']}")

    st.subheader("🐝 Apiculture indicators")
    st.dataframe(
        pd.DataFrame(data.APICULTURE_INDICATORS).rename(
            columns={"indicator": "Indicator", "unit": "Unit", "description": "Description"}
        ),
        use_container_width=True, hide_index=True,
    )

    st.subheader("🐟 Aquaculture indicators")
    st.dataframe(
        pd.DataFrame(data.AQUACULTURE_INDICATORS).rename(
            columns={"indicator": "Indicator", "unit": "Unit", "description": "Description"}
        ),
        use_container_width=True, hide_index=True,
    )

# ---------------------------------------------------------------------------
# 🗺️ GEO-POLITICAL & STRATEGIC
# ---------------------------------------------------------------------------
elif choice == "🗺️ Geo-Political & Strategic":
    st.title("Geo-Political & Strategic Domains")
    st.plotly_chart(map_view.geopolitical_map(), use_container_width=True, config={"scrollZoom": True})

    st.header("🗺️ Strategic Overview")
    for k, v in data.GEOPOLITICAL_DOMAIN.items():
        with st.expander(k):
            st.write(v)

    st.header("⚖️ Internal Inter-Provincial Water Disputes: Punjab vs. Sindh")
    d = data.INTERNAL_WATER_DISPUTES
    st.write(d["overview"])
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sindh's Grievances (Lower Riparian)")
        st.write(d["Sindh's Grievances (Lower Riparian)"])
    with c2:
        st.subheader("Punjab's Counter-Claims (Upper Riparian)")
        st.write(d["Punjab's Counter-Claims (Upper Riparian)"])
    st.subheader("Structural Gridlocks / Deadlock")
    st.write(d["Structural Gridlocks / Deadlock"])
    st.subheader("Environmental Impacts of Indian Chenab Projects on Punjab's Crops")
    for k, v in d["Environmental Impacts of Indian Chenab Projects on Punjab's Crops"].items():
        st.markdown(f"**{k}:** {v}")

    st.header("⚖️ Legal Mechanisms to Resolve IRSA Inter-Provincial Disputes")
    for k, v in data.IRSA_LEGAL_MECHANISMS.items():
        st.markdown(f"**{k}:** {v}")

    with st.expander("📚 Sources for this section"):
        for ref in data.SOURCES["Indus Waters Treaty & Arbitration"] + data.SOURCES["Dams & Water Governance"]:
            st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# 🇨🇳 CHINA HYDROPOWER (CPEC)
# ---------------------------------------------------------------------------
elif choice == "🇨🇳 China Hydropower (CPEC)":
    st.title("The Financial Footprint of China's Investments in Pakistan's Hydropower")
    st.plotly_chart(map_view.china_hydropower_map(), use_container_width=True, config={"scrollZoom": True})

    fp = data.CHINA_HYDROPOWER_FOOTPRINT
    st.markdown(f"**Dominant share of FDI:** {fp['Dominant Share of FDI']}")

    st.subheader("Major Hydropower Asset Portfolio")
    df = pd.DataFrame([
        {"Project": k, **v} for k, v in fp["Major Hydropower Asset Portfolio"].items()
    ]).rename(columns={
        "capacity_MW": "Capacity (MW)", "river": "River", "status": "Status", "notes": "Notes",
    })
    kit.explore(df, key="kit_14")

    total_mw = sum(v["capacity_MW"] for v in fp["Major Hydropower Asset Portfolio"].values())
    st.metric("Combined CPEC hydropower capacity (portfolio total)", f"{total_mw:,.1f} MW")

    st.markdown("### Portfolio network by host river")
    st.plotly_chart(network_view.hydropower_cpec_network(), use_container_width=True, config={"scrollZoom": True})

    with st.expander("📚 Sources for this section"):
        for ref in data.SOURCES["CPEC Hydropower Projects"]:
            st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# 🇮🇳 CHENAB PROJECTS, FLOW CONCERNS & INDUS WATERS TREATY
# ---------------------------------------------------------------------------
elif choice == "🇮🇳 Chenab Projects, Flow Concerns & Indus Waters Treaty":
    st.title("🇮🇳 Chenab Projects, Flow Concerns and Indus Waters Treaty")
    st.plotly_chart(map_view.india_dam_disputes_map(), use_container_width=True, config={"scrollZoom": True})

    dd = data.INDIA_DAM_DESIGN_DISPUTES
    tp = dd["technical_points_of_contention"]

    st.header("Pakal Dul (1,000 MW) and Ratle (850 MW)")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Pakal Dul Dam")
        st.metric("Capacity", f"{dd['Pakal Dul Dam']['capacity_MW']} MW")
        st.markdown(f"**River:** {dd['Pakal Dul Dam']['river']}")
        st.markdown(f"**Location:** {dd['Pakal Dul Dam']['location']}")
    with c2:
        st.subheader("Ratle Dam")
        st.metric("Capacity", f"{dd['Ratle Dam']['capacity_MW']} MW")
        st.markdown(f"**River:** {dd['Ratle Dam']['river']}")
        st.markdown(f"**Location:** {dd['Ratle Dam']['location']}")

    st.header("India's CEA/NHPC-listed Indus-basin hydropower projects (J&K)")
    st.caption(
        f"India's Central Electricity Authority lists {cea.OPERATIONAL_COUNT} operational + "
        f"{cea.UNDER_CONSTRUCTION_COUNT} under-construction = {len(cea.PROJECTS)} projects in this "
        f"inventory, totalling {cea.TOTAL_CAPACITY_MW:,.1f} MW "
        f"({cea.OPERATIONAL_CAPACITY_MW:,.1f} MW operational, {cea.UNDER_CONSTRUCTION_CAPACITY_MW:,.1f} MW "
        f"under construction)."
    )
    st.plotly_chart(map_view.india_hydropower_cea_map(cea.PROJECTS), use_container_width=True, config={"scrollZoom": True})
    cea_df = pd.DataFrame(cea.PROJECTS)[["rank", "name", "river", "district", "capacity_MW", "status"]].rename(
        columns={"rank": "#", "name": "Project", "river": "River", "district": "District",
                 "capacity_MW": "Capacity (MW)", "status": "Status"}
    )
    kit.explore(cea_df, key="kit_15")
    st.caption(cea.EXCLUDED_PROJECTS_NOTE)
    st.info(cea.MAP_NOTE)
    with st.expander("📚 Source"):
        st.markdown(f"- {cea.SOURCE_NOTE}")

    st.header("Technical points raised by Pakistan in the IWT proceedings")
    for topic in ["Pondage Capacity", "Freeboard Height & Dam Elevation", "Deep-Level Outlets and Gated Spillways"]:
        with st.expander(topic):
            st.markdown(f"**The issue:** {tp[topic]['issue']}")
            st.markdown(f"**Pakistan's view:** {tp[topic]['pakistan_view']}")

    st.header("Head Marala / crop-impact issue")
    hm_dispute = data.INTERNAL_WATER_DISPUTES["Environmental Impacts of Indian Chenab Projects on Punjab's Crops"]
    st.markdown(f"**Flow reductions reported at Head Marala:** {hm_dispute['Flow Reductions at Head Marala']}")
    st.markdown(f"**Reported crop impacts:** {hm_dispute['Devastating Crop Impacts']}")
    st.info(data.HEAD_MARALA_NOTE)

    st.header("Court of Arbitration (PCA) timeline")
    st.caption("Indus Waters Western Rivers Arbitration (Islamic Republic of Pakistan v. Republic of India), PCA Case No. 2023-01")
    for item in data.PCA_TIMELINE:
        with st.expander(f"{item['date']} — {item['event']}"):
            st.write(item["detail"])
    st.info(data.COA_VALIDITY_NOTE)

    st.header("India's proposed inter-basin canal / transfer projects")
    icp = data.INDIA_PROPOSED_CANAL_PROJECTS
    st.write(icp["overview"])
    st.subheader("113km Indus-to-Rajasthan Canal (reported proposal)")
    st.write(icp["113km Indus-to-Rajasthan Canal (reported proposal)"])
    st.subheader("Two new canal systems (reported proposals)")
    for name, detail in icp["Two New Canal Systems (reported proposals)"].items():
        with st.expander(name):
            st.write(detail)
    st.markdown(f"**Expedited hydropower construction (reported):** {icp['Expedited Hydropower Construction (reported)']}")
    st.caption(icp["framing_note"])

    tab_overview, tab_atrocities = st.tabs(
        ["📋 Dispute Overview (above)", "⚖️ Indian Atrocities — Detailed Technical & Timeline Record"]
    )
    with tab_overview:
        st.caption("See the sections above on this page for the dam profiles, Head Marala issue, PCA timeline and India's proposed canal projects.")

    with tab_atrocities:
        st.caption(
            "Everything in this tab is presented as Pakistan's and India's REPORTED positions in the ongoing "
            "IWT technical dispute — including the specific disputed figures below — not as adjudicated fact. "
            "The Neutral Expert (Annexure F) and Court of Arbitration (Annexure G) tracks are parallel, and the "
            "two governments dispute each other's characterization of both the designs and the processes."
        )

        st.subheader("🔧 The Disputed Engineering Specifications")
        st.write(data.TECHNICAL_DISPUTE_DETAILS["framing_note"])
        for topic in ["Pondage Capacity (Live Storage)", "Orifice Spillways & Gate Placements",
                      "Intake Submergence Levels", "Freeboard Heights"]:
            detail = data.TECHNICAL_DISPUTE_DETAILS[topic]
            with st.expander(topic):
                st.markdown(f"**What it is:** {detail['what_it_is']}")
                st.markdown(f"**The dispute:** {detail['the_dispute']}")
                st.markdown(f"**Pakistan's strategic concern:** {detail['pakistans_strategic_concern']}")

        st.subheader("⏳ The Neutral Expert Timeline (2026–2027)")
        ne_df = pd.DataFrame(data.NEUTRAL_EXPERT_TIMELINE).rename(
            columns={"date": "Date", "milestone": "Milestone", "detail": "Detail"}
        )
        kit.explore(ne_df, key="kit_16")
        for item in data.NEUTRAL_EXPERT_TIMELINE:
            st.markdown(f"**{item['date']} — {item['milestone']}**")
        st.caption(
            "World Bank-appointed Neutral Expert (Michel Lino) process under the treaty's Annexure F "
            "technical-review track, running in parallel with the Court of Arbitration proceedings above."
        )

        st.subheader("🧊 The Concrete Freeze & Competing Positions")
        freeze = data.COA_CONCRETE_FREEZE_AND_DEFIANCE
        for k in ["The Concrete Freeze (31 Aug 2026)", "The Engineering Risk Pakistan Raises", "India's Reported Position"]:
            with st.expander(k):
                st.write(freeze[k])
        st.info(freeze["framing_note"])

    st.header("📊 IWT Infographics")
    st.caption(
        "Reference infographics summarizing the treaty's permanence clause, dispute-resolution "
        "mechanism, data-sharing suspension, dam-design contention, and permitted western-river "
        "uses — presented as explanatory summaries, not primary legal text. Verify against the "
        "treaty text and PCA/Neutral Expert filings before citing in a formal context."
    )
    IWT_INFOGRAPHICS = [
        {
            "title": "The IWT Treaty",
            "file": "assets/iwt_infographics/the_iwt_treaty_dispute_resolution.png",
            "caption": "The treaty's three-tier dispute-resolution mechanism — Permanent Indus "
                       "Commission (PIC), Neutral Expert, and Court of Arbitration — with the "
                       "Baglihar (2007) and Kishanganga (2013) cases that tested it.",
        },
        {
            "title": "Article XII(3): Modification by Consent",
            "file": "assets/iwt_infographics/article_xii3_modification_by_consent.png",
            "caption": "The treaty has no expiry date and can only be modified by mutual "
                       "consent of both governments (Article XII(3)) — contrasted with the "
                       "2023 Indian modification notice, Pakistan's refusal, and the 2025 "
                       "'held in abeyance' standoff.",
        },
        {
            "title": "IWT Main Points",
            "file": "assets/iwt_infographics/iwt_main_points.png",
            "caption": "A six-point summary of the treaty's core provisions: river allocation, "
                       "permitted uses, storage restrictions, data sharing, dispute resolution, "
                       "and the permanence clause.",
        },
        {
            "title": "Impact on Transboundary Water Cooperation",
            "file": "assets/iwt_infographics/impact_on_transboundary_water_cooperation.png",
            "caption": "Before 2025 vs. April 2025: the suspension of river-flow, rainfall, "
                       "flood-forecast and dam-release data exchange between the two sides "
                       "under Article VII.",
        },
        {
            "title": "1960 Dam Design vs. Modern Design",
            "file": "assets/iwt_infographics/1960_dam_design.png",
            "caption": "The 1960 treaty envisioned small run-of-river weirs with negligible "
                       "pondage; the contested zone in today's disputes is the gap between the "
                       "Annexure D storage limit and a modern gated dam's actual intake level.",
        },
        {
            "title": "Western Rivers (Pakistan) — Permitted Uses",
            "file": "assets/iwt_infographics/western_rivers_pakistan.png",
            "caption": "India's four permitted-use categories on the western rivers (Indus, "
                       "Jhelum, Chenab) under the treaty: domestic use, non-consumptive use, "
                       "limited agriculture on pre-1960 irrigated areas, and run-of-river "
                       "hydropower subject to Annexure D storage limits.",
        },
    ]
    IWT_INFOGRAPHIC_TEXT_KEYS = {
        "The IWT Treaty": "The IWT Treaty",
        "Article XII(3): Modification by Consent": "Article XII(3) Modification by Consent",
        "IWT Main Points": "IWT Main points",
        "Impact on Transboundary Water Cooperation": "Impact on Transboundary Water Cooperation",
        "1960 Dam Design vs. Modern Design": "1960 Dam Design",
        "Western Rivers (Pakistan) — Permitted Uses": "Western Rivers Pakistan",
    }

    st.caption("🔍 Scroll or pinch to zoom into any infographic below, and drag to pan — the same control as the app's maps.")
    infographic_cols = st.columns(2)
    for i, item in enumerate(IWT_INFOGRAPHICS):
        with infographic_cols[i % 2]:
            try:
                fig = render_interactive_image(asset_path(item["file"]), title=item["title"])
                st.plotly_chart(
                    fig, use_container_width=True, config={"scrollZoom": True},
                    key=f"iwt_infographic_{i}",
                )
                st.caption(item["caption"])
            except Exception:
                pass
            text_key = IWT_INFOGRAPHIC_TEXT_KEYS.get(item["title"])
            text_content = data.IWT_TREATY_INFOGRAPHIC.get(text_key) if text_key else None
            if text_content:
                with st.expander("📝 Key points (text version)"):
                    for point in text_content["points"]:
                        st.markdown(f"- {point}")
                    st.caption(text_content["source_note"])

    with st.expander("📚 Sources for this section"):
        for ref in data.SOURCES["Indus Waters Treaty & Arbitration"]:
            st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# 🧮 INTERACTIVE HYDRAULIC MODELS
# ---------------------------------------------------------------------------
elif choice == "🧮 Interactive Hydraulic Models":
    st.title("Interactive Hydraulic & Risk Models")
    st.caption(
        "⚠️ Simplified, illustrative models for dashboard exploration only — "
        "not validated hydrological/engineering tools."
    )

    with st.expander("📍 Reference map — real infrastructure these models are inspired by", expanded=False):
        st.plotly_chart(map_view.irrigation_network_geomap(), use_container_width=True, config={"scrollZoom": True})
        st.caption(
            "The reservoir, shortage-sharing, link-canal and risk-index tools below use "
            "generic user-entered numbers — this map just shows where the real dams, "
            "barrages and link canals they're modeled on actually sit."
        )

    model_tab1, model_tab2, model_tab3, model_tab4 = st.tabs(
        ["Reservoir Simulation", "Shortage-Sharing Allocation", "Link Canal Transfer", "Disaster Risk Index"]
    )

    with model_tab1:
        st.subheader("Reservoir Mass-Balance Simulation")
        st.caption(
            "Period-by-period balance: available = storage + inflow − evaporation; "
            "release is capped at demand and at what's available; any shortfall is "
            "a shortage, any excess above capacity spills. This balance logic was "
            "cross-checked period-by-period against an independently-produced "
            "12-period reservoir mass-balance reference run and reproduces it "
            "exactly given the same inputs."
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            capacity = st.number_input("Live storage capacity", value=1000.0, min_value=0.1)
            current = st.number_input("Starting storage", value=600.0, min_value=0.0)
        with c2:
            inflow = st.number_input("Inflow per period", value=450.0, step=10.0)
            outflow = st.number_input("Demand per period", value=400.0, step=10.0)
        with c3:
            evap = st.number_input("Evaporation / seepage loss per period", value=20.0, step=1.0)
            target = st.number_input("Target (operating) storage", value=600.0, min_value=0.0)
        days = st.slider("Simulation horizon (periods)", 5, 120, 12)

        state = hm.ReservoirState("Reservoir", capacity, current, inflow, outflow, evap, target)
        trace = hm.simulate_reservoir(state, days)
        df = pd.DataFrame(trace)
        st.line_chart(df.set_index("day")[["storage_maf", "target_storage"]])
        if df["spilling"].any():
            st.warning("Reservoir reaches full capacity and begins spilling during this simulation.")
        if (df["shortage"] > 0).any():
            st.warning("Demand exceeds available water (storage + inflow − evaporation) in at least one period — a shortage occurs.")
        st.dataframe(
            df.rename(columns={
                "day": "Period", "storage_maf": "End Storage", "inflow": "Inflow",
                "demand": "Demand", "evaporation": "Evaporation", "release": "Release",
                "shortage": "Shortage", "spill": "Spill", "target_storage": "Target Storage",
                "storage_deviation": "Storage Deviation", "spilling": "Spilling?",
            }),
            use_container_width=True, hide_index=True,
        )

    with model_tab2:
        st.subheader("Simplified Shortage-Sharing Allocation")
        st.caption("Illustrative equal-percentage shortage-sharing model — not the official IRSA formula.")
        total = st.number_input("Total available water (MAF)", value=100.0, min_value=0.0)
        shortage = st.slider("System-wide shortage (%)", 0, 50, 10)
        alloc = hm.allocate_shortage(total, shortage)
        st.bar_chart(pd.Series(alloc, name="Allocation (MAF)"))
        st.dataframe(
            pd.DataFrame(alloc.items(), columns=["Province", "Allocation (MAF)"]),
            use_container_width=True, hide_index=True,
        )

    with model_tab3:
        st.subheader("Link Canal Transfer Calculator")
        c1, c2, c3 = st.columns(3)
        with c1:
            src_flow = st.number_input("Source river flow (cusecs)", value=50000, step=1000)
        with c2:
            canal_cap = st.number_input("Link canal capacity (cusecs)", value=15000, step=500)
        with c3:
            offtake = st.slider("Requested offtake (% of source flow)", 0, 100, 40)
        result = hm.link_canal_transfer(src_flow, canal_cap, offtake)
        c1, c2, c3 = st.columns(3)
        c1.metric("Requested (cusecs)", f"{result['requested_cusecs']:,.0f}")
        c2.metric("Transferred (cusecs)", f"{result['transferred_cusecs']:,.0f}")
        c3.metric("Remaining in source river (cusecs)", f"{result['remaining_in_source_river_cusecs']:,.0f}")
        if result["capacity_limited"]:
            st.info("Transfer is capped by the link canal's design capacity, not the offtake request.")

    with model_tab4:
        st.subheader("Composite Disaster Risk Index (illustrative)")
        c1, c2, c3 = st.columns(3)
        with c1:
            flood = st.slider("Flood exposure", 0, 10, 7)
            glof = st.slider("GLOF susceptibility", 0, 10, 6)
        with c2:
            drought = st.slider("Drought exposure", 0, 10, 5)
            seismic = st.slider("Seismic hazard", 0, 10, 7)
        with c3:
            coastal = st.slider("Coastal exposure", 0, 10, 4)
            capacity_score = st.slider("Institutional capacity (higher = better)", 0, 10, 4)

        score, band = hm.composite_disaster_risk_index(flood, glof, drought, seismic, coastal, capacity_score)
        st.metric("Composite Risk Score (0-100)", score, delta=band)
        band_colors = {"Low": "🟢", "Moderate": "🟡", "High": "🟠", "Severe": "🔴"}
        st.markdown(f"### {band_colors.get(band, '')} Risk Band: **{band}**")

# ---------------------------------------------------------------------------
# 🛰️ SEBAL EVAPOTRANSPIRATION ENGINE
# ---------------------------------------------------------------------------
elif choice == "🛰️ SEBAL Evapotranspiration Engine":
    st.title("SEBAL Model: Indus Basin Advanced Evapotranspiration Engine")
    st.caption("Created and designed by Engr. Syed Hassan Iqbal Shah (ELECT/28314)")
    st.caption(
        "⚠️ Offline, upload-driven re-implementation of the published SEBAL/METRIC "
        "surface-energy-balance algorithm — not pulled from live satellite imagery "
        "(no Earth Engine account needed). It is NOT validated until you compare it "
        "with real field lysimeter / eddy-covariance / Bowen-ratio measurements in the "
        "✅ Validation tab. Educational/illustrative only; verify before any "
        "operational or water-allocation use."
    )

    with st.expander("ℹ️ How this works & what to upload", expanded=False):
        st.markdown(
            "SEBAL (Bastiaanssen et al. 1998) solves the surface energy balance "
            "**Rn = G + H + LE** for the latent heat flux (LE), which is then "
            "converted to evapotranspiration. This module runs the full chain — "
            "net radiation → soil heat flux → aerodynamic resistance with "
            "iterative Monin-Obukhov stability correction → hot/cold anchor-pixel "
            "calibration → sensible heat flux → ET — on a table of per-zone or "
            "per-pixel remote-sensing-derived inputs that **you upload or edit "
            "below**, instead of pulling imagery live from Google Earth Engine.\n\n"
            "**Required columns:** `Name`, `NDVI`, `Albedo`, `Ts_C` (surface "
            "temperature, °C), `Ta_C` (air temperature, °C), `Rs_down` (incoming "
            "shortwave radiation, W/m²), `Wind_ms` (wind speed, m/s).\n\n"
            "**Optional columns:** `Latitude`, `Longitude`, `Elevation_m`, "
            "`Crop_Height_m`, `Day_of_Year`, `Transmissivity` — improve the "
            "FAO-56 daily-radiation fallback and roughness-length estimate when "
            "supplied, but the model runs without them.\n\n"
            "**Method references:** Bastiaanssen et al. (1998) SEBAL; Allen, "
            "Tasumi & Trezza (2007) METRIC; Allen et al. (1998) FAO-56; "
            "Brutsaert (1982); Paulson (1970) / Webb (1970)."
        )

    tab_run, tab_analytics, tab_validate = st.tabs(["🧮 SEBAL Model", "📊 CSV Analytics (Bar / Pie / Scatter / Line) & Map", "✅ Validation vs Field Measurements"])
    st.session_state["sebal_last_results"] = None

    with tab_run:
        template_df = sebal.csv_template()
        st.download_button(
            "⬇️ Download CSV template",
            data=template_df.to_csv(index=False).encode("utf-8"),
            file_name="sebal_input_template.csv",
            mime="text/csv",
        )

        data_source = st.radio(
            "Data source", ["Use synthetic demo dataset", "Upload my own CSV", "Edit a table here"],
            horizontal=True, key="sebal_source",
        )

        raw_df = None
        if data_source == "Use synthetic demo dataset":
            n_zones = st.slider("Number of demo zones", 4, 20, 8, key="sebal_demo_n")
            raw_df = sebal.generate_sample_dataset(n=n_zones)
            st.caption("Synthetic demo data for illustration only — not real satellite observations.")
        elif data_source == "Upload my own CSV":
            up = st.file_uploader("Upload a per-zone/per-pixel CSV", type=["csv"], key="sebal_upload")
            if up is not None:
                try:
                    raw_df = file_import.load_csv_generic(up)
                except file_import.FileImportError as e:
                    st.error(str(e))
            else:
                st.info("Upload a CSV, or switch to the demo dataset / editable table above.")
        else:
            seed_df = sebal.generate_sample_dataset(n=6)
            raw_df = st.data_editor(seed_df, num_rows="dynamic", use_container_width=True, key="sebal_editor")

        if raw_df is not None and not raw_df.empty:
            try:
                standardized = sebal.standardize_columns(raw_df)
            except sebal.SebalInputError as e:
                st.error(str(e))
                standardized = None

            if standardized is not None:
                st.subheader("Input Data")
                st.dataframe(standardized, use_container_width=True, hide_index=True)

                with st.expander("⚙️ Calibration & environment settings", expanded=False):
                    c1, c2 = st.columns(2)
                    with c1:
                        auto_pixels = st.checkbox("Auto-select hot/cold anchor pixels", value=True, key="sebal_auto")
                        atm_eps = st.slider("Atmospheric emissivity", 0.70, 0.95, 0.85, 0.01, key="sebal_eps")
                    with c2:
                        doy = st.slider("Default day-of-year (if not in data)", 1, 365, 180, key="sebal_doy")
                        elev = st.number_input("Default elevation (m, if not in data)", value=200.0, step=10.0, key="sebal_elev")

                    hot_i = cold_i = None
                    if not auto_pixels:
                        names = standardized["Name"].astype(str).tolist()
                        cold_name = st.selectbox("Cold (wet/vegetated) pixel", names, index=0, key="sebal_cold_sel")
                        hot_name = st.selectbox("Hot (dry/bare) pixel", names, index=min(1, len(names) - 1), key="sebal_hot_sel")
                        cold_i = standardized.index[standardized["Name"].astype(str) == cold_name][0]
                        hot_i = standardized.index[standardized["Name"].astype(str) == hot_name][0]

                try:
                    results, calib = sebal.run_sebal(
                        standardized, hot_idx=hot_i, cold_idx=cold_i,
                        atm_emissivity=atm_eps, default_day_of_year=doy, default_elevation_m=elev,
                    )
                except Exception as e:
                    st.error(f"SEBAL run failed: {e}")
                    results, calib = None, None

                if results is not None:
                    st.session_state["sebal_last_results"] = results
                    st.subheader("Hot / Cold Pixel Calibration")
                    cc1, cc2, cc3 = st.columns(3)
                    cc1.metric("Cold pixel (wet/vegetated)", calib["cold_pixel_name"])
                    cc2.metric("Hot pixel (dry/bare)", calib["hot_pixel_name"])
                    cc3.metric("Fitted dT = a + b·Ts", f"a={calib['a']:.3f}, b={calib['b']:.4f}")

                    st.subheader("Energy Balance & Evapotranspiration Results")
                    show_cols = [
                        "Name", "NDVI", "Rn_Wm2", "G_Wm2", "H_Wm2", "LE_Wm2",
                        "Evaporative_Fraction", "ET_inst_mm_hr", "ET24_mm_day",
                    ]
                    st.dataframe(
                        results[show_cols].rename(columns={
                            "Rn_Wm2": "Rn (W/m²)", "G_Wm2": "G (W/m²)", "H_Wm2": "H (W/m²)",
                            "LE_Wm2": "LE (W/m²)", "Evaporative_Fraction": "Evap. Fraction",
                            "ET_inst_mm_hr": "ET inst (mm/hr)", "ET24_mm_day": "ET24 (mm/day)",
                        }),
                        use_container_width=True, hide_index=True,
                    )

                    chart_df = results.set_index("Name")[["ET24_mm_day"]]
                    st.bar_chart(chart_df)

                    avg_et24 = float(results["ET24_mm_day"].mean())
                    st.metric("Average daily ET across zones (ET24)", f"{avg_et24:.2f} mm/day")

                    has_coords = (
                        {"Latitude", "Longitude"}.issubset(standardized.columns)
                        and standardized[["Latitude", "Longitude"]].notna().all(axis=None)
                    )
                    if has_coords:
                        map_points = results.rename(columns={"Name": "Name"}).copy()
                        map_points["Latitude"] = standardized["Latitude"]
                        map_points["Longitude"] = standardized["Longitude"]
                        map_points["Category"] = pd.cut(
                            map_points["ET24_mm_day"], bins=4,
                            labels=["Low ET", "Moderate ET", "High ET", "Very High ET"],
                        ).astype(str)
                        st.plotly_chart(
                            map_view.custom_points_map(map_points, title="SEBAL Zones — Daily ET (mm/day)"),
                            use_container_width=True, config={"scrollZoom": True}, key="sebal_map",
                        )

                    st.subheader("Export")
                    st.download_button(
                        "⬇️ Download results CSV",
                        data=results.to_csv(index=False).encode("utf-8"),
                        file_name="sebal_results.csv",
                        mime="text/csv",
                        key="sebal_csv_dl",
                    )
                    try:
                        import sebal_report
                        pdf_bytes = sebal_report.build_sebal_pdf_report(results, calib)
                        st.download_button(
                            "⬇️ Download PDF report",
                            data=pdf_bytes,
                            file_name="sebal_report.pdf",
                            mime="application/pdf",
                            key="sebal_pdf_dl",
                        )
                    except ImportError:
                        st.caption(
                            "PDF export requires the 'reportlab' package (see requirements.txt)."
                        )
                    except Exception as e:
                        st.caption(f"PDF report could not be generated: {e}")


    with tab_analytics:
        st.subheader("CSV Analytics — Bar, Pie, Scatter & Line Charts")
        st.caption(
            "Upload any CSV file(s) — telemetry readings, SEBAL results you exported "
            "above, water-quality logs, crop data, anything tabular — and build a bar, "
            "pie, scatter or line chart from any of its columns. If a file also has "
            "recognizable latitude/longitude columns, it is automatically plotted on "
            "an interactive map below the chart."
        )
        an_files = st.file_uploader(
            "Upload one or more CSV files", type=["csv"], accept_multiple_files=True,
            key="sebal_an_upload",
        )

        if an_files:
            file_names = [f.name for f in an_files]
            if len(an_files) > 1:
                chosen_name = st.selectbox("Choose a file to analyze", file_names, key="sebal_an_file_pick")
            else:
                chosen_name = file_names[0]
            chosen_file = next(f for f in an_files if f.name == chosen_name)

            try:
                chosen_file.seek(0)
            except Exception:
                pass
            try:
                df_raw = file_import.load_csv_generic(chosen_file)
            except file_import.FileImportError as e:
                st.error(str(e))
                df_raw = None

            if df_raw is not None:
                st.success(f"Parsed a {df_raw.shape[0]}×{df_raw.shape[1]} table from **{chosen_name}**.")
                st.dataframe(df_raw, use_container_width=True, hide_index=True)

                all_cols = list(df_raw.columns)
                numeric_cols = df_raw.select_dtypes(include="number").columns.tolist()
                if not numeric_cols:
                    coerced = df_raw.apply(pd.to_numeric, errors="coerce")
                    numeric_cols = [c for c in coerced.columns if coerced[c].notna().any()]

                chart_type = st.selectbox(
                    "Chart type", ["Bar", "Pie", "Scatter", "Line"], key="sebal_an_chart_type"
                )

                if chart_type == "Bar":
                    x_col = st.selectbox("Category / X axis", all_cols, key="sebal_an_bar_x")
                    y_col = st.selectbox("Value / Y axis", numeric_cols or all_cols, key="sebal_an_bar_y")
                    fig = px.bar(df_raw, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                elif chart_type == "Pie":
                    names_col = st.selectbox("Labels", all_cols, key="sebal_an_pie_names")
                    values_col = st.selectbox("Values", numeric_cols or all_cols, key="sebal_an_pie_values")
                    fig = px.pie(df_raw, names=names_col, values=values_col, title=f"{values_col} share by {names_col}")
                elif chart_type == "Scatter":
                    x_col = st.selectbox("X axis", numeric_cols or all_cols, key="sebal_an_scatter_x")
                    y_col = st.selectbox("Y axis", numeric_cols or all_cols, key="sebal_an_scatter_y")
                    color_choice = st.selectbox("Color by (optional)", ["None"] + all_cols, key="sebal_an_scatter_color")
                    fig = px.scatter(
                        df_raw, x=x_col, y=y_col,
                        color=None if color_choice == "None" else color_choice,
                        title=f"{y_col} vs {x_col}",
                    )
                else:  # Line
                    x_col = st.selectbox("X axis", all_cols, key="sebal_an_line_x")
                    y_col = st.selectbox("Y axis", numeric_cols or all_cols, key="sebal_an_line_y")
                    fig = px.line(df_raw, x=x_col, y=y_col, title=f"{y_col} over {x_col}", markers=True)

                st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True}, key="sebal_an_chart")

            try:
                chosen_file.seek(0)
            except Exception:
                pass
            try:
                df_points = file_import.load_any(chosen_file)
            except file_import.FileImportError:
                df_points = None

            if df_points is not None and not df_points.empty:
                st.subheader("🗺️ Map (latitude/longitude columns detected)")
                st.plotly_chart(
                    map_view.custom_points_map(df_points, title=f"Map — {chosen_name}"),
                    use_container_width=True, config={"scrollZoom": True}, key="sebal_an_map",
                )
                st.dataframe(df_points, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Download parsed map points CSV",
                    df_points.to_csv(index=False).encode("utf-8"),
                    file_name="sebal_analytics_map_points.csv",
                    mime="text/csv",
                    key="sebal_an_map_dl",
                )
        else:
            st.info(
                "Upload one or more CSV files above to build charts here — e.g. the "
                "telemetry or water-quality CSVs from the Upload File tab, or a results "
                "CSV exported from the SEBAL Model tab. Files with latitude/longitude "
                "columns also get an automatic map."
            )

    with st.expander("📚 Sources & method references"):
        for label, url in [
            ("Bastiaanssen et al. (1998) — SEBAL formulation, J. Hydrology",
             "https://doi.org/10.1016/S0022-1694(98)00253-4"),
            ("Allen, Tasumi & Trezza (2007) — METRIC model, J. Irrigation & Drainage Eng.",
             "https://doi.org/10.1061/(ASCE)0733-9437(2007)133:4(380)"),
            ("Allen et al. (1998) — FAO Irrigation & Drainage Paper 56",
             "https://www.fao.org/4/X0490E/X0490E00.htm"),
            ("Brutsaert (1982) — Evaporation into the Atmosphere",
             "https://doi.org/10.1007/978-94-017-1497-6"),
        ]:
            st.markdown(f"- [{label}]({url})")
        st.caption(
            "Re-implemented from the published formulation for this offline "
            "dashboard module — not derived from any proprietary SEBAL/METRIC "
            "software or Earth Engine script."
        )

# ---------------------------------------------------------------------------
# 📤 UPLOAD FILE → MAP & CHARTS
# ---------------------------------------------------------------------------
    with tab_validate:
        sebal_validation.render(st.session_state.get("sebal_last_results"))

elif choice == "📤 Upload File → Map, Charts & Analytics":
    st.title("Upload Your Own Data → Map, Charts & Analytics")
    st.caption(
        "Upload a CSV or PDF and turn it into an interactive map, or a bar, pie, "
        "scatter or line chart — no coding required."
    )
    with st.expander("📋 Expected file format", expanded=False):
        st.markdown(
            "**For the Map tab:** a table with latitude/longitude columns, using headers "
            "such as `lat`/`latitude` and `lon`/`longitude` (or `lng`, `x`, `y`). An "
            "optional `name` (or `label`/`place`/`site`) column labels the points, and an "
            "optional `category` (or `type`/`group`) column color-codes them. In a PDF, "
            "either a table with the same kind of columns, or plain text with coordinate "
            "pairs on their own lines (e.g. `Site A: 31.52, 74.35`).\n\n"
            "**For the Charts tab:** any CSV table works — just pick which columns to "
            "chart. In a PDF, either a table, or lines like `Wheat: 25000` (label/number "
            "pairs), which is common in simple report summaries."
        )
        example_df = pd.DataFrame({
            "name": ["Islamabad", "Karachi", "Lahore"],
            "lat": [33.70, 24.86, 31.55],
            "lon": [73.10, 67.01, 74.35],
            "category": ["Capital", "Port City", "Capital"],
        })
        st.dataframe(example_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download example CSV",
            example_df.to_csv(index=False).encode("utf-8"),
            file_name="example_locations.csv",
            mime="text/csv",
        )

    uploaded_file = st.file_uploader("Choose a CSV or PDF file", type=["csv", "pdf"])

    if uploaded_file is not None:
        tab_map, tab_charts = st.tabs(["🗺️ Map", "📊 Charts"])

        with tab_map:
            try:
                uploaded_file.seek(0)
            except Exception:
                pass
            try:
                df_points = file_import.load_any(uploaded_file)
            except file_import.FileImportError as e:
                st.info(f"Couldn't plot this file as a map: {e}")
            else:
                st.success(f"Parsed {len(df_points)} location(s) from **{uploaded_file.name}**.")
                st.plotly_chart(
                    map_view.custom_points_map(df_points, title=f"Map — {uploaded_file.name}"),
                    use_container_width=True, config={"scrollZoom": True},
                )
                st.dataframe(df_points, use_container_width=True, hide_index=True)
                st.download_button(
                    "Download parsed data as CSV",
                    df_points.to_csv(index=False).encode("utf-8"),
                    file_name="parsed_locations.csv",
                    mime="text/csv",
                    key="download_map_csv",
                )

        with tab_charts:
            try:
                uploaded_file.seek(0)
            except Exception:
                pass
            try:
                df_raw = file_import.load_any_generic(uploaded_file)
            except file_import.FileImportError as e:
                st.error(str(e))
            else:
                st.success(f"Parsed a {df_raw.shape[0]}×{df_raw.shape[1]} table from **{uploaded_file.name}**.")
                st.dataframe(df_raw, use_container_width=True, hide_index=True)

                all_cols = list(df_raw.columns)
                numeric_cols = df_raw.select_dtypes(include="number").columns.tolist()
                if not numeric_cols:
                    coerced = df_raw.apply(pd.to_numeric, errors="coerce")
                    numeric_cols = [c for c in coerced.columns if coerced[c].notna().any()]

                chart_type = st.selectbox("Chart type", ["Bar", "Pie", "Scatter", "Line"])

                if chart_type == "Bar":
                    x_col = st.selectbox("Category / X axis", all_cols, key="bar_x")
                    y_col = st.selectbox("Value / Y axis", numeric_cols or all_cols, key="bar_y")
                    fig = px.bar(df_raw, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                elif chart_type == "Pie":
                    names_col = st.selectbox("Labels", all_cols, key="pie_names")
                    values_col = st.selectbox("Values", numeric_cols or all_cols, key="pie_values")
                    fig = px.pie(df_raw, names=names_col, values=values_col, title=f"{values_col} share by {names_col}")
                elif chart_type == "Scatter":
                    x_col = st.selectbox("X axis", numeric_cols or all_cols, key="scatter_x")
                    y_col = st.selectbox("Y axis", numeric_cols or all_cols, key="scatter_y")
                    color_choice = st.selectbox("Color by (optional)", ["None"] + all_cols, key="scatter_color")
                    fig = px.scatter(
                        df_raw, x=x_col, y=y_col,
                        color=None if color_choice == "None" else color_choice,
                        title=f"{y_col} vs {x_col}",
                    )
                else:  # Line
                    x_col = st.selectbox("X axis", all_cols, key="line_x")
                    y_col = st.selectbox("Y axis", numeric_cols or all_cols, key="line_y")
                    fig = px.line(df_raw, x=x_col, y=y_col, title=f"{y_col} over {x_col}", markers=True)

                st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
    else:
        st.info("No file uploaded yet — showing example data below.")
        map_tab, chart_tab = st.tabs(["🗺️ Map example", "📊 Chart example"])
        with map_tab:
            example_df = pd.DataFrame({
                "Name": ["Islamabad", "Karachi", "Lahore"],
                "Latitude": [33.70, 24.86, 31.55],
                "Longitude": [73.10, 67.01, 74.35],
                "Category": ["Capital", "Port City", "Capital"],
            })
            st.plotly_chart(
                map_view.custom_points_map(example_df, title="Example — Pakistani Cities"),
                use_container_width=True, config={"scrollZoom": True},
            )
        with chart_tab:
            example_chart_df = pd.DataFrame({
                "Crop": ["Wheat", "Cotton", "Rice", "Sugarcane", "Maize"],
                "Area (000 ha)": [9000, 2100, 2800, 1050, 1500],
            })
            st.plotly_chart(
                px.bar(example_chart_df, x="Crop", y="Area (000 ha)", title="Example — Crop Area"),
                use_container_width=True, config={"scrollZoom": True},
            )

    st.markdown("---")
    st.header("📡 River Basin Telemetry & Water Quality Analytics")
    st.caption(
        "Two lightweight Python analysis engines ship with this project — `telemetry_engine.py` "
        "and `water_quality_engine.py` — importable here, or runnable standalone from the command "
        "line (e.g. `python telemetry_engine.py --days 90 --out chart.png`) to produce a Matplotlib "
        "chart outside the app. Real Indus Waters Treaty PIC-exchanged telemetry isn't publicly "
        "published, so the data below is clearly-labeled illustrative/synthetic unless you analyze "
        "your own uploaded file."
    )

    telemetry_tab, water_quality_tab = st.tabs(
        ["🌊 Telemetry Variance", "🧪 Water Quality (EC · pH · DO)"]
    )

    with telemetry_tab:
        st.subheader("Which river basin reports the highest average telemetry variance?")
        days = st.slider("Days of synthetic telemetry", 30, 365, 90, key="tel_days")
        seed = st.number_input("Random seed (reproducibility)", value=42, step=1, key="tel_seed")
        df_tel = telemetry_engine.generate_synthetic_telemetry(days=days, seed=int(seed))
        group_col, value_col = "Basin", "Discharge_cumecs"
        data_source_note = "Illustrative synthetic daily discharge data (not real PIC-exchanged telemetry)."

        if uploaded_file is not None:
            use_upload = st.checkbox(
                "Analyze my uploaded file's telemetry instead", key="tel_use_upload_cb"
            )
            if use_upload:
                try:
                    uploaded_file.seek(0)
                except Exception:
                    pass
                try:
                    df_uploaded = file_import.load_any_generic(uploaded_file)
                except file_import.FileImportError as e:
                    st.error(str(e))
                else:
                    cat_cols = df_uploaded.select_dtypes(exclude="number").columns.tolist()
                    num_cols = df_uploaded.select_dtypes(include="number").columns.tolist()
                    if cat_cols and num_cols:
                        group_col = st.selectbox("Group / basin column", cat_cols, key="tel_u_group_col")
                        value_col = st.selectbox("Value column", num_cols, key="tel_u_value_col")
                        df_tel = df_uploaded
                        data_source_note = f"Using your uploaded file **{uploaded_file.name}**."
                    else:
                        st.info(
                            "Couldn't find both a categorical (basin/group) column and a numeric "
                            "column in this file — showing illustrative data instead."
                        )

        st.caption(data_source_note)
        summary_df = telemetry_engine.compute_basin_variance(df_tel, value_col=value_col, group_col=group_col)
        top = summary_df.iloc[0]
        st.success(
            f"Highest telemetry variance: **{top[group_col]}** "
            f"(variance = {top['variance']:.1f}, std. dev. = {top['std']:.1f})"
        )
        st.plotly_chart(
            px.bar(
                summary_df, x=group_col, y="variance", color=group_col,
                title=f"Telemetry variance by {group_col}",
            ),
            use_container_width=True, config={"scrollZoom": True},
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with water_quality_tab:
        st.subheader("Water Quality Snapshot — EC · pH · Dissolved Oxygen (DO)")
        st.caption(
            "Illustrative per-basin snapshot, classified against WHO / Pakistan NSDWQ / FAO "
            "guideline thresholds. Change the seed for a new illustrative reading."
        )
        wq_seed = st.number_input("Random seed", value=7, step=1, key="wq_seed")
        df_wq = water_quality_engine.generate_synthetic_water_quality(seed=int(wq_seed))
        df_wq["WQI_composite"] = df_wq.apply(water_quality_engine.composite_water_quality_index, axis=1)
        st.dataframe(df_wq, use_container_width=True, hide_index=True)

        wq_col1, wq_col2, wq_col3 = st.columns(3)
        with wq_col1:
            st.plotly_chart(
                px.bar(df_wq, x="Basin", y="EC_uS_cm", color="EC_class", title="Electrical Conductivity"),
                use_container_width=True, config={"scrollZoom": True},
            )
        with wq_col2:
            st.plotly_chart(
                px.bar(df_wq, x="Basin", y="pH", color="pH_class", title="pH"),
                use_container_width=True, config={"scrollZoom": True},
            )
        with wq_col3:
            st.plotly_chart(
                px.bar(df_wq, x="Basin", y="DO_mg_L", color="DO_class", title="Dissolved Oxygen (DO)"),
                use_container_width=True, config={"scrollZoom": True},
            )

        st.plotly_chart(
            px.bar(
                df_wq, x="Basin", y="WQI_composite",
                title="Composite Water Quality Index (illustrative, equal-weighted across EC/pH/DO)",
            ),
            use_container_width=True, config={"scrollZoom": True},
        )

        with st.expander("📏 Guideline thresholds used"):
            for param, t in water_quality_engine.WATER_QUALITY_THRESHOLDS.items():
                st.markdown(f"**{param}:** {t['note']}")

        with st.expander("📚 Sources for this section"):
            for ref in data.SOURCES.get("Water Quality Guidelines (EC · pH · DO)", []):
                st.markdown(f"- [{ref['label']}]({ref['url']})")

# ---------------------------------------------------------------------------
# 🪖 PAKISTAN ARMY'S ROLE ACROSS SECTORS
# ---------------------------------------------------------------------------
elif choice == "🪖 Pakistan Army's Role Across Sectors":
    st.title("Pakistan Army's Role Across This Project's Sectors")
    st.caption(
        "An explanatory, source-tagged summary — not an official or legal statement. "
        "Contested items are shown as each side's reported position."
    )
    st.info(army_role.FRAMING_NOTE)
    st.caption(army_role.EVIDENCE_NOTE)

    _rows = []
    for _name, _sec in army_role.SECTORS.items():
        _pts = _sec["points"]
        _rows.append({
            "Sector": _name,
            "Related dashboard page": _sec["dashboard_section"],
            "Points": len(_pts),
            "Source-backed": sum(1 for _, t in _pts if t == "Source-backed"),
            "Reported - verify": sum(1 for _, t in _pts if t == "Reported - verify"),
            "Supplied reference": sum(1 for _, t in _pts if t == army_role.SUPPLIED),
        })
    kit.explore(pd.DataFrame(_rows), key="kit_17")

    _icons = {"Source-backed": "✅", "Reported - verify": "🔎", army_role.SUPPLIED: "📄"}
    _aq = st.text_input("🔎 Search all points on this page (keyword)", value="", key="army_search").strip().lower()
    _atag = st.multiselect("Show evidence tags", ["Source-backed", "Reported - verify", army_role.SUPPLIED],
                           default=["Source-backed", "Reported - verify", army_role.SUPPLIED], key="army_tagfilter")
    _tab_names = list(army_role.SECTORS.keys())
    _all_tabs = st.tabs(_tab_names + ["🏛️ Federal Ministries"])
    with _all_tabs[-1]:
        st.subheader("Federal Ministries")
        st.caption("Each federal ministry is shown with the Government of Pakistan state emblem; individual ministry logos "
                   "were not supplied. The page mapping is the project author's navigation aid, not an official statement of mandates.")
        st.markdown(gov_logos.ministries_html(), unsafe_allow_html=True)
        st.markdown("**Ministries and the dashboard pages they relate to**")
        kit.explore(pd.DataFrame(gov_logos.ministries_rows()), key="kit_ministries", chart=False)
    for _tab, _name in zip(_all_tabs[:-1], _tab_names):
        with _tab:
            _sec = army_role.SECTORS[_name]
            st.subheader(_name)
            st.caption(f"Related dashboard page: {_sec['dashboard_section']}")
            if _sec.get("diagram"):
                st.code(_sec["diagram"], language=None)
            for _text, _tag in _sec["points"]:
                if _tag not in _atag or (_aq and _aq not in _text.lower()):
                    continue
                st.markdown(f"- {_icons.get(_tag, '🔎')} {_text}  \n  <sub>*{_tag}*</sub>", unsafe_allow_html=True)
            for _tbl_title, _tbl_rows in _sec.get("tables", []):
                st.markdown(f"**{_tbl_title}**")
                kit.explore(pd.DataFrame(_tbl_rows), key=f"kit_18_{_name}_{_tbl_title}")

    with st.expander("📚 Sources for this section"):
        for _label, _url in army_role.SOURCES:
            st.markdown(f"- [{_label}]({_url})")
        st.caption(army_role.SUPPLIED_SOURCE_NOTE)

    st.header("Armed Forces of Pakistan")
    st.markdown(army_emblems.armed_forces_html(), unsafe_allow_html=True)
    st.subheader("Flags")
    st.markdown(army_emblems.flags_html("Flags"), unsafe_allow_html=True)
    st.subheader("Roundels")
    st.markdown(army_emblems.flags_html("Roundels", 80), unsafe_allow_html=True)
    st.subheader("Emblems")
    st.markdown(army_emblems.flags_html("Emblems", 120), unsafe_allow_html=True)

    st.header("Pakistan Army Coat of Arms")
    st.caption("Corps, regiment and unit emblems supplied by the project owner (reference only). "
               "Names marked 'verify' were identified from the image — please confirm. "
               "The Army's central coat of arms was not supplied.")
    for _grp in army_emblems.GROUPS:
        st.subheader(_grp)
        st.markdown(army_emblems.group_html(_grp), unsafe_allow_html=True)

elif choice == "⚓ Pakistan Navy's Role Across This Project's Sectors":
    _emb = navy_role.emblem_b64()
    st.markdown(
        '<div style="display:flex;align-items:center;gap:14px;">'
        + (f'<img src="data:image/png;base64,{_emb}" style="height:70px;width:auto;" />' if _emb else "")
        + "<h1 style='margin:0;'>Pakistan Navy's Role Across This Project's Sectors</h1></div>",
        unsafe_allow_html=True,
    )
    st.caption(navy_role.NOTE)
    st.header(navy_role.HEADING)
    st.markdown(navy_role.commands_html(), unsafe_allow_html=True)
    _have = len(navy_role.COMMANDS)
    if _have < navy_role.EXPECTED_COMMANDERS:
        st.info(f"{_have} of {navy_role.EXPECTED_COMMANDERS} commander titles added so far — "
                f"the remaining {navy_role.EXPECTED_COMMANDERS - _have} are waiting to be supplied.")
    kit.explore(pd.DataFrame(navy_role.COMMANDS, columns=["Commander title", "Abbreviation"]),
                key="kit_navy_cmds", chart=False)

    st.header("Pakistan Navy Training Establishments")
    st.markdown(security_bodies.group_html("Pakistan Navy Training Establishments", 90), unsafe_allow_html=True)

elif choice in ("☀️ Solar Energy Sectors", "⛏️ Mining Sectors", "🥜 Dry Fruit Sector"):
    _is_solar = choice.startswith("☀️")
    _is_dry = choice.startswith("🥜")
    _data = em.SOLAR if _is_solar else (em.DRYFRUIT if _is_dry else em.MINING)
    _key = "solar" if _is_solar else ("dryfruit" if _is_dry else "mining")
    st.title("☀️ Solar Energy Sectors of Pakistan" if _is_solar else ("🥜 Dry Fruit Sector of Pakistan" if _is_dry else "⛏️ Mining Sectors of Pakistan"))
    st.caption("Source-tagged explanatory summary — indicative figures, not official statistics.")
    st.caption(em.NOTE)
    _icons = {"Source-backed": "✅", "Reported - verify": "🔎", em.SUP: "📄"}

    _summary = [{"Sector": n, "Points": len(d["points"]),
                 "Source-backed": sum(1 for _, t in d["points"] if t == "Source-backed"),
                 "Reported - verify": sum(1 for _, t in d["points"] if t == "Reported - verify"),
                 "Supplied reference": sum(1 for _, t in d["points"] if t == em.SUP),
                 "Mapped sites": len(d.get("sites", []))} for n, d in _data.items()]
    kit.explore(pd.DataFrame(_summary), key="kit_19")

    _all_sites = []
    for _n, _d in _data.items():
        for _s in _d.get("sites", []):
            _all_sites.append({**_s, "Sector": _n})
    if _all_sites:
        _sdf = pd.DataFrame(_all_sites)
        _sdf["Category"] = _sdf["Sector"]
        st.subheader("Map of listed sites (approximate locations)")
        st.plotly_chart(map_view.custom_points_map(_sdf, "Solar projects" if _is_solar else ("Dry-fruit production hubs" if _is_dry else "Mining sites")),
                        use_container_width=True, config={"scrollZoom": True}, key=f"em_map_{_key}")

    _eq = st.text_input("🔎 Search all points on this page (keyword)", value="", key=f"em_search_{_key}").strip().lower()
    _etag = st.multiselect("Show evidence tags", ["Source-backed", "Reported - verify", em.SUP],
                           default=["Source-backed", "Reported - verify", em.SUP], key=f"em_tag_{_key}")
    _names = list(_data.keys())
    for _tab, _n in zip(st.tabs(_names), _names):
        with _tab:
            _d = _data[_n]
            st.subheader(_n)
            for _text, _tag in _d["points"]:
                if _tag not in _etag or (_eq and _eq not in _text.lower()):
                    continue
                st.markdown(f"- {_icons.get(_tag, '🔎')} {_text}  \n  <sub>*{_tag}*</sub>", unsafe_allow_html=True)
            if _d.get("sites"):
                st.markdown("**Listed sites**")
                kit.explore(pd.DataFrame(_d["sites"]), key=f"kit_20_{_key}_{_n}")
    with st.expander("📚 Sources for this section"):
        for _label, _url in (em.DRY_SOURCES if _is_dry else em.SOURCES):
            st.markdown(f"- [{_label}]({_url})")

# ---------------------------------------------------------------------------
# 📚 SOURCES
# ---------------------------------------------------------------------------
elif choice == "🤖 CrewAI Sector Agents":
    st.title("🤖 CrewAI Sector Agents")
    st.caption("An agent team for every sector in this project. Results are drawn as bar graphs, pie charts, scatter plots, "
               "line charts and histograms from the project's own data; an optional CrewAI crew (your own API key) can write a brief. "
               "Figures are curated summaries — verify against primary sources before formal use.")
    crew_agents.render("Dams & Barrages", key="ca_hub", expanded=True, title="🤖 Choose a sector")

elif choice == "🤖 AI Agents (CrewAI)":
    agents_ui.render_page()

elif choice == "🔎 Search Everything":
    st.title("🔎 Search Everything")
    st.caption("One search box across sections, solar / mining / dry-fruit findings, ministries and every logo in the reference panel.")
    _q = st.text_input("Search", value="", key="se_q", placeholder="e.g. Thar, Gwadar, WAPDA, tariff, police…")
    _scope = st.multiselect("Look in", ["Sections", "Solar / Mining / Dry Fruit findings", "Federal ministries", "Logos & bodies"],
                            default=["Sections", "Solar / Mining / Dry Fruit findings", "Federal ministries", "Logos & bodies"], key="se_scope")
    _n = _q.strip().lower()
    if not _n:
        st.info("Type a word above to search.")
    else:
        _hits = 0
        if "Sections" in _scope:
            _r = [s_ for s_ in SECTIONS if _n in s_.lower() and s_ != choice]
            if _r:
                st.subheader("Sections")
                for s_ in _r:
                    st.markdown(f"- {s_}  _(pick it in the sidebar)_")
                _hits += len(_r)
        if "Solar / Mining / Dry Fruit findings" in _scope:
            _rows = []
            for _label, _d in (("Solar", em.SOLAR), ("Mining", em.MINING), ("Dry Fruit", em.DRYFRUIT)):
                for _tab, _v in _d.items():
                    for _txt, _tag in _v.get("points", []):
                        if _n in _txt.lower() or _n in _tab.lower():
                            _rows.append({"Sector": _label, "Tab": _tab, "Finding": _txt, "Evidence": _tag})
            if _rows:
                st.subheader(f"Findings ({len(_rows)})")
                kit.explore(pd.DataFrame(_rows), key="se_find", chart=False, expanded=False)
                _hits += len(_rows)
        if "Federal ministries" in _scope:
            _m = [r for r in gov_logos.ministries_rows() if any(_n in str(v).lower() for v in r.values())]
            if _m:
                st.subheader(f"Ministries ({len(_m)})")
                st.dataframe(pd.DataFrame(_m), use_container_width=True, hide_index=True)
                _hits += len(_m)
        if "Logos & bodies" in _scope:
            _b = security_bodies.rows(_n)
            if _b:
                st.subheader(f"Logos & bodies ({len(_b)})")
                for _g in security_bodies.GROUPS:
                    _h = security_bodies.group_html(_g, 64, _n)
                    if "<img" in _h:
                        st.markdown(f"**{_g}**")
                        st.markdown(_h, unsafe_allow_html=True)
                _hits += len(_b)
        if _hits == 0:
            st.warning("No matches. Try a shorter or different word.")
        else:
            st.success(f"{_hits} match(es) for “{_q.strip()}”.")

elif choice == "📚 Sources":
    st.title("📚 Sources")
    st.caption(
        "Primary and official references behind the geopolitical, CPEC, dam-governance "
        "and Indus Basin Irrigation System content in this dashboard. Everything else "
        "(rivers, mountains, lakes, deserts, climate regions, coordinates) is a curated "
        "summary for visualization — see the accuracy note on the Overview page."
    )
    for topic, refs in data.SOURCES.items():
        st.subheader(topic)
        for ref in refs:
            st.markdown(f"- [{ref['label']}]({ref['url']})")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit · Plotly · NetworkX")
st.sidebar.caption("👤 Created by **Engr. Syed Hassan Iqbal Shah (ELECT/28314)**")

# ---------------------------------------------------------------------------
# 🤖 Sector agents for the current page (above the logo panel)
# ---------------------------------------------------------------------------
if choice != "🤖 CrewAI Sector Agents":
    if st.toggle("🤖 Show sector agents (charts & insights) for this page", value=False, key="ca_on"):
        crew_agents.render(crew_agents.PAGE_TO_SECTOR.get(choice, "Dams & Barrages"), key="ca_page", expanded=True,
                           title="🤖 Sector agents for this page")

# 🤖 Per-section AI agents (charts + findings), shown at the bottom of each data section
if choice != "🤖 AI Agents (CrewAI)":
    agents_ui.render_panel(choice)

# ---------------------------------------------------------------------------
# 🛡️ Interactive logo panel (bottom of every page, above the credit banner)
# ---------------------------------------------------------------------------
with st.expander("🛡️ Law enforcement, security & justice bodies"):
    _pq = st.text_input("Search bodies", value="", key="lp_q", placeholder="e.g. police, PAF, council, WAPDA…")
    _pg = st.multiselect("Groups", security_bodies.GROUPS, default=[], key="lp_g",
                         help="Leave empty to show every group.")
    _pc1, _pc2 = st.columns(2)
    with _pc1:
        _psize = st.slider("Logo size", 40, 140, 78, step=2, key="lp_size")
    with _pc2:
        _pview = st.radio("View", ["Logo grid", "Table"], horizontal=True, key="lp_view")
    _prows = security_bodies.rows(_pq, _pg)
    _m1, _m2, _m3 = st.columns(3)
    _m1.metric("Logos shown", len(_prows))
    _m2.metric("Total logos", len(security_bodies.BODIES))
    _m3.metric("Groups", len({r_["Group"] for r_ in _prows}))
    if _prows:
        st.download_button("⬇️ Download this list (CSV)", pd.DataFrame(_prows).to_csv(index=False).encode("utf-8"),
                           file_name="logo_list.csv", mime="text/csv", key="lp_dl")
    if _pview == "Table":
        st.dataframe(pd.DataFrame(_prows), use_container_width=True, hide_index=True)
    else:
        for _g in (_pg or security_bodies.GROUPS):
            _h = security_bodies.group_html(_g, _psize, _pq)
            if "<img" in _h:
                _cnt = sum(1 for r_ in _prows if r_["Group"] == _g)
                st.markdown(f"**{_g}** · {_cnt}")
                st.markdown(_h, unsafe_allow_html=True)
    if _prows:
        _pick = st.selectbox("🔍 Inspect one logo", [r_["Name"] for r_ in _prows], key="lp_pick")
        _bytes = security_bodies.image_bytes(_pick)
        if _bytes:
            st.image(_bytes, caption=_pick, width=260)
    _short = st.multiselect("📌 Build a shortlist (pin logos to compare side by side)",
                            [b_[0] for b_ in security_bodies.BODIES], default=[], key="lp_short")
    if _short:
        _sc = st.columns(min(len(_short), 4))
        for _i, _n in enumerate(_short):
            with _sc[_i % len(_sc)]:
                _bb = security_bodies.image_bytes(_n)
                if _bb:
                    st.image(_bb, caption=_n, width=150)
    st.caption("Reference only; names marked 'verify' / 'to confirm' were identified from the image. Logos do not imply endorsement.")

st.markdown("---")
# Credit banner shown at the bottom of every page (rendered after all page content).
def _credit_row(b64, mime, img_h, text, size):
    return (
        '<div style="display:flex;align-items:center;gap:6px;margin:2px 0;">'
        f'<img src="data:{mime};base64,{b64}" style="height:{img_h}px;width:auto;display:block;" />'
        f'<span style="font-size:{size}px;font-weight:700;line-height:1.2;">{text}</span></div>'
    )

_uof_b64 = getattr(flag_assets, "UOF_JPG_B64", "")
_uof_text = "BSc Electrical Engineering (Electronic)"
_uof_seal = getattr(flag_assets, "UOF_SEAL_PNG_B64", "")
_uof_row = (
    '<div style="display:flex;align-items:center;gap:6px;margin:2px 0;">'
    + (f'<img src="data:image/jpeg;base64,{_uof_b64}" style="height:64px;width:auto;display:block;" />' if _uof_b64 else '')
    + f'<span style="font-size:20px;font-weight:700;line-height:1.2;">{_uof_text}</span>'
    + (f'<img src="data:image/png;base64,{_uof_seal}" style="height:56px;width:auto;display:block;" />' if _uof_seal else '')
    + '</div>'
)
_ispr_block = (
    '<div style="display:flex;align-items:center;gap:6px;">'
    f'<img src="data:image/png;base64,{flag_assets.ISPR_PNG_B64}" style="height:72px;width:auto;display:block;" />'
    '<span style="font-size:22px;font-weight:700;line-height:1.2;">Dedicated to ISPR</span></div>'
)
st.markdown(
    '<div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;">'
    '<div>'
    + _credit_row(flag_assets.SNAP_JPG_B64, "image/jpeg", 80, "Engr. Syed Hassan Iqbal Shah", 26)
    + _uof_row
    + _credit_row(flag_assets.PEC_PNG_B64, "image/png", 56, "PEC Accredited Engineer", 20)
    + '</div>' + _ispr_block + '</div>',
    unsafe_allow_html=True,
)

