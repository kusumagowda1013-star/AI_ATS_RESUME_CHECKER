from resume_parser import ResumeParser

parser = ResumeParser()

resume_text = parser.parse_resume("uploads/sample.pdf")

print("Resume extracted successfully!")
print("--------------------------------")
print(resume_text)