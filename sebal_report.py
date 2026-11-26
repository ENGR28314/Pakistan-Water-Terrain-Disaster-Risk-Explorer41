"""
sebal_report.py
Builds a downloadable offline PDF summary of a SEBAL evapotranspiration run,
using reportlab (no internet access needed). A matplotlib bar chart of
ET24 by zone is rendered to a PNG and embedded in the PDF.
"""

from __future__ import annotations

import io

import pandas as pd


def _render_et24_chart_png(df: pd.DataFrame) -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3.2), dpi=150)
    names = df["Name"].astype(str).tolist()
    values = df["ET24_mm_day"].tolist()
    ax.bar(range(len(names)), values, color="#1f7a4d")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=35, ha="right", fontsize=7)
    ax.set_ylabel("ET24 (mm/day)")
    ax.set_title("SEBAL Daily Evapotranspiration by Zone")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def build_sebal_pdf_report(results: pd.DataFrame, calib: dict, author: str = "Engr. Syed Hassan Iqbal Shah (ELECT/28314)") -> bytes:
    """Returns PDF bytes for a summary report of a SEBAL run. Requires reportlab."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=16)
    normal = styles["Normal"]
    small = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8, textColor=colors.grey)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=18 * mm, bottomMargin=16 * mm, leftMargin=16 * mm, rightMargin=16 * mm,
    )
    story = []

    story.append(Paragraph("SEBAL Model — Indus Basin Evapotranspiration Report", title_style))
    story.append(Paragraph(f"Created and designed by {author}", normal))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Offline, upload-driven SEBAL/METRIC energy-balance evapotranspiration "
        "run. Educational / illustrative output — not validated against field "
        "lysimeter or eddy-covariance measurements; verify before operational use.",
        small,
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Hot / Cold Pixel Calibration", styles["Heading2"]))
    calib_rows = [
        ["Cold pixel (wet/vegetated)", calib.get("cold_pixel_name", "—"), f"{calib.get('Ts_cold_C', 0):.2f} °C"],
        ["Hot pixel (dry/bare)", calib.get("hot_pixel_name", "—"), f"{calib.get('Ts_hot_C', 0):.2f} °C"],
        ["Fitted dT = a + b·Ts", f"a = {calib.get('a', 0):.4f}", f"b = {calib.get('b', 0):.4f}"],
    ]
    t = Table([["Anchor", "Zone", "Value"]] + calib_rows, colWidths=[55 * mm, 70 * mm, 45 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a4d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    try:
        png = _render_et24_chart_png(results)
        story.append(Image(io.BytesIO(png), width=165 * mm, height=75 * mm))
        story.append(Spacer(1, 10))
    except Exception:
        pass

    story.append(Paragraph("Per-Zone Results", styles["Heading2"]))
    cols = ["Name", "NDVI", "Rn_Wm2", "G_Wm2", "H_Wm2", "LE_Wm2", "ET_inst_mm_hr", "ET24_mm_day"]
    cols = [c for c in cols if c in results.columns]
    header = ["Zone", "NDVI", "Rn (W/m²)", "G (W/m²)", "H (W/m²)", "LE (W/m²)", "ET inst (mm/hr)", "ET24 (mm/day)"][: len(cols)]
    data_rows = []
    for _, row in results.iterrows():
        data_rows.append([
            str(row["Name"])[:28],
            f"{row['NDVI']:.2f}" if "NDVI" in results.columns else "",
            f"{row['Rn_Wm2']:.0f}" if "Rn_Wm2" in results.columns else "",
            f"{row['G_Wm2']:.0f}" if "G_Wm2" in results.columns else "",
            f"{row['H_Wm2']:.0f}" if "H_Wm2" in results.columns else "",
            f"{row['LE_Wm2']:.0f}" if "LE_Wm2" in results.columns else "",
            f"{row['ET_inst_mm_hr']:.3f}" if "ET_inst_mm_hr" in results.columns else "",
            f"{row['ET24_mm_day']:.2f}" if "ET24_mm_day" in results.columns else "",
        ])
    tbl = Table([header] + data_rows, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a4d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef5ef")]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "Method: Bastiaanssen et al. (1998) SEBAL; Allen, Tasumi & Trezza (2007) "
        "METRIC refinements; Allen et al. (1998) FAO-56 solar-geometry fallback; "
        "Brutsaert (1982) roughness-length relation; Paulson (1970) / Webb (1970) "
        "Monin-Obukhov stability corrections. Re-implemented from the published "
        "formulation for this offline, upload-driven dashboard module — not "
        "derived from any proprietary SEBAL/METRIC software.",
        small,
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()
