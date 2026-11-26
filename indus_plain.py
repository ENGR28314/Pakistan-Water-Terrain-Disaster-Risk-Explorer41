"""
indus_plain.py
Section: Indus Plain - geographic location & boundaries, major divisions (Upper / Lower),
schematic doab cross-section, waterlogging & salinity, and Rabi vs Kharif cropping.

The maps and diagrams are SCHEMATIC drawings (matplotlib, no map tiles). Boundary lines and
river courses are simplified for explanation; they are not survey-grade GIS data.
The descriptive text was supplied by the project owner as reference material.
"""

import numpy as np
import pandas as pd
import streamlit as st

NOTE = ("Reference material supplied by the project owner. The drawings are schematic "
        "(simplified boundaries and river courses) - not survey-grade GIS data.")

# ------------------------------------------------------------------ geometry (lon, lat)
# Pakistan part of the plain, split at Mithankot (where the Panjnad joins the Indus).
UPPER = [(75.1, 32.4), (74.6, 32.8), (73.9, 32.7), (73.1, 32.8), (72.4, 32.75), (71.7, 32.95),
         (71.0, 32.8), (70.7, 32.2), (70.35, 31.4), (70.05, 30.5), (69.85, 29.6), (69.9, 28.9),
         (71.2, 28.9), (72.9, 29.2), (73.8, 30.0), (74.5, 31.1), (74.6, 31.6), (74.9, 32.1)]
LOWER = [(69.9, 28.9), (71.2, 28.9), (70.4, 28.0), (69.6, 27.4), (69.2, 26.5), (69.4, 25.6),
         (69.0, 24.7), (68.6, 24.2), (68.0, 23.8), (67.3, 23.9), (67.2, 24.6), (67.6, 25.2),
         (67.8, 26.0), (67.7, 26.9), (67.9, 27.6), (68.4, 28.2), (68.9, 28.7)]
HIGHLAND = [(66.0, 25.3), (67.5, 25.2), (67.8, 26.0), (67.7, 26.9), (67.9, 27.6), (68.4, 28.2),
            (68.9, 28.7), (69.9, 28.9), (69.85, 29.6), (70.05, 30.5), (70.35, 31.4), (70.7, 32.2),
            (71.0, 32.8), (71.7, 32.95), (72.4, 32.75), (73.1, 32.8), (73.9, 32.7), (74.6, 32.8),
            (75.1, 32.4), (76.5, 32.4), (76.5, 34.0), (66.0, 34.0)]
SEA = [(66.0, 23.0), (70.0, 23.0), (69.0, 23.7), (68.2, 23.8), (67.3, 23.9), (67.2, 24.6),
       (66.8, 24.8), (66.0, 25.2)]
DESERT = [(71.2, 28.9), (70.4, 28.0), (69.6, 27.4), (69.2, 26.5), (69.4, 25.6), (69.0, 24.7),
          (68.6, 24.2), (69.8, 23.6), (75.0, 23.6), (75.0, 28.6), (73.8, 30.0), (72.9, 29.2)]

RIVERS = {
    "Indus": [(71.5, 32.9), (71.35, 32.0), (71.0, 31.0), (70.85, 30.5), (70.4, 29.0),
              (69.7, 28.4), (68.86, 27.7), (68.3, 25.4), (67.92, 24.75), (67.4, 24.0)],
    "Jhelum": [(73.7, 32.9), (73.0, 32.5), (72.4, 31.7), (72.15, 31.15)],
    "Chenab": [(74.45, 32.67), (73.9, 32.0), (72.15, 31.15), (71.2, 30.0), (71.02, 29.35)],
    "Ravi": [(75.0, 32.3), (74.35, 31.6), (73.2, 30.9), (72.0, 30.6), (71.6, 30.3)],
    "Sutlej": [(74.55, 31.1), (73.9, 30.3), (72.5, 29.55), (71.7, 29.4), (71.02, 29.35)],
    "Panjnad": [(71.02, 29.35), (70.37, 28.93)],
}
CITIES = {"Lahore": (74.35, 31.55), "Multan": (71.47, 30.2), "Mithankot": (70.37, 28.93),
          "Sukkur": (68.86, 27.7), "Hyderabad": (68.37, 25.4), "Thatta": (67.92, 24.75)}


