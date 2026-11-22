import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)

from werkzeug.utils import secure_filename

from resume_parser import ResumeParser
from nlp_processor import NLPProcessor
from ats_checker import ATSChecker
from scoring import ScoringEngine
from recommendations import RecommendationEngine
from report_generator import ReportGenerator


# ==========================================
# FLASK APPLICATION CONFIGURATION
# ==========================================

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# ==========================================
# CHECK ALLOWED FILE EXTENSIONS
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# RESUME ANALYSIS
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    try:

        # ==================================
        # STEP 1: RECEIVE RESUME
        # ==================================

        if "resume" not in request.files:

            return "No resume file was uploaded.", 400

        file = request.files["resume"]

        if file.filename == "":

            return "Please select a resume file.", 400

        if not allowed_file(file.filename):

            return (
                "Unsupported file format. "
                "Please upload PDF, DOCX or TXT.",
                400
            )

        original_filename = file.filename

        safe_filename = secure_filename(original_filename)

        if not safe_filename:

            return "Invalid filename.", 400

        unique_name = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        saved_filename = (
            unique_name + "_" + safe_filename
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            saved_filename
        )

        file.save(file_path)

        # ==================================
        # STEP 2: PARSE RESUME
        # ==================================

        parser = ResumeParser()

        resume_text = parser.parse_resume(file_path)

        if not resume_text or not resume_text.strip():

            return (
                "Could not extract text from the resume. "
                "Please upload another file.",
                400
            )

        print("\n========== UPLOADED FILE DETAILS ==========")

        print("Original filename:", original_filename)
        print("Saved filename:", saved_filename)
        print("Saved file path:", file_path)
        print("Extracted text length:", len(resume_text))

        print("\nFirst 500 characters:")
        print(repr(resume_text[:500]))

        print("\n========== RESUME PARSING ==========")
        print(resume_text)

        # ==================================
        # STEP 3: NLP ANALYSIS
        # ==================================

        nlp = NLPProcessor()

        analysis = nlp.analyze_resume(resume_text)

        print("\n========== NLP ANALYSIS ==========")

        print("Technical Skills:")
        print(analysis["technical_skills"])

        print("Soft Skills:")
        print(analysis["soft_skills"])

        print("Action Verbs:")
        print(analysis["action_verbs"])

        print("Sections:")
        print(analysis["sections"])

        # ==================================
        # STEP 4: EXTRACT JOB SKILLS
        # ==================================

        job_skills_input = request.form.get(
            "job_skills",
            ""
        )

        job_skills = [
            skill.strip().lower()
            for skill in job_skills_input.split(",")
            if skill.strip()
        ]

        print("\n========== JOB SKILLS ==========")
        print(job_skills)

        # ==================================
        # STEP 5: ATS CHECKING
        # ==================================

        ats_checker = ATSChecker()

        # Use job requirements when provided.
        # Otherwise, use skills detected by NLP.

        keywords_to_check = (
            job_skills
            if job_skills
            else analysis["technical_skills"]
        )

        ats_report = ats_checker.check_resume(
            resume_text,
            keywords_to_check
        )

        print("\n========== ATS RESULTS ==========")
        print(ats_report)

        # ==================================
        # STEP 6: ATS SCORE CALCULATION
        # ==================================

        scorer = ScoringEngine()

        score_report = scorer.calculate_score(
            ats_report
        )

        print("\n========== ATS SCORE ==========")
        print(score_report)

        # ==================================
        # STEP 7: RECOMMENDATIONS
        # ==================================

        recommendation_engine = RecommendationEngine()

        recommendations_report = (
            recommendation_engine.generate_full_report(
                ats_report,
                analysis["technical_skills"],
                job_skills
            )
        )

        print("\n========== RECOMMENDATIONS ==========")
        print(recommendations_report)

        # ==================================
        # STEP 8: PDF REPORT GENERATION
        # ==================================

        report_generator = ReportGenerator()

        report_filename = (
            "ATS_Report_" + unique_name + ".pdf"
        )

        report_path = os.path.join(
            REPORT_FOLDER,
            report_filename
        )

        report_generator.generate_report(
            score_report,
            ats_report,
            recommendations_report,
            report_path
        )

        print("\nPDF report generated:", report_path)

        # ==================================
        # STEP 9: DISPLAY RESULTS
        # ==================================

        return render_template(
            "result.html",
            score_report=score_report,
            ats_report=ats_report,
            analysis=analysis,
            recommendations_report=recommendations_report,
            report_filename=report_filename
        )

    except Exception as error:

        print("\n========== APPLICATION ERROR ==========")

        print(error)

        app.logger.exception(
            "Resume analysis failed"
        )

        return (
            "Resume analysis failed. "
            "Please check the application terminal for details.",
            500
        )


# ==========================================
# PDF DOWNLOAD
# ==========================================

@app.route("/download/<filename>")
def download_report(filename):

    safe_filename = secure_filename(filename)

    if not safe_filename:

        return "Invalid report filename.", 400

    report_path = os.path.join(
        REPORT_FOLDER,
        safe_filename
    )

    if not os.path.isfile(report_path):

        return "Report not found.", 404

    return send_from_directory(
        REPORT_FOLDER,
        safe_filename,
        as_attachment=True
    )


# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )