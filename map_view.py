"""
map_view.py
Plotly-based map rendering helpers for the Streamlit app.

All maps use go.Scattermap (Plotly's MapLibre-based map trace, layout.map)
on a tile-based "open-street-map" basemap — a free, no-API-key OSM raster
style — instead of the old Scattergeo country-silhouette projection. This
gives continuous scroll-wheel/pinch zoom and pan, the same way Google
Maps/Earth behaves — streamlit's plotly_chart is called with
config={"scrollZoom": True} in app.py so the mouse wheel zooms instead of
scrolling the page.

go.Scattermap/layout.map (not the older, Mapbox-GL-based
go.Scattermapbox/layout.mapbox, which this app deliberately avoids) is
Plotly's current, actively-maintained map API as of Plotly 5.24+; requires
plotly>=5.24.0 (see requirements.txt). The older Scattermapbox trace
depends on Mapbox GL JS, which in current releases requires a Mapbox
access token for ANY style including nominally "free" ones like
"open-street-map" — Scattermap's MapLibre backend does not have that
restriction, which is why it's used here instead.

Note on basemap: "open-street-map" is a free, no-API-key street-map tile
style. True satellite photo imagery (the literal Google Earth look)
requires a Mapbox/Google API token, which this app does not use —
street-map tiles are the closest token-free equivalent.

Marker "symbol" shapes (stars, triangles, etc.) are NOT used here because
Scattermap only renders custom symbol icons on a token-gated vector style;
on token-free raster styles like "open-street-map" they silently fail to
render. Layers are instead distinguished by marker color/size. Likewise
Scattermap lines don't support a "dash" style or polygon "fill" — only
width/color — so dashed lines and shaded desert outlines from the old
Scattergeo version are drawn as solid outlines/lines instead.
"""

import math

import plotly.graph_objects as go
from coordinates import (
    PROVINCE_COORDS, RIVER_COORDS, DAM_COORDS, MOUNTAIN_PEAK_COORDS, LAKE_COORDS,
    LINK_CANAL_LINES, CLIMATE_REGION_POINTS, GEOPOLITICAL_COORDS,
    INDIA_DISPUTED_DAM_COORDS, CPEC_HYDROPOWER_NAMES, HISTORICAL_EVENT_COORDS,
    CONFLUENCE_COORDS, DESERT_COORDS, DESERT_OUTLINES, NOTABLE_FOREST_COORDS,
    NATIONAL_PARK_COORDS, INDUS_DELTA_SITE_COORDS, TELEMETRY_FALLBACK_COORDS,
)

PAK_CENTER = {"lat": 30.3753, "lon": 69.3451}
MAP_STYLE = "open-street-map"


def _fit_bounds(lats, lons, pad_factor: float = 1.6, min_zoom: float = 1.0, max_zoom: float = 14.0):
    """
    Compute an approximate (center, zoom) pair that fits all given points —
    the go.Scattermap/layout.map equivalent of Scattergeo's
    fitbounds="locations". Heuristic, not survey-grade:
    zoom = log2(360 / padded angular span).
    """
    lats = [v for v in lats if v is not None]
    lons = [v for v in lons if v is not None]
    if not lats or not lons:
        return dict(PAK_CENTER), 4.6
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)
    center = {"lat": (lat_min + lat_max) / 2, "lon": (lon_min + lon_max) / 2}
    span = max(lat_max - lat_min, lon_max - lon_min, 0.02) * pad_factor
    zoom = math.log2(360.0 / span)
    zoom = max(min_zoom, min(max_zoom, zoom))
    return center, zoom


def _base_figure(title: str, center: dict = None, zoom: float = 4.6, height: int = 600) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        map=dict(
            style=MAP_STYLE,
            center=center or PAK_CENTER,
            zoom=zoom,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=height,
        legend=dict(bgcolor="rgba(255,255,255,0.8)"),
    )
    return fig


def province_overview_map() -> go.Figure:
    fig = _base_figure("Provinces of Pakistan — Capitals")
    lats = [v["lat"] for v in PROVINCE_COORDS.values()]
    lons = [v["lon"] for v in PROVINCE_COORDS.values()]
    names = [f"{k} (Capital: {v['capital']})" for k, v in PROVINCE_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text",
        marker=dict(size=14, color="crimson"),
        textposition="top center", name="Provinces", hoverinfo="text",
    ))
    return fig