def _poly(ax, pts, **kw):
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon(pts, closed=True, **kw))


def plain_map(mode="boundaries"):
    """mode = 'boundaries' (one colour + boundary notes) or 'divisions' (Upper / Lower + doabs)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8.6, 8.4))
    ax.set_xlim(66.0, 76.5)
    ax.set_ylim(23.0, 34.0)
    ax.set_aspect(1 / np.cos(np.radians(29)))
    ax.set_facecolor("#f4f1ea")

    _poly(ax, HIGHLAND, fc="#d8c3a5", ec="none", alpha=0.75, zorder=1)
    _poly(ax, SEA, fc="#bfe0f2", ec="none", zorder=1)
    _poly(ax, DESERT, fc="#f3e3a4", ec="none", alpha=0.8, zorder=1)

    if mode == "divisions":
        _poly(ax, UPPER, fc="#8fcf8a", ec="#2f6f2f", lw=1.6, alpha=0.9, zorder=2)
        _poly(ax, LOWER, fc="#f6b26b", ec="#a85b00", lw=1.6, alpha=0.9, zorder=2)
    else:
        _poly(ax, UPPER, fc="#9ad59a", ec="#2f6f2f", lw=1.6, alpha=0.9, zorder=2)
        _poly(ax, LOWER, fc="#9ad59a", ec="#2f6f2f", lw=1.6, alpha=0.9, zorder=2)

    # mountain ranges / plateau lines
    ax.plot([71.0, 70.4, 69.95, 69.8], [32.5, 31.4, 30.4, 29.4], color="#7b4a1e", lw=7, alpha=0.55,
            solid_capstyle="round", zorder=3)
    ax.plot([67.45, 67.3, 67.15], [27.1, 26.2, 25.2], color="#7b4a1e", lw=7, alpha=0.55,
            solid_capstyle="round", zorder=3)
    ax.plot([71.7, 72.5, 73.3], [33.05, 33.0, 33.05], color="#7b4a1e", lw=6, alpha=0.55,
            solid_capstyle="round", zorder=3)

    for name, pts in RIVERS.items():
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color="#1f6fb5", lw=2.4 if name == "Indus" else 1.6, zorder=4)
    for name, (x, y) in CITIES.items():
        ax.plot(x, y, "o", color="#222", ms=4, zorder=5)
        ax.text(x + 0.12, y - 0.05, name, fontsize=7.5, zorder=6)

    kw = dict(fontsize=8, ha="center", va="center", zorder=7)
    ax.text(68.4, 30.6, "BALOCHISTAN\nPLATEAU", color="#6b4a1e", fontweight="bold", **kw)
    ax.text(69.55, 31.3, "Sulaiman\nRange", color="#4a2c0d", rotation=70, **kw)
    ax.text(66.85, 26.3, "Kirthar\nMountains", color="#4a2c0d", rotation=80, **kw)
    ax.text(72.5, 33.3, "Salt Range", color="#4a2c0d", **kw)
    ax.text(74.1, 33.35, "Potohar Plateau", color="#6b4a1e", fontweight="bold", **kw)
    ax.text(75.7, 33.1, "Himalayan &\nSub-Himalayan\npiedmonts", color="#6b4a1e", fontweight="bold", **kw)
    ax.text(67.4, 23.35, "Arabian Sea", color="#1f4e79", style="italic", fontweight="bold", **kw)
    ax.text(69.5, 23.85, "Rann of\nKachchh", color="#7a6a1e", **kw)
    ax.text(72.4, 27.0, "Thar &\nCholistan deserts", color="#7a6a1e", **kw)
    ax.text(75.6, 31.0, "plain continues into\nIndian Punjab →", color="#2f6f2f", fontsize=7.5,
            ha="center", va="center", style="italic", zorder=7)
    for nm, (x, y) in {"Indus": (71.45, 31.6), "Jhelum": (72.75, 32.2), "Chenab": (73.7, 31.9),
                       "Ravi": (73.7, 31.15), "Sutlej": (73.0, 29.85)}.items():
        ax.text(x, y, nm, color="#0b3d6e", fontsize=7, style="italic", zorder=7)

    if mode == "divisions":
        ax.plot([69.9, 71.2], [28.9, 28.9], color="#b00020", lw=2, ls="--", zorder=6)
        ax.text(69.0, 29.2, "Mithankot\n(Panjnad joins Indus)", color="#b00020", fontsize=7.5,
                ha="center", zorder=7)
        ax.text(72.9, 31.35, "UPPER INDUS PLAIN\n(Punjab)", color="#1f4d1f", fontsize=10,
                fontweight="bold", ha="center", zorder=7)
        ax.text(68.75, 26.35, "LOWER\nINDUS\nPLAIN\n(Sindh)", color="#7a3d00", fontsize=10,
                fontweight="bold", ha="center", zorder=7)
        ax.text(70.2, 32.0, "Sindh Sagar\nDoab", fontsize=7, ha="center", color="#1f4d1f", zorder=7)
        ax.text(72.9, 32.55, "Chaj Doab", fontsize=7, ha="center", color="#1f4d1f", zorder=7)
        ax.text(74.2, 32.15, "Rachna\nDoab", fontsize=7, ha="center", color="#1f4d1f", zorder=7)
        ax.text(73.4, 30.55, "Bari Doab", fontsize=7, ha="center", color="#1f4d1f", zorder=7)
        ax.text(68.15, 24.35, "Indus\nDelta", fontsize=8, ha="center", color="#7a3d00", zorder=7)
        ax.set_title("Major geographic divisions of the Indus Plain (schematic)", fontsize=12)
    else:
        box = dict(boxstyle="round,pad=0.3", fc="white", ec="#555", alpha=0.92)
        ax.annotate("NORTH / EAST\nHimalayan & Sub-Himalayan piedmonts,\nPotohar Plateau, Salt Range",
                    xy=(74.2, 32.75), xytext=(71.0, 33.62), fontsize=7.5, bbox=box, zorder=8,
                    arrowprops=dict(arrowstyle="->", color="#333"))
        ax.annotate("WEST\nSulaiman Range, Kirthar Mountains,\nBalochistan Plateau",
                    xy=(69.95, 30.2), xytext=(66.2, 28.9), fontsize=7.5, bbox=box, zorder=8,
                    arrowprops=dict(arrowstyle="->", color="#333"))
        ax.annotate("SOUTH\nArabian Sea & Rann of Kachchh",
                    xy=(68.0, 23.9), xytext=(70.6, 23.05), fontsize=7.5, bbox=box, zorder=8,
                    arrowprops=dict(arrowstyle="->", color="#333"))
        ax.set_title("Geographic location & boundaries of the Indus Plain (schematic)", fontsize=12)

    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.grid(alpha=0.25, lw=0.5)
    fig.tight_layout()
    return fig


def doab_cross_section():
    """Schematic cross-section of a doab between two rivers."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = np.linspace(0, 100, 600)
    ground = np.interp(x, [0, 6, 12, 26, 31, 40, 50, 60, 69, 74, 88, 94, 100],
                       [0.6, 0.1, 1.3, 1.9, 6.4, 7.1, 7.5, 7.1, 6.4, 1.9, 1.3, 0.1, 0.6])
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.6, 11.4)
    ax.axis("off")

    # soil / alluvium
    ax.fill_between(x, -1.4, ground, color="#caa56f", zorder=1)
    # active flood plains (Khaddar / Bet)
    for lo, hi in ((0, 27.5), (72.5, 100)):
        m = (x >= lo) & (x <= hi)
        ax.fill_between(x[m], -0.2, ground[m], color="#9bc47a", alpha=0.9, zorder=2)
    # old flood plain / bar upland (Bangar)
    m = (x >= 27.5) & (x <= 72.5)
    ax.fill_between(x[m], -0.2, ground[m], color="#e6d28a", alpha=0.95, zorder=2)
    ax.plot(x, ground, color="#5a3d1a", lw=2, zorder=4)

    # dry-season river water
    for a, b in ((0, 10), (90, 100)):
        m = (x >= a) & (x <= b)
        ax.fill_between(x[m], ground[m], 1.0, where=ground[m] < 1.0, color="#4aa3df", zorder=3)
    # monsoon flood level + water table
    ax.axhline(3.4, xmin=0.0, xmax=0.30, color="#1f6fb5", ls="--", lw=1.4, zorder=5)
    ax.axhline(3.4, xmin=0.70, xmax=1.0, color="#1f6fb5", ls="--", lw=1.4, zorder=5)
    ax.text(14.5, 3.75, "monsoon flood level", color="#1f6fb5", fontsize=8, ha="center")
    ax.text(85.5, 3.75, "monsoon flood level", color="#1f6fb5", fontsize=8, ha="center")
    ax.plot(x, np.interp(x, [0, 30, 50, 70, 100], [0.3, 1.4, 1.8, 1.4, 0.3]) + 0.1,
            color="#2a6fb0", ls=":", lw=1.3, zorder=3)
    ax.text(50, 0.6, "water table (rises under unlined canals)", color="#fff", fontsize=8, ha="center",
            zorder=6, bbox=dict(boxstyle="round,pad=0.15", fc="#2a6fb0", ec="none", alpha=0.85))

    # oxbow lake + sandbar in active flood plain
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((19, 1.5), 4.2, 0.45, color="#4aa3df", zorder=3))
    ax.text(18.5, 2.35, "oxbow lake", fontsize=7.5, color="#245f8f", ha="center", style="italic")
    ax.text(10.6, 1.9, "sandbar", fontsize=7.5, color="#6b4a1e", ha="center", style="italic")

    def lab(xx, yy, txt, **kw):
        ax.text(xx, yy, txt, ha="center", va="center", fontsize=9, zorder=7,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#444", alpha=0.95), **kw)

    ax.text(5, -0.35, "RIVER A\n(low-flow channel)", ha="center", fontsize=8.5, color="#fff",
            fontweight="bold", zorder=7)
    ax.text(95, -0.35, "RIVER B\n(low-flow channel)", ha="center", fontsize=8.5, color="#fff",
            fontweight="bold", zorder=7)
    lab(18, 5.3, "ACTIVE FLOOD PLAIN\nKhaddar / Bet\nflooded every monsoon; fresh silt")
    lab(82, 5.3, "ACTIVE FLOOD PLAIN\nKhaddar / Bet\nflooded every monsoon; fresh silt")
    lab(50, 9.6, "OLD FLOOD PLAIN / BAR UPLAND\nBangar\nabove flood level; stable older alluvium;\nsettlements, roads, perennial canal farming")
    lab(28.3, 8.6, "SCARP (bluff)\n3-10 m")
    lab(71.7, 8.6, "SCARP (bluff)\n3-10 m")
    for xx in (28.7, 71.3):
        ax.annotate("", xy=(xx + (1.6 if xx < 50 else -1.6), 4.6), xytext=(xx, 7.7),
                    arrowprops=dict(arrowstyle="->", color="#333"), zorder=7)
    for xx, tx in ((18, 18), (82, 82)):
        ax.annotate("", xy=(xx, 2.4), xytext=(tx, 4.2), arrowprops=dict(arrowstyle="->", color="#333"), zorder=7)
    ax.annotate("", xy=(50, 7.6), xytext=(50, 8.7), arrowprops=dict(arrowstyle="->", color="#333"), zorder=7)

    ax.annotate("", xy=(100, 10.9), xytext=(0, 10.9), arrowprops=dict(arrowstyle="<->", color="#555"))
    ax.text(50, 10.97, "DOAB  (interfluve between two rivers) - schematic, not to scale", ha="center",
            va="bottom", fontsize=9.5, fontweight="bold")
    fig.tight_layout()
    return fig


def waterlogging_flow():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    def box(x, y, w, h, txt, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                                    fc=fc, ec="#333", lw=1.2))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=8.5)

    cause = [("Unlined canals on\nflat Bangar zones", "#fde0b5"),
             ("Seepage into the\nlow-gradient plain", "#fde0b5"),
             ("Water table rises\ninto the root zone", "#f9c7c7"),
             ("WATERLOGGING\nroots choked", "#f4a6a6"),
             ("Summer heat:\nevaporation at surface", "#f9c7c7"),
             ("SALINITY\nsalt crust (Sem & Thur)", "#e88a8a")]
    w, gap = 1.6, 0.42
    for i, (t, c) in enumerate(cause):
        x0 = 0.1 + i * (w + gap)
        box(x0, 4.1, w, 1.2, t, c)
        if i < len(cause) - 1:
            ax.annotate("", xy=(x0 + w + gap - 0.03, 4.7), xytext=(x0 + w + 0.03, 4.7),
                        arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.text(0.1, 5.65, "THE CAUSE", fontsize=10, fontweight="bold")
    ax.text(0.1, 3.45, "THE SOLUTIONS", fontsize=10, fontweight="bold")
    sol = [("SCARP projects\ndeep tube wells pump out\ngroundwater, flush salts down", "#cde8c3"),
           ("Canal lining\nconcrete / plastic sheets\nstop seepage", "#cde8c3"),
           ("Tile drainage\nunderground perforated pipes\ncarry excess water away", "#cde8c3"),
           ("Surface drains\ne.g. LBOD in Sindh,\nsaline runoff to Arabian Sea", "#cde8c3")]
    w2, gap2 = 2.75, 0.2
    for i, (t, c) in enumerate(sol):
        box(0.1 + i * (w2 + gap2), 1.0, w2, 1.9, t, c)
    fig.tight_layout()
    return fig


def crop_calendar():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sow, grow, harv = "#f2c14e", "#7cb869", "#c0562b"
    rows = {
        "Rabi (winter)": [(9, 12, sow), (0, 3, grow), (3, 5, harv)],
        "Kharif (summer / monsoon)": [(3, 6, sow), (6, 9, grow), (9, 12, harv)],
    }
    fig, ax = plt.subplots(figsize=(10, 2.8))
    for i, (name, segs) in enumerate(rows.items()):
        for a, b, c in segs:
            ax.barh(i, b - a, left=a, color=c, edgecolor="white", height=0.55)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(list(rows))
    ax.set_xticks(np.arange(12) + 0.5)
    ax.set_xticklabels(months)
    ax.set_xlim(0, 12)
    for xx in range(13):
        ax.axvline(xx, color="#ddd", lw=0.6, zorder=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=sow, label="Sowing"), Patch(color=grow, label="Growing"),
                       Patch(color=harv, label="Harvest")], ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.18), frameon=False)
    ax.set_title("Cropping calendar of the Indus Plain (indicative)", fontsize=11)
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


