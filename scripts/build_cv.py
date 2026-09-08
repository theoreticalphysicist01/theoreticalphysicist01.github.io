from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "cv.pdf"
OUTPUT.parent.mkdir(exist_ok=True)

TEXT = HexColor("#292b2d")
MUTED = HexColor("#676b6d")
ACCENT = HexColor("#215b72")

styles = getSampleStyleSheet()
name = ParagraphStyle("Name", parent=styles["Title"], fontName="Times-Bold", fontSize=28, leading=31, textColor=TEXT, spaceAfter=4)
subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=MUTED)
section = ParagraphStyle("Section", parent=styles["Heading2"], fontName="Times-Bold", fontSize=13, leading=17, textColor=TEXT, spaceBefore=15, spaceAfter=7)
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=TEXT)
pub = ParagraphStyle("Pub", parent=body, leftIndent=0, firstLineIndent=0, spaceAfter=7)
small_right = ParagraphStyle("Right", parent=subtitle, alignment=TA_RIGHT)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#d8dad7")); canvas.line(22*mm, 18*mm, 188*mm, 18*mm)
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica", 7.5)
    canvas.drawString(22*mm, 12*mm, "Zeng-Zhao Li - Curriculum Vitae")
    canvas.drawRightString(188*mm, 12*mm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=22*mm, leftMargin=22*mm, topMargin=21*mm, bottomMargin=24*mm, title="Zeng-Zhao Li - Curriculum Vitae", author="Zeng-Zhao Li")

story = []
header = Table([[Paragraph("Zeng-Zhao Li", name), Paragraph("zengzhaoli09@gmail.com<br/>zengzhaoli.github.io", small_right)]], colWidths=[105*mm, 61*mm])
header.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0)]))
story += [header, Spacer(1, 8), Paragraph("RESEARCHER IN QUANTUM SCIENCE", subtitle)]
story += [Paragraph("Current Appointment", section), Paragraph("Shenzhen International Quantum Academy<br/>Silicon Quantum Computing Laboratory", body)]
story += [Paragraph("Research Profile", section), Paragraph("Theoretical research in quantum information and computation, non-Hermitian quantum physics, exceptional points, open quantum systems, quantum transport, quantum control, spin qubits, and silicon quantum computing.", body)]
story += [Paragraph("Selected Publications", section)]
publications = [
    ("2025", "Z.-W. Li, J. Chen, W. Xiong, X. Xue, and <b>Z.-Z. Li</b>, \"Quantum Coulomb drag signatures of Majorana bound states,\" arXiv:2512.02401."),
    ("2025", "<b>Z.-Z. Li</b>, C.-H. Lam, C.-T. Yip, and B. Li, \"Spectral signatures of the Markovian to non-Markovian transition in open quantum systems,\" <i>APL Quantum</i> 2."),
    ("2024", "<b>Z.-Z. Li</b> and K. B. Whaley, \"Enhancement of vibrationally assisted energy transfer by proximity to exceptional points, probed by fluorescence-detected vibrational spectroscopy,\" <i>Phys. Rev. Research</i> 6, 023149."),
    ("2023", "<b>Z.-Z. Li</b>, W. Chen, M. Abbasi, K. W. Murch, and K. B. Whaley, \"Speeding Up Entanglement Generation by Proximity to Higher-Order Exceptional Points,\" <i>Phys. Rev. Lett.</i> 131, 100202."),
    ("2022", "<b>Z.-Z. Li</b>, J. Atalaya, and K. B. Whaley, \"Topological quantum interference in a pumped Su-Schrieffer-Heeger lattice,\" <i>Phys. Rev. A</i> 105, 052209."),
    ("2022", "<b>Z.-Z. Li</b>, L. Ko, Z. Yang, M. Sarovar, and K. B. Whaley, \"Interplay of vibration- and environment-assisted energy transfer,\" <i>New J. Phys.</i> 24, 033032."),
]
for year, citation in publications:
    row = Table([[Paragraph(year, subtitle), Paragraph(citation, pub)]], colWidths=[16*mm, 150*mm])
    row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
    story.append(row)
story += [Paragraph("Full publication record", section), Paragraph("The complete, updateable list with DOI, journal, arXiv, and PDF links is available at zengzhaoli.github.io/publications.html.", body)]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
