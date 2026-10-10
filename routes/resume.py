from flask import Blueprint, render_template, request
import os
from services.resume_service import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx,
    analyze_resume
)
from flask import session, redirect, url_for

resume = Blueprint("resume", __name__)

UPLOAD_FOLDER = "uploads"


@resume.route("/resume", methods=["GET", "POST"])
def resume_page():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    message = ""
    resume_text = ""
    analysis = ""

    if request.method == "POST":

        file = request.files.get("resume")

        if file and file.filename:

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(filepath)

            message = f"""
        Resume uploaded successfully:
        {file.filename}
        """

            if file.filename.endswith(".txt"):

                resume_text = extract_text_from_txt(
                    filepath
                )

            elif file.filename.endswith(".pdf"):

                resume_text = extract_text_from_pdf(
                    filepath
                )

            elif file.filename.endswith(".docx"):

                resume_text = extract_text_from_docx(
                    filepath
                )

            if not resume_text.strip():

                message = """
        The uploaded resume appears to be empty.

        Please upload a valid resume file.
        """
            if not resume_text.strip():

                message = """
            The uploaded file is empty, corrupted,
            or contains no readable text.
            """
            
            else:

                analysis = analyze_resume(
                    resume_text
                )

    return render_template(
        "resume.html",
        message=message,
        resume_text=resume_text,
        analysis=analysis
    )