DIVISIONS = [
    ("Location", "Himalayan foothills down to Mithankot (largely Punjab province)",
     "Mithankot down to the Indus Delta near Thatta (largely Sindh province)"),
    ("River system", "Indus plus its five eastern tributaries: Jhelum, Chenab, Ravi, Beas, Sutlej",
     "'Nilotic' character: the Indus flows as one massive channel with no significant tributaries "
     "after the Panjnad joins it at Mithankot"),
    ("Key features",
     "Doabs (land between two rivers): Sindh Sagar, Chaj, Rachna and Bari Doab; extensive canal irrigation",
     "Flat, low-lying; occasional limestone outcrops near Sukkur and Hyderabad; flood-protective bunds, "
     "meanders, oxbow lakes; sprawling tidal delta ending at the Arabian Sea"),
]

FEATURES = [
    ("River channels (low flow)", "Lowest points of the landscape; where the rivers flow in the dry season."),
    ("Active flood plain (Khaddar / Bet)",
     "Low land beside the river beds. Completely inundated by summer monsoon floods, depositing fresh "
     "fertile silt. Dynamic features: sandbars and oxbow lakes."),
    ("The scarp (bluff)",
     "A steep slope or miniature cliff 3-10 m high; the natural terrace boundary between the active flood "
     "plain and the older, higher ground."),
    ("Old flood plain / bar upland (Bangar)",
     "The elevated central spine of the doab, above normal monsoon flood level and protected from annual "
     "flooding. Older, stable alluvial soil; main zone for permanent settlements, roads and year-round "
     "perennial canal agriculture."),
]

