from resume_parser import ResumeParser
from nlp_processor import NLPProcessor
from ats_checker import ATSChecker

# Extract resume text
parser = ResumeParser()
resume_text = parser.parse_resume("uploads/sample.pdf")

# Extract technical skills
nlp = NLPProcessor()
analysis = nlp.analyze_resume(resume_text)

# Run ATS checks
checker = ATSChecker()
report = checker.check_resume(
    resume_text,
    analysis["technical_skills"]
)

# Display results
print("\n========== ATS CHECK REPORT ==========")

for check_name, result in report["results"].items():

    status = "PASS" if result["passed"] else "FAIL"

    print(f"\n{check_name.upper()}: {status}")
    print(result["message"])

print("\n========== SUMMARY ==========")
print("Total Checks:", report["total_checks"])
print("Passed Checks:", report["passed_checks"])
print("Failed Checks:", report["failed_checks"])

print("\n========== TEST COMPLETED ==========")