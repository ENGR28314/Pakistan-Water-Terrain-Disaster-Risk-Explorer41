# Pakistan Water, Terrain & Disaster-Risk Explorer

An interactive Streamlit dashboard covering Pakistan's provinces, river
systems, dams/barrages/link canals, climatic regions, mountain ranges,
lakes, deserts, forests, national parks, national disaster-risk context, and
the socio-economic, agro-economic and geo-political dimensions of water
management — including the Indus Waters Treaty, inter-provincial disputes,
CPEC hydropower investment, and India's upstream dam-design disputes.

Created by **Engr. Syed Hassan Iqbal Shah (ELECT/28314)**.

## Maps

Every map in this app is built with Plotly `Scattermap` (the MapLibre-based
trace, `layout.map`) on a free, token-free "open-street-map" tile basemap —
a real slippy map with continuous scroll-wheel/pinch zoom and drag-to-pan,
the way Google Maps behaves (`st.plotly_chart(..., config={"scrollZoom":
True})` everywhere). `Scattermap` is used deliberately instead of the
older, Mapbox-GL-based `Scattermapbox`/`layout.mapbox`, which now requires
a Mapbox access token for any style — including nominally free ones —
under current Mapbox GL JS behavior; `Scattermap`'s MapLibre backend has no
such restriction. True satellite photo imagery (the literal Google *Earth*
look) still needs a Mapbox/Google API token, which this app does not use —
street-map tiles are the closest token-free equivalent. Marker layers are
distinguished by color/size rather than custom icon shapes, since this
token-free raster style doesn't render custom symbol icons.

## Features

- **Provinces** — Gilgit-Baltistan, KPK, Punjab, Sindh, Balochistan, AJK,
  ICT: capitals, area, rivers, climate, mountain ranges, lakes.
- **Rivers** — source, upstream/downstream path, confluences, associated
  infrastructure, an interactive map, and a schematic confluence network
  diagram.
- **Dams & Barrages** — type, river, province, year completed, capacity,
  purpose, plus a schematic irrigation-network diagram.
- **Link Canals** — the Indus Basin Irrigation System's (IBIS) inter-river
  transfer canals (C-J, T-P, T-S, SMB, MB, R-Q, Q-B, B-S).
- **Climatic Regions** — Temperate, Tropical, Polar, Arid, Highland.
- **Mountain Ranges** — Northern Highlands (Karakoram, Himalayas, Hindu
  Kush, Hindu Raj) and Western/Southern Border Ranges (Spin Ghar, Sulaiman,
  Kirthar, Toba Kakar, Salt Range): highest peaks, surrounding areas,
  climbing details, geology, tourist guides, and associated rivers.
- **Lakes** — major lakes across provinces with formation type.
- **Deserts** — Thar, Cholistan, Kharan, Thal, and the Katpana cold desert,
  with province, approximate area, type, and mapped extents.
- **Forests** — the five main forest types (coniferous, mangrove, riverain/
  bela, tropical thorn/scrub, irrigated/planted), plus notable forests
  (Changa Manga, Ziarat Juniper, Ushu, Dir/Kumrat, Soon Valley, Mukshpuri,
  Rama Meadows, Kalam, Chitral, Margalla Hills scrub, etc.) with location,
  covered area, history & origin, wildlife & nature, and attractions.
- **National Parks** — Ayub, Jallo Park, Lulusar-Dudipatsar, Lal Suhanra,
  Kirthar, Khunjerab, Chitral Gol, Hingol, Shakarparian, Pir Lasura,
  Hazarganji-Chiltan, Machiara, Margalla Hills, Rajana/Bhagat Wildlife
  Park, and several municipal recreational parks in Multan/Lahore/
  Islamabad — with province, area, establishment and notes.
- **Indus Delta Soil Salinity (EMI Survey)** — electromagnetic induction
  (EMI) survey and soil-sampling methodology, FAO/Richards salinity-sodicity
  classification thresholds, published depth-wise EC/ESP exceedance
  findings (Solangi et al., 2019), and an interactive map/charts of
  interpolated EC, pH, ESP and salinity class across illustrative sample
  sites in Thatta, Sujawal and Badin districts.
- **WAPDA Telemetry Network** — the real station/facility lists behind the
  Eastern Rivers Wireless Network (surveyed coordinates) and the Western
  Rivers HF Radio Network (approximate fallback coordinates), on an
  interactive map.