def rivers_map(selected_rivers=None) -> go.Figure:
    fig = _base_figure("Major Rivers of Pakistan")
    rivers = RIVER_COORDS if not selected_rivers else {
        k: v for k, v in RIVER_COORDS.items() if k in selected_rivers
    }
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896",
    ]
    for i, (name, points) in enumerate(rivers.items()):
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines+markers", name=name,
            line=dict(width=3, color=palette[i % len(palette)]),
            marker=dict(size=5), hoverinfo="name",
        ))
    return fig


def dams_barrages_map(selected=None) -> go.Figure:
    fig = _base_figure("Dams, Barrages & Hydropower Projects")
    items = DAM_COORDS if not selected else {k: v for k, v in DAM_COORDS.items() if k in selected}
    lats = [v["lat"] for v in items.values()]
    lons = [v["lon"] for v in items.values()]
    names = [f"{k} ({v['river']}, {v['province']})" for k, v in items.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers",
        marker=dict(size=13, color="darkgreen"),
        name="Dams / Barrages / Hydropower",
        hovertext=names, hoverinfo="text",
    ))
    return fig


def mountains_map() -> go.Figure:
    fig = _base_figure("Highest Peaks by Mountain Range")
    lats = [v["lat"] for v in MOUNTAIN_PEAK_COORDS.values()]
    lons = [v["lon"] for v in MOUNTAIN_PEAK_COORDS.values()]
    names = [f"{k} — {v['elevation_m']} m" for k, v in MOUNTAIN_PEAK_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text",
        marker=dict(size=12, color="saddlebrown"),
        textposition="top center", name="Peaks", hoverinfo="text",
    ))
    return fig


def lakes_map() -> go.Figure:
    fig = _base_figure("Lakes of Pakistan")
    lats = [v["lat"] for v in LAKE_COORDS.values()]
    lons = [v["lon"] for v in LAKE_COORDS.values()]
    names = [f"{k} ({v['province']})" for k, v in LAKE_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers",
        marker=dict(size=12, color="dodgerblue"),
        hovertext=names, hoverinfo="text", name="Lakes",
    ))
    return fig


def deserts_map() -> go.Figure:
    fig = _base_figure("Deserts of Pakistan")
    # Approximate extent outline (no polygon fill on Scattermap — drawn as a closed line loop)
    for name, outline in DESERT_OUTLINES.items():
        lats = [p[0] for p in outline]
        lons = [p[1] for p in outline]
        if lats and (lats[0], lons[0]) != (lats[-1], lons[-1]):
            lats = lats + [lats[0]]
            lons = lons + [lons[0]]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines",
            line=dict(width=2, color="rgba(180, 140, 40, 0.8)"),
            name=f"{name} (approx. extent)", hoverinfo="name",
        ))
    lats = [v["lat"] for v in DESERT_COORDS.values()]
    lons = [v["lon"] for v in DESERT_COORDS.values()]
    names = [f"{k} ({v['province']})" for k, v in DESERT_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text",
        marker=dict(size=13, color="#c68b28"),
        textposition="bottom center", name="Deserts", hoverinfo="text",
    ))
    return fig


