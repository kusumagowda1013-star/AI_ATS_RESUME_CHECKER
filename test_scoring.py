from resume_parser import ResumeParser
from nlp_processor import NLPProcessor
from ats_checker import ATSChecker
from scoring import ScoringEngine

# Extract resume text
parser = ResumeParser()
resume_text = parser.parse_resume("uploads/sample.pdf")

# Analyze resume
nlp = NLPProcessor()
analysis = nlp.analyze_resume(resume_text)

# Perform ATS checks
checker = ATSChecker()
ats_report = checker.check_resume(
    resume_text,
    analysis["technical_skills"]
)

# Calculate ATS score
scorer = ScoringEngine()
score_report = scorer.calculate_score(ats_report)

# Display score
print("\n========== ATS SCORE REPORT ==========")

print("ATS Score:", score_report["ats_score"], "/ 100")
print("Grade:", score_report["grade"])

print("\n========== SCORE BREAKDOWN ==========")

for check, details in score_report["breakdown"].items():

    print(f"\n{check.upper()}")
    print("Status:", details["status"])
    print("Weight:", details["weight"])
    print("Earned:", details["earned_score"])

print("\n========== SCORING COMPLETED ==========")