- **National Disaster Risk Context** — hazard profile (hydro-meteorological,
  tectonic, climatological/emerging, anthropogenic), exposure & vulnerability
  assessment, emerging risks (GLOFs, erratic monsoons, sea intrusion), and
  baseline / medium / worst-case risk scenarios.
- **Socio-Economic & Agro-Economic Domains** — food security, employment,
  urban growth, tourism, the Indus Basin Irrigation System, GDP linkages,
  the Rabi/Kharif crop-season calendar (crop, typical sowing/harvest window,
  and an engineering/water-demand note per crop), allied agriculture sectors
  (apiculture and aquaculture, each with an indicator/unit/description
  table), and an **editable, input-driven province/region dataset**
  (cultivated area, crop production, employment, honey production,
  aquaculture production) with a Bar/Pie/Scatter/Line chart picker — shown
  under both the Socio-Economic and Agro-Economic headers, sharing the same
  underlying editable table.
- **Geo-Political & Strategic Domains** — Kashmir hydro-politics, the Indus
  Waters Treaty, maritime trade infrastructure, Punjab-vs-Sindh internal
  water disputes, and IRSA/CCI/Supreme Court legal mechanisms.
- **China's CPEC Hydropower Footprint** — Karot, Suki Kinari, Kohala, Azad
  Pattan, with a portfolio network diagram.
- **Chenab Projects, Flow Concerns & Indus Waters Treaty** — Pakal Dul
  (1,000 MW) and Ratle (850 MW) technical contentions (pondage, freeboard,
  spillway design) Pakistan has raised in IWT proceedings; the Head Marala
  flow/crop-impact issue (reported as stakeholder claims, not asserted as a
  causal crop-loss estimate); a dated Court of Arbitration (PCA) timeline
  including the 31 Aug 2026 construction-freeze order and a Pakistan-stated
  note on the Court's validity under Article IX; India's reported proposed
  inter-basin canal/transfer projects (the 113km canal, the Chenab–Ravi–
  Beas–Sutlej and Ravi–Beas link canals, and expedited hydropower
  construction); and a dedicated **"Indian Atrocities" tab** with the
  detailed, specifically-sourced technical dispute figures (pondage,
  spillway, intake-submergence and freeboard numbers at Kishenganga/Ratle),
  the Nov 2026–Jul 2027 Neutral Expert timeline, and the parallel
  Court-of-Arbitration concrete-freeze order alongside India's reported
  non-compliance position — all presented as each side's reported claims,
  not adjudicated fact. Also includes India's own CEA/NHPC-sourced
  inventory of 17 Indus-basin hydropower projects in J&K (10 operational +
  7 under construction, ~6,911.5 MW total), mapped and tabled, kept as a
  separate dataset from the Pakistan-statement-sourced project list since
  the two are independently compiled and may not agree on scope.
- **Indus Waters Treaty map cross-check** — the official WAPDA "Link
  Canals & Barrage" reference map's feature list (link canals, barrages,
  rivers, Line of Control, Working Boundary, Churna Island), shown as a
  cross-check against this dashboard's own data on the Link Canals page.
- **Pakistan Army's Role Across Sectors** (`army_role.py`) — a thirteen-tab,
  source-tagged summary of the Army's role in dams/hydropower (FWO, Corps of
  Engineers), flood management and relief, disaster response, canals and
  agriculture (the Green Pakistan Initiative / Cholistan Canal, with Sindh's
  objections shown alongside), Karakoram/Gilgit-Baltistan connectivity and
  telecom (KKH, SCO), project security (CPEC SSD, planned WAPDA force),
  geo-politics, the wider economy, and forests/lakes/deserts/parks. Each point
  is tagged "Source-backed" or "Reported - verify"; contested items are shown as
  each side's stated position, not adjudicated fact. Includes SIFC/LIMS water
  technology, corporate-farming and Gulf-investment material, the Lahore High
  Court land-lease proceedings and the Army's reported IWT stance, taken from
  reference text supplied by the project owner and tagged "Supplied reference -
  verify" because it cites no individual sources.
- **Interactive Hydraulic Models** — simplified reservoir mass-balance
  simulation, shortage-sharing allocation, link-canal transfer calculator,
  and a composite disaster-risk-index tool.
