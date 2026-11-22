from resume_parser import ResumeParser
from nlp_processor import NLPProcessor

# Extract resume text
parser = ResumeParser()
resume_text = parser.parse_resume("uploads/sample.pdf")

# Analyze resume
nlp = NLPProcessor()
result = nlp.analyze_resume(resume_text)

# Display results
print("\n========== NLP ANALYSIS ==========")

print("\n1. TECHNICAL SKILLS")
print(result["technical_skills"])

print("\n2. SOFT SKILLS")
print(result["soft_skills"])

print("\n3. ACTION VERBS")
print(result["action_verbs"])

print("\n4. RESUME SECTIONS")

for section, content in result["sections"].items():
    print(f"\n{section.upper()}:")
    print(content)

print("\n5. TOP KEYWORDS")
print(result["keywords"])

print("\n========== ANALYSIS COMPLETED ==========")