SOLUTIONS = [
    ("SCARP projects", "Salinity Control and Reclamation Projects: thousands of deep tube wells pump out "
                       "groundwater, lowering the water table and flushing salts back down."),
    ("Canal lining", "Lining main canals with concrete or plastic sheets to eliminate seepage."),
    ("Tile drainage", "Underground perforated pipes collect and carry away excess water."),
    ("Surface drains", "Infrastructure such as the Left Bank Outfall Drain (LBOD) in Sindh channels saline "
                       "runoff out to the Arabian Sea."),
]

SEASONS = [
    ("Kharif (summer / monsoon)", "Sown April-June; harvested October-December",
     "Rice, cotton, sugarcane, corn (maize), millet",
     "Rice thrives in the heavy soils of the Old Flood Plain and Lower Indus Plain where perennial canal "
     "water is abundant. Cotton is concentrated in the drier, well-drained soils of the southern Bangar "
     "(e.g. Multan and Bahawalpur divisions)."),
    ("Rabi (winter / dry season)", "Sown October-December; harvested April-May",
     "Wheat (primary staple), gram (chickpeas), barley, mustard, winter vegetables",
     "Wheat is planted across the Old Flood Plains using canal water, and extensively in the Active Flood "
     "Plains (Bet lands) right after the summer floods recede, using residual soil moisture and freshly "
     "deposited fertile silt."),
]


