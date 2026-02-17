# utils/resume_parser.py

import re
import pdfplumber
from docx import Document


def extract_text_from_resume(file_path: str) -> str:
    """
    Extracts raw text from PDF or DOCX resume
    """
    text = ""

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    else:
        raise ValueError("Unsupported file format")

    return clean_resume_text(text)


def clean_resume_text(resume_text: str) -> str:
    """
    Cleans resume text for ML processing
    """
    if not resume_text:
        return ""

    text = resume_text.lower()

    text = re.sub(r'\S+@\S+', ' ', text)          # emails
    text = re.sub(r'\+?\d[\d\s\-]{8,}', ' ', text)  # phone numbers
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  # special chars
    text = re.sub(r'\s+', ' ', text)              # extra spaces

    return text.strip()