def combined_overview_map() -> go.Figure:
    """One map layering provinces, rivers, dams and peaks for a quick overview."""
    fig = _base_figure("Pakistan — Combined Water & Terrain Overview")

    for name, points in RIVER_COORDS.items():
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines", name=name,
            line=dict(width=2, color="#1f77b4"), showlegend=False,
            hoverinfo="name",
        ))

    dam_lats = [v["lat"] for v in DAM_COORDS.values()]
    dam_lons = [v["lon"] for v in DAM_COORDS.values()]
    dam_names = list(DAM_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=dam_lats, lon=dam_lons, text=dam_names, mode="markers",
        marker=dict(size=9, color="darkgreen"),
        name="Dams / Barrages", hoverinfo="text",
    ))

    peak_lats = [v["lat"] for v in MOUNTAIN_PEAK_COORDS.values()]
    peak_lons = [v["lon"] for v in MOUNTAIN_PEAK_COORDS.values()]
    peak_names = list(MOUNTAIN_PEAK_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=peak_lats, lon=peak_lons, text=peak_names, mode="markers",
        marker=dict(size=9, color="saddlebrown"),
        name="Major Peaks", hoverinfo="text",
    ))

    prov_lats = [v["lat"] for v in PROVINCE_COORDS.values()]
    prov_lons = [v["lon"] for v in PROVINCE_COORDS.values()]
    prov_names = list(PROVINCE_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=prov_lats, lon=prov_lons, text=prov_names, mode="markers",
        marker=dict(size=12, color="crimson"),
        name="Provinces", hoverinfo="text",
    ))

    desert_lats = [v["lat"] for v in DESERT_COORDS.values()]
    desert_lons = [v["lon"] for v in DESERT_COORDS.values()]
    desert_names = list(DESERT_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=desert_lats, lon=desert_lons, text=desert_names, mode="markers",
        marker=dict(size=9, color="#c68b28"),
        name="Deserts", hoverinfo="text",
    ))
    return fig


def climatic_regions_map() -> go.Figure:
    fig = _base_figure("Climatic Regions of Pakistan")
    palette = {
        "Temperate": "#2ca02c", "Tropical": "#ff7f0e", "Polar": "#17becf",
        "Arid": "#d62728", "Highland": "#9467bd",
    }
    for region, points in CLIMATE_REGION_POINTS.items():
        lats = [p["lat"] for p in points]
        lons = [p["lon"] for p in points]
        labels = [p["label"] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, text=labels, mode="markers", name=region,
            marker=dict(size=13, color=palette.get(region, "gray")),
            hovertext=[f"{region}: {l}" for l in labels], hoverinfo="text",
        ))
    return fig


def link_canals_map() -> go.Figure:
    fig = _base_figure("Link Canals — Indus Basin Irrigation System (IBIS)")
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f",
    ]
    for i, (name, pts) in enumerate(LINK_CANAL_LINES.items()):
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines+markers", name=name,
            line=dict(width=4, color=palette[i % len(palette)]),
            marker=dict(size=7),
            hovertext=name, hoverinfo="text",
        ))
    # overlay the main rivers faintly for geographic context
    for river, points in RIVER_COORDS.items():
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines", showlegend=False,
            line=dict(width=1.5, color="rgba(100,150,220,0.5)"), hoverinfo="skip",
        ))
    return fig


def geopolitical_map() -> go.Figure:
    fig = _base_figure("Geo-Political & Strategic Water Infrastructure")
    color_by_type = {
        "Indian upstream project": "#d62728",
        "Pakistan headworks": "#2ca02c",
        "Pakistan hydropower": "#1f77b4",
        "Maritime trade infrastructure": "#9467bd",
        "Regional context": "#7f7f7f",
    }
    by_type = {}
    for name, info in GEOPOLITICAL_COORDS.items():
        by_type.setdefault(info["type"], {"lat": [], "lon": [], "text": []})
        by_type[info["type"]]["lat"].append(info["lat"])
        by_type[info["type"]]["lon"].append(info["lon"])
        by_type[info["type"]]["text"].append(name)
    for t, d in by_type.items():
        fig.add_trace(go.Scattermap(
            lat=d["lat"], lon=d["lon"], text=d["text"], mode="markers", name=t,
            marker=dict(size=13, color=color_by_type.get(t, "gray")),
            hovertext=d["text"], hoverinfo="text",
        ))
    return fig


