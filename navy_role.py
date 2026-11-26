"""
navy_role.py
Content for the "Pakistan Navy's Role Across This Project's Sectors" page.

Commander titles are supplied by the project owner. Add further commanders to COMMANDS below
(title, abbreviation); the page picks them up automatically.
"""
import army_emblems
import navy_logos

HEADING = "PAKISTAN NAVY FORCE COMMANDS"
EXPECTED_COMMANDERS = 7

COMMANDS = [
    ("Commander Karachi", "COMKAR"),
    ("Commander Logistics", "COMLOG"),
    ("Commander Pakistan Fleet", "COMPAK"),
    ("Commander Coastal Command", "COMCOAST"),
    ("Commander Field and Operational Sea Training", "COMFOST"),
    ("Commander Central Punjab", "COMCEP"),
    ("Commander North", "COMNOR"),
]

# Subordinate commands under each commander, keyed by abbreviation. Not yet supplied -> empty list.
SUBORDINATE_COMMANDS = {abbr: [] for _t, abbr in COMMANDS}
SUBORDINATE_COMMANDS.update({
    "COMKAR": [
        "Pakistan Naval Academy (PNA), PNS Rahbar, Manora",
        "Pakistan Navy Engineering College (PNEC), PNS Johar",
        "Maritime Warfare Training Center (MWTC), PNS Bahadur",
        "Mechanical Training Establishment (MTE), PNS Karsaz",
        "Pakistan Navy School of Management (PNSM), PNS Rahnuma",
        "Pakistan Navy School of Logistics (PNSL)",
        "Pakistan Navy Medical Training School (PNMTS) at PNS Shifa",
        "Naval Physical Training & Sports Complex (NPT&SC)",
        "Pakistan Navy Diving School, PNS Himalaya",
        "PNS Dilawar",
        "PNS Rahat",
        "PNS Nigraan",
    ],
    "COMLOG": [
        "Naval Configuration Management Authority (NCMA)",
        "Naval Maintenance Group Ormara (NMGO)",
        "Naval Maintenance Group Gwadar (NMGG)",
        "Managing Director Weapons and Armaments (MDWA)",
        "Machinery Depot Dockyard Karachi (MDD(K))",
        "Commander Depot (COMDEP)",
        "PNS Peshawar",
        "PN Polytechnic Institute (PNPI)",
        "Cantonment Board Faisal (CBF)",
        "Dr. Shazia Shaheed Medical Centre (DSSMC)",
    ],
    "COMPAK": [
        "Commander Naval Aviation (COMNAV)",
        "Commander 5th Submarine Squadron (COMSUBS (SUBRON-5))",
        "Commander 9th Auxiliary & Minesweeper Squadron (COMAUXMIN-9)",
        "Commander 21st Auxiliary Squadron (COMAUXRON-21)",
        "Commander 14th Destroyer Squadron (COMDESRON (DESRON-14))",
        "Commander 25th Destroyer Squadron (COMDESRON (DESRON-25))",
        "18th Destroyer Squadron (DESRON-18)",
        "10th Patrol Craft Squadron (PATRON-10)",
    ],
    "COMCOAST": [
        "Commander Jinnah Naval Base (JNB)",
        "Commander Gwadar Naval Base (COMCOAST)",
        "Commander West (COMWEST)",
        "Special Service Group (Navy) SSG(N)",
        "Air Defence (AD)",
        "Joint Maritime Information Coordination Center (JMICC)",
        "Creeks Brigade (CreekBDG)",
        "Force Protection Brigade (FPBDG)",
    ],
    "COMCEP": [
        "Pakistan Navy War College (PNWC), Walton, Lahore",
        "PNS Punjab",
    ],
    "COMNOR": [
        "PNS Zafar",
        "PNS Hafeez",
        "Fleet Protection Battalion (1st FP BN)",
        "Naval Provost Unit (NPU)",
    ],
})

NOTE = ("Titles on this page were supplied by the project owner. Roles and responsibilities are not "
        "described here until they are supplied and checked against official Pakistan Navy sources.")


def emblem_b64():
    for name, grp, b64 in army_emblems.FLAGS_ROUNDELS:
        if name == "Pakistan Navy emblem":
            return b64
    return ""


def _img(key: str, h: int) -> str:
    b64 = navy_logos.LOGOS.get(key)
    if not b64:
        return ""
    mime = "image/jpeg" if b64.startswith("/9j/") else "image/png"
    return (f'<img alt="{key}" src="data:{mime};base64,{b64}" '
            f'style="height:{h}px;width:auto;max-width:{int(h * 1.2)}px;object-fit:contain;display:block;flex:none;" />')


def _subs_html(abbr: str) -> str:
    subs = SUBORDINATE_COMMANDS.get(abbr) or []
    if not subs:
        return '<div style="font-size:12px;opacity:.65;font-style:italic;">to be supplied</div>'
    rows = []
    any_logo = any(s in navy_logos.LOGOS for s in subs)
    for s in subs:
        logo = _img(s, 46)
        rows.append('<div style="display:flex;align-items:center;gap:8px;margin:5px 0;">'
                    + (logo or ('<div style="width:46px;flex:none;"></div>' if any_logo else ''))
                    + f'<div style="font-size:13px;line-height:1.25;">{s}</div></div>')
    return "".join(rows)


def commands_html() -> str:
    cells = []
    for i, (title, abbr) in enumerate(COMMANDS, 1):
        cells.append(
            '<div style="min-width:260px;max-width:340px;padding:12px 16px;border:1px solid rgba(128,128,128,.4);'
            'border-left:5px solid #0b2a6f;border-radius:8px;">'
            + _img(abbr, 96) +
            f'<div style="font-size:12px;opacity:.7;margin-top:4px;">Command {i}</div>'
            f'<div style="font-size:17px;font-weight:700;line-height:1.25;">{title}</div>'
            f'<div style="font-size:15px;font-weight:600;letter-spacing:1px;margin-top:2px;">({abbr})</div>'
            '<div style="margin-top:8px;padding-top:6px;border-top:1px solid rgba(128,128,128,.35);">'
            '<div style="font-size:13px;font-weight:700;">Subordinate Commands</div>'
            + _subs_html(abbr) + '</div></div>'
        )
    return '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 14px 0;">' + "".join(cells) + "</div>"
