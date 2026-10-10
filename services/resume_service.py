from PyPDF2 import PdfReader
from docx import Document
from services.gemini_service import ask_gemini

def extract_text_from_txt(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return text if text else ""

def extract_text_from_pdf(filepath):

    try:

        reader = PdfReader(filepath)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception:

        return ""

def extract_text_from_docx(filepath):

    try:

        document = Document(filepath)

        text = ""

        for paragraph in document.paragraphs:

            if paragraph.text:
                text += paragraph.text + "\n"

        return text

    except Exception:

        return ""


def analyze_resume(resume_text):

    prompt = f"""
    You are an expert ATS Resume Reviewer.

    Analyze this resume and provide:

    # Resume Summary

    # ATS Score
    Give a score out of 100.

    # Strengths

    # Weaknesses

    # Missing Skills

    # Recommended Job Roles
    Suggest 3-5 suitable roles.

    # Interview Readiness
    Beginner / Intermediate / Advanced

    # Learning Roadmap
    Give next skills to learn.

    # Suggestions for Improvement

    # Overall Rating
    Give rating out of 10.

    IMPORTANT:
    - Do NOT reproduce the resume.
    - Do NOT show extracted text.
    - Use Markdown.
    - Be concise and professional.

    Resume:

    {resume_text}
    """

    return ask_gemini(prompt)