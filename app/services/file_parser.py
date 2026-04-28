from PyPDF2 import PdfReader
from docx import Document


# =========================
# PDF PARSER
# =========================
def parse_pdf(file):
    reader = PdfReader(file.file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# =========================
# DOCX PARSER
# =========================
def parse_docx(file):
    doc = Document(file.file)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text


# =========================
# TXT PARSER
# =========================
def parse_txt(file):
    return file.file.read().decode("utf-8")