def render():
    st.title("🌾 Indus Plain: Geography, Doabs, Salinity & Cropping")
    st.caption(NOTE)
    t1, t2, t3, t4, t5 = st.tabs([
        "1. Location & Boundaries", "2. Major Divisions", "3. Doab Cross-Section",
        "4. Waterlogging & Salinity", "5. Rabi vs Kharif Cropping",
    ])

    with t1:
        st.subheader("Geographic location & boundaries of the Indus Plain")
        st.pyplot(plain_map("boundaries"), clear_figure=True)
        st.markdown(
            "- **North / East:** bounded by the Himalayan and Sub-Himalayan piedmonts, the Pothohar "
            "Plateau and the Salt Range.\n"
            "- **West:** bounded by the Sulaiman Range, Kirthar Mountains and the Balochistan Plateau.\n"
            "- **South:** terminates at the Arabian Sea and the Rann of Kachchh."
        )

    with t2:
        st.subheader("Major geographic divisions of the Indus Plain")
        st.markdown("The plain is divided into two primary sections based on physiography, river "
                    "patterns and location.")
        st.pyplot(plain_map("divisions"), clear_figure=True)
        st.dataframe(pd.DataFrame(DIVISIONS, columns=["", "1. Upper Indus Plain", "2. Lower Indus Plain"]),
                     use_container_width=True, hide_index=True)

    with t3:
        st.subheader("Schematic cross-section of a doab")
        st.markdown("This schematic shows how a typical interfluve (doab) between two rivers is structured: "
                    "the **active flood plain**, the **old flood plain** and the **bar upland**.")
        st.pyplot(doab_cross_section(), clear_figure=True)
        st.markdown("**Key topographical features**")
        st.dataframe(pd.DataFrame(FEATURES, columns=["Feature", "Description"]),
                     use_container_width=True, hide_index=True)

    with t4:
        st.subheader("Environmental challenges: waterlogging & salinity")
        st.markdown(
            "The introduction of a massive, unlined canal network across the flat Bangar zones "
            "inadvertently disrupted the natural hydrological balance.\n\n"
            "**The cause:** centuries of water seeping out from unlined canals into the flat, low-gradient "
            "plains caused the underground water table to rise. When the water table reaches the root zone "
            "it chokes the plants (**waterlogging**). As this water evaporates at the surface in the intense "
            "summer heat it leaves a crust of dissolved underground salts, rendering the soil toxic to crops "
            "(**salinity / Sem and Thur**)."
        )
        st.pyplot(waterlogging_flow(), clear_figure=True)
        st.markdown("**The solutions**")
        st.dataframe(pd.DataFrame(SOLUTIONS, columns=["Measure", "How it works"]),
                     use_container_width=True, hide_index=True)

    with t5:
        st.subheader("Crop cultivation patterns (Rabi vs Kharif)")
        st.markdown("The timing and location of agriculture in the Indus Plain are strictly tied to the "
                    "seasonal monsoons and temperature changes.")
        st.pyplot(crop_calendar(), clear_figure=True)
        st.dataframe(pd.DataFrame(SEASONS, columns=["Season", "Timeline", "Key crops", "Zonal choice"]),
                     use_container_width=True, hide_index=True)