- **SEBAL Model: Indus Basin Advanced Evapotranspiration Engine** (created
  and designed by Engr. Syed Hassan Iqbal Shah (ELECT/28314)) — an offline, upload-driven
  re-implementation of the published SEBAL/METRIC surface-energy-balance
  algorithm (`sebal_engine.py`): net radiation → NDVI/albedo-based soil
  heat flux → Brutsaert (1982) roughness length → wind extrapolation to the
  200 m blending height → iterative Monin-Obukhov-corrected aerodynamic
  resistance (Paulson 1970 / Webb 1970) → hot/cold anchor-pixel calibration
  of the dT = a + b·Ts relationship (Bastiaanssen et al. 1998; Allen,
  Tasumi & Trezza 2007 METRIC) → sensible/latent heat flux → instantaneous
  and evaporative-fraction-upscaled daily ET (ET24), with an FAO-56 (Allen
  et al. 1998) solar-geometry fallback for days/sites without measured
  daily radiation. Runs entirely on a per-zone/per-pixel table you upload,
  hand-edit, or generate as a clearly-labeled synthetic demo dataset — no
  Google Earth Engine account or live satellite pull is used or required.
  Results include a per-zone table, an ET24 bar chart, an optional map (when
  coordinates are supplied), and CSV/PDF export (the PDF report is built
  with `reportlab`, including an embedded Matplotlib chart). A second
  **"CSV Analytics & Map"** tab on the same page accepts any CSV file(s) —
  not just the SEBAL schema — and builds a **bar, pie, scatter or line
  chart** from any of its columns (same picker as the Upload File tab), and
  automatically plots the file on an **interactive map** whenever it has
  recognizable latitude/longitude columns, so telemetry exports, SEBAL
  results, or any other tabular data can be explored and mapped without
  leaving this page. This is an educational re-implementation from the
  published literature, not derived from any proprietary SEBAL/METRIC
  software — it has not been validated against field lysimeter/eddy-
  covariance data and should not be used
  operationally without independent calibration.
