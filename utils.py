import io

from docx import Document

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_docx(text):

    if not text:
        return None

    document = Document()

    for line in text.split("\n"):

        document.add_paragraph(line)

    output = io.BytesIO()

    document.save(output)

    output.seek(0)

    return output


def create_pdf(text):

    output = io.BytesIO()

    doc = SimpleDocTemplate(output)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        story.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    doc.build(story)

    output.seek(0)

    return output