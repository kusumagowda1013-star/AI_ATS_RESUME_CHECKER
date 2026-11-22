from resume_parser import ResumeParser
from nlp_processor import NLPProcessor
from ats_checker import ATSChecker
from scoring import ScoringEngine
from recommendations import RecommendationEngine
from report_generator import ReportGenerator


# Step 1: Extract resume text
parser = ResumeParser()
resume_text = parser.parse_resume("uploads/sample.pdf")


# Step 2: Analyze resume
nlp = NLPProcessor()
analysis = nlp.analyze_resume(resume_text)


# Step 3: Perform ATS checks
ats = ATSChecker()
ats_report = ats.check_resume(resume_text, analysis)


# Step 4: Calculate ATS score
scorer = ScoringEngine()
score_report = scorer.calculate_score(ats_report)


# Step 5: Generate recommendations
recommendation_engine = RecommendationEngine()

recommendations_report = recommendation_engine.generate_full_report(
    ats_report,
    analysis["technical_skills"],
    ["python", "sql", "machine learning", "react"]
)


# Step 6: Generate PDF report
report_generator = ReportGenerator()

output_path = report_generator.generate_report(
    score_report,
    ats_report,
    recommendations_report,
    "reports/sample_resume_report.pdf"
)


print("PDF report generated successfully!")
print("Report location:", output_path)
print("ATS Score:", score_report["ats_score"])
print("Grade:", score_report["grade"])