def india_dam_disputes_map() -> go.Figure:
    fig = _base_figure("India's Upstream Dam Projects — Pakal Dul & Ratle (Chenab Basin)")
    lats = [v["lat"] for v in INDIA_DISPUTED_DAM_COORDS.values()]
    lons = [v["lon"] for v in INDIA_DISPUTED_DAM_COORDS.values()]
    names = [f"{k} — {v['capacity_MW']} MW ({v['river']})" for k, v in INDIA_DISPUTED_DAM_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text", name="Disputed upstream dams",
        marker=dict(size=15, color="crimson"),
        textposition="bottom center", hoverinfo="text",
    ))
    # Show Marala Headworks (Pakistan's downstream receiving point) for context
    fig.add_trace(go.Scattermap(
        lat=[DAM_COORDS["Marala Headworks"]["lat"]], lon=[DAM_COORDS["Marala Headworks"]["lon"]],
        text=["Marala Headworks (Pakistan, downstream)"], mode="markers+text", name="Downstream (Pakistan)",
        marker=dict(size=13, color="#2ca02c"), textposition="top center",
        hoverinfo="text",
    ))
    lats_line = [INDIA_DISPUTED_DAM_COORDS["Ratle Dam (India)"]["lat"], DAM_COORDS["Marala Headworks"]["lat"]]
    lons_line = [INDIA_DISPUTED_DAM_COORDS["Ratle Dam (India)"]["lon"], DAM_COORDS["Marala Headworks"]["lon"]]
    fig.add_trace(go.Scattermap(
        lat=lats_line, lon=lons_line, mode="lines", showlegend=False,
        line=dict(width=2, color="rgba(200,50,50,0.5)"), hoverinfo="skip",
    ))
    return fig


def china_hydropower_map() -> go.Figure:
    fig = _base_figure("CPEC Hydropower Portfolio — China-Financed Projects")
    items = {k: v for k, v in DAM_COORDS.items() if k in CPEC_HYDROPOWER_NAMES}
    lats = [v["lat"] for v in items.values()]
    lons = [v["lon"] for v in items.values()]
    names = [f"{k} ({v['river']}, {v['province']})" for k, v in items.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text", name="CPEC Hydropower Projects",
        marker=dict(size=15, color="#de2910"),
        textposition="top center", hoverinfo="text",
    ))
    return fig


def historical_events_map() -> go.Figure:
    fig = _base_figure("Historical Disaster Events — Timeline Map")
    lats = [v["lat"] for v in HISTORICAL_EVENT_COORDS.values()]
    lons = [v["lon"] for v in HISTORICAL_EVENT_COORDS.values()]
    names = [f"{k} ({v['year']})" for k, v in HISTORICAL_EVENT_COORDS.items()]
    years = [v["year"] for v in HISTORICAL_EVENT_COORDS.values()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text", name="Historical Events",
        marker=dict(
            size=16, color=years, colorscale="OrRd", showscale=True,
            colorbar=dict(title="Year"),
        ),
        textposition="top center", hoverinfo="text",
    ))
    return fig


def river_confluence_geomap() -> go.Figure:
    """Real-map version: rivers plus labeled confluence points."""
    fig = _base_figure("River Confluence Points (geographic)")
    for river, points in RIVER_COORDS.items():
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines", name=river,
            line=dict(width=2.5), hoverinfo="name",
        ))
    conf_lats = [v["lat"] for v in CONFLUENCE_COORDS.values()]
    conf_lons = [v["lon"] for v in CONFLUENCE_COORDS.values()]
    conf_names = list(CONFLUENCE_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=conf_lats, lon=conf_lons, text=conf_names, mode="markers", name="Confluences",
        marker=dict(size=12, color="black"),
        hovertext=conf_names, hoverinfo="text",
    ))
    return fig


def irrigation_network_geomap() -> go.Figure:
    """Real-map version: rivers, barrages/dams and link canals together."""
    fig = _base_figure("Irrigation & Hydropower Network (geographic)")
    for river, points in RIVER_COORDS.items():
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines", showlegend=False,
            line=dict(width=1.5, color="rgba(31,119,180,0.5)"), hoverinfo="skip",
        ))
    for name, pts in LINK_CANAL_LINES.items():
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, mode="lines", name=name,
            line=dict(width=3, color="#ff7f0e"), hoverinfo="name",
        ))
    dam_lats = [v["lat"] for v in DAM_COORDS.values()]
    dam_lons = [v["lon"] for v in DAM_COORDS.values()]
    dam_names = list(DAM_COORDS.keys())
    fig.add_trace(go.Scattermap(
        lat=dam_lats, lon=dam_lons, text=dam_names, mode="markers", name="Dams / Barrages / Hydropower",
        marker=dict(size=10, color="darkgreen"), hoverinfo="text",
    ))
    return fig


def custom_points_map(df, title: str = "Uploaded Data on Map") -> go.Figure:
    """
    Build a map from a user-supplied DataFrame with 'Name', 'Latitude' and
    'Longitude' columns (see file_import.py, which produces this shape from
    an uploaded CSV or PDF). Any extra columns are shown in the hover text.
    An optional 'Category' column splits points into separate colored traces.
    The view auto-fits to the plotted points instead of staying pinned to
    Pakistan, since uploaded data may cover any part of the world.
    """
    center, zoom = _fit_bounds(list(df["Latitude"]), list(df["Longitude"]))
    fig = _base_figure(title, center=center, zoom=zoom)

    hover_cols = [c for c in df.columns if c not in {"Latitude", "Longitude", "Category"}]
    hovertext = df.apply(
        lambda r: "<br>".join(f"{c}: {r[c]}" for c in hover_cols), axis=1
    )

    if "Category" in df.columns:
        palette = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        ]
        for i, (cat, grp) in enumerate(df.groupby("Category")):
            fig.add_trace(go.Scattermap(
                lat=grp["Latitude"], lon=grp["Longitude"], mode="markers",
                text=hovertext.loc[grp.index], hoverinfo="text", name=str(cat),
                marker=dict(size=11, color=palette[i % len(palette)]),
            ))
    else:
        fig.add_trace(go.Scattermap(
            lat=df["Latitude"], lon=df["Longitude"], mode="markers",
            text=hovertext, hoverinfo="text", name="Uploaded points",
            marker=dict(size=12, color="#e6550d"),
        ))

    return fig


def telemetry_network_map(eastern_stations, western_stations) -> go.Figure:
    """
    Map WAPDA's flood-forecasting telemetry network: Eastern Rivers wireless
    stations (surveyed coordinates, from telemetry_network.EASTERN_RIVERS_WIRELESS_STATIONS)
    and Western Rivers HF radio stations (approximate fallback coordinates,
    from telemetry_network.WESTERN_RIVERS_HF_RADIO_STATIONS + coordinates.TELEMETRY_FALLBACK_COORDS).
    """
    fig = _base_figure("WAPDA Flood-Forecasting Telemetry Network")

    e_lats = [s["lat"] for s in eastern_stations]
    e_lons = [s["lon"] for s in eastern_stations]
    e_names = [s["location"] for s in eastern_stations]
    fig.add_trace(go.Scattermap(
        lat=e_lats, lon=e_lons, text=e_names, mode="markers", hoverinfo="text",
        name="Eastern Rivers — Wireless Network (surveyed)",
        marker=dict(size=10, color="#1f77b4"),
    ))

    w_lats, w_lons, w_names = [], [], []
    for s in western_stations:
        coord = TELEMETRY_FALLBACK_COORDS.get(s["facility"])
        if not coord:
            continue
        w_lats.append(coord["lat"])
        w_lons.append(coord["lon"])
        w_names.append(f"{s['facility']} (approx. location)")
    fig.add_trace(go.Scattermap(
        lat=w_lats, lon=w_lons, text=w_names, mode="markers", hoverinfo="text",
        name="Western Rivers — HF Radio Network (approximate)",
        marker=dict(size=10, color="#d62728"),
    ))

    return fig


def forests_map() -> go.Figure:
    fig = _base_figure("Notable Forests of Pakistan")
    lats = [v["lat"] for v in NOTABLE_FOREST_COORDS.values()]
    lons = [v["lon"] for v in NOTABLE_FOREST_COORDS.values()]
    names = [f"{k} ({v['province']})" for k, v in NOTABLE_FOREST_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers+text",
        marker=dict(size=12, color="#2e7d32"),
        textposition="top center", name="Notable Forests", hoverinfo="text",
    ))
    return fig