- **Upload File → Map, Charts & Analytics** — upload your own **CSV or PDF**
  and either plot it on an interactive map (needs recognizable latitude/
  longitude columns) or build a **bar, pie, scatter or line chart** from any
  of its columns. PDFs work via table extraction, with a text-based fallback
  (coordinate pairs for the map, `Label: value` lines for charts). The same
  tab also hosts two standalone analysis **engines**:
  - **Telemetry variance engine** (`telemetry_engine.py`) — answers "which
    river basin reports the highest average telemetry variance?" using
    clearly-labeled illustrative daily discharge data (real Indus Waters
    Treaty PIC-exchanged telemetry isn't publicly published), or your own
    uploaded basin/value data.
  - **Water quality engine** (`water_quality_engine.py`) — classifies
    illustrative per-basin **EC, pH and dissolved oxygen (DO)** readings
    against WHO / Pakistan NSDWQ / FAO guideline thresholds and computes a
    simple composite water-quality index.

  Both engines are plain Python modules with no Streamlit dependency — they
  can be imported into other scripts or run standalone from the command
  line to produce a Matplotlib chart, e.g.:
  ```
  python telemetry_engine.py --days 90 --seed 7 --out telemetry_variance.png
  python water_quality_engine.py --seed 3 --out water_quality.png
  ```

## Project structure

```
.
├── app.py                # Main Streamlit application (page/section routing)
├── data_loader.py         # All curated reference data (provinces, rivers, dams,
│                           # canals, climate, mountains, lakes, deserts, forests,
│                           # national parks, disaster risk, socio-economic/agro-
│                           # economic, geo-political, CPEC, India dam disputes)
├── coordinates.py         # Lat/lon reference data used for mapping
├── map_view.py             # Plotly geographic map builders
├── network_view.py         # NetworkX + Plotly schematic network diagrams
├── hydraulic_model.py       # Simplified interactive hydraulic/risk models
├── file_import.py           # CSV/PDF → DataFrame parsing (Upload File → Map, Charts & Analytics tab)
├── telemetry_engine.py       # River-basin telemetry variance analysis/visualization engine (standalone-runnable)
├── telemetry_network.py       # WAPDA telemetry station/facility reference lists (Eastern wireless + Western HF radio)
├── india_hydropower_cea.py     # India's CEA/NHPC-sourced 17-project Indus-basin hydropower inventory (J&K)
├── water_quality_engine.py    # EC/pH/DO water-quality classification & index engine (standalone-runnable)
├── army_role.py               # Pakistan Army's role by sector (source-tagged)
├── flag_assets.py             # Embedded PEC/ISPR emblem images
├── sebal_engine.py            # SEBAL/METRIC evapotranspiration physics pipeline (offline, upload-driven)
├── sebal_report.py            # reportlab PDF report export for a SEBAL run
├── requirements.txt
├── .gitignore
└── README.md
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Data accuracy & scope note

This is an **educational/reference dashboard**. Coordinates are
approximate, and infrastructure figures (capacities, completion years,
allocation percentages) are curated summaries for visualization purposes.
Before using any figure in a formal, legal or engineering context, verify
against primary sources: WAPDA, IRSA, PMD, NDMA/PDMA, the Indus Waters
Treaty (1960) text, and the Water Apportionment Accord (1991). The
interactive hydraulic and risk-index models in the final tab are simplified
teaching tools, not validated simulators. The SEBAL evapotranspiration
engine is likewise a from-the-literature re-implementation (see its
section above) and is not validated against field measurements.

**On `requirements.txt` scope:** the SEBAL module intentionally stays on
`numpy`/`pandas` (already dependencies) plus `reportlab` for PDF export.
It does **not** add `earthengine-api`, `geemap`, `folium`, `geopandas`,
`shapely` or `scikit-learn` — those support a *live* Earth-Engine imagery
pipeline, which this offline/upload-driven implementation doesn't use, and
several of them (`geopandas`/`shapely` especially, via their GDAL/GEOS
system-library dependency) are a common source of Streamlit Cloud build
failures when they aren't actually needed.

## Notes on compiled files

Compiled bytecode files (`.cpython-*.pyc`, under `__pycache__/`) are
generated automatically by Python when the app runs — they are not meant
to be hand-authored or committed, which is why `.gitignore` excludes them.

## ☀️ Solar & ⛏️ Mining Sectors
Two pages (`energy_minerals.py`): solar (utility parks, rooftop/net-metering, off-grid, solar tube wells, floating/canal-top, hydro-solar & green hydrogen, supply chain) and mining (coal, copper-gold, salt/gypsum, limestone, chromite/iron, marble/granite, gemstones, mining–water nexus) with approximate site maps. Items are tagged Source-backed / Reported - verify.

## 🔍 Interactivity (all sectors)
`interactive_kit.py` gives every data table a search box, column and numeric-range filters, sorting, CSV download and a chart builder (bar/line/scatter/pie/histogram). The Army, Solar and Mining pages also have keyword search and evidence-tag filters.

## 🥜 Dry Fruit Sector & expanded Mining
New Dry Fruit page (hubs map, exports, constraints, tariffs) and added Mining tabs (Provincial Ownership Laws, PMIF) from owner-supplied text, tagged "Supplied reference - verify".

## Navigation & logo-panel interactivity
- Sidebar **🔎 Find a section** filters the section list as you type.
- **🔎 Search Everything** page searches sections, solar/mining/dry-fruit findings, ministries and all logos.
- The **🛡️ Law enforcement, security & justice bodies** panel now sits at the bottom of every page (above the credit banner) with search, group filter, logo-size slider, grid/table view and a single-logo inspector.

## 🤖 CrewAI sector agents
- New page **🤖 CrewAI Sector Agents** plus a per-page toggle at the bottom of every page (above the logo panel).
- Covers: provinces, rivers, dams & barrages, link canals, lakes, deserts, national parks, disaster events/hazards, agro-socio-economic, Indus Delta soil, Army role, solar, mining and dry fruit.
- Built-in agents (Data Profiler, Chart Planner, Insight Analyst, Chart Builder) need no API key and draw bar graphs, pie charts, scatter plots, line charts and histograms, plus a "build your own chart" tool and CSV download.
- Optional CrewAI crew (Sector Data Analyst -> Chart Strategist -> Briefing Writer): `pip install -r requirements-crewai.txt`, then enter a model name and your own API key on the page. Keys are used for that run only and are not stored.

## 🤖 AI agents for every sector
- **AI Agents (CrewAI)** page and a "🤖 AI agents for this section" panel at the bottom of each data section.
- 20 sector tables (provinces, rivers, dams, link canals, climate, peaks, lakes, deserts, forests, parks, Indus-delta salinity,
  disaster events/hazards, socio-economic, CPEC hydropower, India projects, Army role, solar, mining, dry fruit) + your own CSV.
- Output: bar, pie, scatter, line and histogram charts (only where the data supports them), findings, caveats, Markdown/CSV downloads.
- **Rule-based agents** (default): Profiler -> Analyst -> Chart Planner -> Reviewer; offline, no key, every number computed from the table.
- **CrewAI crew** (optional): `pip install -r requirements-agents.txt`, then choose "CrewAI crew + LLM" and enter your own API key
  (or put it in Streamlit secrets as OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY). The LLM's chart plan is validated against
  the real columns before drawing; if it is unusable the rule-based planner is used. Not part of the offline test harness.
