# utils/resume_parser.py

import re

def clean_resume_text(resume_text: str) -> str:
    """
    Cleans resume text for ML processing
    """
    if not resume_text:
        return ""

    text = resume_text.lower()

    # Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove phone numbers
    text = re.sub(r'\+?\d[\d\s\-]{8,}', ' ', text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