def national_parks_map() -> go.Figure:
    fig = _base_figure("National Parks & Major Recreational Parks of Pakistan")
    lats = [v["lat"] for v in NATIONAL_PARK_COORDS.values()]
    lons = [v["lon"] for v in NATIONAL_PARK_COORDS.values()]
    names = [f"{k} ({v['province']})" for k, v in NATIONAL_PARK_COORDS.items()]
    fig.add_trace(go.Scattermap(
        lat=lats, lon=lons, text=names, mode="markers",
        marker=dict(size=11, color="#1565c0"),
        name="Parks", hoverinfo="text",
    ))
    return fig


def single_park_map(name: str, lat: float, lon: float, zoom: float = 10.0) -> go.Figure:
    """Zoomed-in map highlighting one selected national/recreational park.
    Fully pannable/zoomable — this starting zoom is just where it opens."""
    fig = _base_figure(f"{name} — Location", center={"lat": lat, "lon": lon}, zoom=zoom, height=450)
    fig.add_trace(go.Scattermap(
        lat=[lat], lon=[lon], text=[name], mode="markers+text",
        marker=dict(size=16, color="#1565c0"),
        textposition="top center", name=name, hoverinfo="text",
    ))
    return fig


def indus_delta_soil_map(sample_sites) -> go.Figure:
    """
    Map the Indus Delta soil-salinity sample sites (see
    data_loader.INDUS_DELTA_SAMPLE_SITES), color-coded by salinity/sodicity
    classification, with EC/pH/ESP shown on hover.
    """
    all_lats, all_lons = [], []
    for rec in sample_sites:
        c = INDUS_DELTA_SITE_COORDS.get(rec["site"])
        if c:
            all_lats.append(c["lat"])
            all_lons.append(c["lon"])
    center, zoom = _fit_bounds(all_lats, all_lons)
    fig = _base_figure("Indus Delta Soil Salinity — Sample Sites", center=center, zoom=zoom)

    class_colors = {
        "Normal (non-saline, non-sodic)": "#2ca02c",
        "Saline soil": "#ff7f0e",
        "Sodic soil": "#9467bd",
        "Saline-sodic soil": "#d62728",
    }

    by_class = {}
    for rec in sample_sites:
        by_class.setdefault(rec["classification"], []).append(rec)

    for cls, records in by_class.items():
        lats, lons, texts = [], [], []
        for rec in records:
            coord = INDUS_DELTA_SITE_COORDS.get(rec["site"])
            if not coord:
                continue
            lats.append(coord["lat"])
            lons.append(coord["lon"])
            texts.append(
                f"{rec['site']} ({rec['district']})<br>"
                f"EC: {rec['EC_dS_per_m']} dS/m<br>pH: {rec['pH']}<br>ESP: {rec['ESP_pct']}%"
            )
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, text=texts, mode="markers", hoverinfo="text",
            name=cls,
            marker=dict(size=12, color=class_colors.get(cls, "#1f77b4")),
        ))

    return fig


def india_hydropower_cea_map(projects) -> go.Figure:
    """
    Map India's CEA/NHPC-listed 17 Indus-basin hydropower projects in
    Jammu & Kashmir (see india_hydropower_cea.PROJECTS), color-coded by
    status (Operational vs Under Construction), sized by capacity.
    """
    lats = [p["lat"] for p in projects if p.get("lat") is not None]
    lons = [p["lon"] for p in projects if p.get("lon") is not None]
    center, zoom = _fit_bounds(lats, lons, pad_factor=1.8)
    fig = _base_figure(
        "India's CEA-Listed Indus-Basin Hydropower Projects (J&K)", center=center, zoom=zoom
    )
    status_colors = {"Operational": "#1f77b4", "Under Construction": "#d62728"}
    by_status = {}
    for p in projects:
        if p.get("lat") is None:
            continue
        by_status.setdefault(p["status"], []).append(p)
    for status, plist in by_status.items():
        lats = [p["lat"] for p in plist]
        lons = [p["lon"] for p in plist]
        texts = [f"{p['name']} — {p['capacity_MW']} MW ({p['river']}, {p['district']})" for p in plist]
        sizes = [8 + (p["capacity_MW"] or 0) / 60 for p in plist]
        fig.add_trace(go.Scattermap(
            lat=lats, lon=lons, text=texts, mode="markers", hoverinfo="text",
            name=status, marker=dict(size=sizes, color=status_colors.get(status, "gray")),
        ))
    return fig
