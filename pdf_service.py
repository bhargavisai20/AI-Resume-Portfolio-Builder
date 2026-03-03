from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


def generate_pdf(file_path, resume_text, user):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=5
    )

    normal_style = styles['Normal']

    # Add Name
    elements.append(Paragraph(user.name, name_style))
    elements.append(Spacer(1, 0.2 * inch))

    # Add Resume Content
    for line in resume_text.split("\n"):
        elements.append(Paragraph(line, normal_style))
        elements.append(Spacer(1, 0.1 * inch))

    doc.build(elements)