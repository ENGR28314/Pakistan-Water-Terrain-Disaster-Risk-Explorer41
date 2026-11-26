"""
security_bodies.py
Logos of law-enforcement, security, justice, military, regulatory and related federal/provincial
bodies, supplied by the project owner. Shown for reference only; names marked "verify" were
identified from the image. Logos do not imply endorsement.
"""

GROUPS = ['Justice, Anti-Corruption & Immigration', 'Police', 'Paramilitary & Maritime', 'Military Bodies', 'Authorities & Agencies', 'Constitutional, Regulatory & Public Sector', 'Public Sector Organizations', 'Federal Authorities, Ports & Projects', 'Defence Industry & Strategic Organizations', 'Corporate & Commercial Entities', 'Science, Technology & Research', 'Governments & Institutions', 'Military Academies & Training Institutions', 'Professional Councils & Associations', 'Associations & Federations', 'Sports Bodies & Federations', 'Discos of WAPDA', 'Gencos of WAPDA', 'Pakistan Air Force Squadrons & Bases', 'Pakistan Navy Units', 'Pakistan Navy Training Establishments', 'PAKISTAN NAVY FORCE COMMANDS']

# Logos with white artwork are shown on a dark chip; wide logos get a wider cell.
BG = {'University of South Asia (USA), Lahore': '#333333', 'All Pakistan Outdoor Advertisers Association (APOAA)': '#333333', 'All Pakistan Stainless Steel Importers and Traders Association (APSSITA)': '#01411c', 'Directorate General of Trade Organizations (DGTO)': '#01411c', 'Pakistan Industrial Technical Assistance Centre (PITAC)': '#01411c', 'National Institute of Oceanography (NIO)': '#ffffff', 'Oil & Gas Regulatory Authority (OGRA)': '#01411c', 'Pakistan Bureau of Statistics': '#0b5d3b', 'Invest Pakistan / Board of Investment (BOI)': '#01411c'}
WIDE = ['Institute of Space Technology (IST), Islamabad', 'Shaheed Mir Sikandar Zehri University (SMSZU), Khuzdar', "Sardar Bahadur Khan Women's University (SBKWU), Quetta", 'Iqra National University (INU), Peshawar', 'Institute of Management Sciences (im|Sciences), Hayatabad, Peshawar', 'CECOS University of IT and Emerging Sciences, Peshawar', 'Preston University', 'Muslim Youth University (MY University), Islamabad', 'Ibadat International University Islamabad (IIUI)', 'Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology (AF-IAST)', 'University of Swabi (UoS)', 'Abasyn University, Peshawar', 'Khyber Medical University (KMU), Peshawar', 'Lahore Institute of Science and Technology (LIST)', 'Multan University of Science & Technology (MUST)', 'Fatima Jinnah Medical University (FJMU), Lahore', 'Information Technology University (ITU), Lahore', 'Cholistan University of Veterinary and Animal Sciences (CUVAS), Bahawalpur', 'NUR International University (NIU), Lahore', 'Institute for Art and Culture (IAC), Lahore', 'National University of Medical Sciences (NUMS)', 'Institute of Management Sciences (Pak-AIMS), Lahore', 'University of South Asia (USA), Lahore', 'Qalandar Shahbaz University of Modern Sciences (QSUMS), Karachi', 'Sohail University, Karachi', 'Malir University of Science and Technology (MUST), Karachi', 'Millennium Institute of Technology and Entrepreneurship (MITE), Karachi', 'Baqai Medical University, Karachi', 'Greenwich University, Karachi', 'Karachi School of Business and Leadership (KSBL), Karachi', 'Dawood University of Engineering and Technology (DUET), Karachi', 'Sukkur IBA University (SIBAU)', 'Fauji Fertilizer Company Limited (FFC)', 'Fauji Cement Company Limited (FCCL)', 'Askari Bank Limited', 'The Hub Power Company Limited (HUBCO)', 'Agri Tech Limited', 'University Medical & Dental College (UMDC), Faisalabad', 'PakAngels', 'Pakistan Tanners Association (PTA)', 'Pakistan Tyre Importers & Dealers Association (PTIDA)', 'Pakistan Electrical & Electronics Merchants Association (PEEMA)', 'Healthcare Devices Association of Pakistan (HDAP)', 'Pakistan Cosmetic Manufacturers Association (PCMA)', 'CropLife Pakistan Association', 'Pakistan Crop Protection Association (PCPA)', 'Pakistan Dairy Association (PDA)', 'All Pakistan Toys Traders Association (APTA)', 'Pakistan Gems Jewellery Traders & Exporters Association (PGJTEA)', 'Air Cargo Agents Association of Pakistan (ACAAP)', 'Pakistan Waste Products Association (PWPA)', 'Pakistan Cloth Merchants Association (PCMA), Karachi', 'Pakistan Denim Manufacturers & Exporters Association (PDMEA)', 'All Pakistan Textile Processing Mills Association (APTPMA)', 'Pakistan Coating Association (PCA)', 'Warehousing & Logistics Association (WLA)', 'Pakistan Association of Food Industries (PAFI)', 'NBFI & Modaraba Association of Pakistan', 'All Pakistan CNG Association', 'Pakistan Bedwear Exporters Association (PBEA)', 'All Pakistan Aluminium Utensils Manufacturers Association (APAUMA)', 'All Pakistan HVACR Association (ALPHA)', "Telecom Operators' Association (TOA)", 'Computer Hardware Association of Pakistan (CHAP)', 'Pakistan Solar Association (PSA)', 'Bahria Foundation', 'Indus River System Authority (IRSA)', 'National Logistics Corporation (NLC)', 'Naya Pakistan Housing & Development Authority']

# Logo data lives in two files so each stays under the GitHub file-size limit.
from security_bodies_data1 import BODIES_1
from security_bodies_data2 import BODIES_2
from security_bodies_data3 import BODIES_3

BODIES = BODIES_1 + BODIES_2 + BODIES_3


def _match(name: str, query: str) -> bool:
    return not query or query.strip().lower() in name.lower()


def group_html(group: str, height: int = 78, query: str = "") -> str:
    cells = []
    for name, grp, b64 in BODIES:
        if grp != group or not _match(name, query):
            continue
        mime = "image/jpeg" if b64.startswith("/9j/") else "image/png"
        wide = name in WIDE
        cell_w, max_w = (int(height * 3.2), int(height * 3.0)) if wide else (int(height * 1.65), int(height * 1.5))
        h = int(height * 0.67) if wide else height
        chip = f"background:{BG[name]};border-radius:6px;padding:4px 6px;" if name in BG else ""
        cells.append(
            f'<div style="width:{cell_w}px;text-align:center;">'
            f'<div style="display:inline-block;{chip}">'
            f'<img alt="{name}" title="{name}" src="data:{mime};base64,{b64}" '
            f'style="height:{h}px;max-width:{max_w}px;width:auto;object-fit:contain;display:block;" /></div>'
            f'<div style="font-size:11px;font-weight:600;line-height:1.2;margin-top:3px;">{name}</div></div>'
        )
    return '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:4px 0 10px 0;">' + "".join(cells) + "</div>"


def rows(query: str = "", groups=None):
    """Plain rows (name, group) for table view / search."""
    return [{"Name": n, "Group": g} for n, g, _ in BODIES
            if (not groups or g in groups) and _match(n, query)]


def image_bytes(name: str):
    import base64
    for n, _g, b64 in BODIES:
        if n == name:
            return base64.b64decode(b64)
    return None
