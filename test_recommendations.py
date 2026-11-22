from resume_parser import ResumeParser
from nlp_processor import NLPProcessor
from ats_checker import ATSChecker
from recommendations import RecommendationEngine

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

# Generate recommendations
engine = RecommendationEngine()

report = engine.generate_full_report(
    ats_report,
    resume_skills=analysis["technical_skills"],
    job_skills=["python", "java", "sql", "machine learning", "react"]
)

# Display ATS recommendations
print("\n========== ATS RECOMMENDATIONS ==========")

for item in report["ats_recommendations"]:
    print("\nCategory:", item["category"])
    print("Priority:", item["priority"])
    print("Suggestion:", item["suggestion"])

# Display skill recommendations
print("\n========== SKILL RECOMMENDATIONS ==========")

print("Missing Skills:", report["skill_recommendations"]["missing_skills"])
print("Suggestion:", report["skill_recommendations"]["suggestion"])

print("\n========== TEST COMPLETED ==========")