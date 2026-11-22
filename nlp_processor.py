import re
from collections import Counter


class NLPProcessor:

    def __init__(self):

        # Technical skills to detect
        self.technical_skills = [
            "python", "java", "c", "c++", "c#", "javascript",
            "html", "css", "sql", "mysql", "mongodb",
            "react", "angular", "node.js", "django", "flask",
            "machine learning", "deep learning",
            "artificial intelligence", "data analysis",
            "data science", "pandas", "numpy",
            "tensorflow", "pytorch", "git", "github",
            "linux", "aws", "azure", "docker"
        ]

        # Soft skills to detect
        self.soft_skills = [
            "communication", "teamwork", "leadership",
            "problem solving", "time management",
            "critical thinking", "creativity",
            "adaptability", "collaboration",
            "decision making", "organization"
        ]

        # Action verbs
        self.action_verbs = [
            "developed", "created", "designed", "implemented",
            "managed", "built", "analyzed", "improved",
            "organized", "led", "achieved", "completed",
            "automated", "tested", "maintained",
            "coordinated", "delivered", "optimized",
            "executed", "established"
        ]

        # Resume section headings
        self.section_names = {

            "contact": [
                "contact", "contact information"
            ],

            "summary": [
                "summary", "professional summary",
                "career objective", "objective", "profile"
            ],

            "education": [
                "education", "academic background",
                "educational qualifications"
            ],

            "skills": [
                "skills", "technical skills",
                "core competencies", "key skills"
            ],

            "soft_skills": [
                "soft skills", "personal skills"
            ],

            "experience": [
                "experience", "work experience",
                "professional experience", "employment history"
            ],

            "projects": [
                "projects", "personal projects",
                "academic projects"
            ],

            "certifications": [
                "certifications", "certificates",
                "licenses"
            ],

            "achievements": [
                "achievements", "awards",
                "accomplishments"
            ]
        }


    # Clean extracted resume text
    def clean_text(self, text):

        if not isinstance(text, str):
            raise TypeError("Resume text must be a string.")

        text = text.lower()

        text = re.sub(r'\r\n?', '\n', text)

        text = re.sub(r'[ \t]+', ' ', text)

        text = re.sub(r'\n+', '\n', text)

        text = re.sub(r'[^\w\s@.+#/-]', ' ', text)

        text = re.sub(r' +', ' ', text)

        return text.strip()


    # Detect resume sections
    def extract_sections(self, text):

        sections = {
            section: []
            for section in self.section_names
        }

        current_section = None

        for line in text.splitlines():

            cleaned_line = line.strip().lower()

            if not cleaned_line:
                continue

            detected_section = None

            for section, headings in self.section_names.items():

                if cleaned_line in headings:
                    detected_section = section
                    break

            if detected_section:

                current_section = detected_section

            elif current_section:

                sections[current_section].append(line.strip())

        for section in sections:

            sections[section] = "\n".join(
                sections[section]
            )

        return sections


    # Detect technical skills
    def extract_skills(self, text):

        cleaned_text = self.clean_text(text)

        found_skills = []

        for skill in self.technical_skills:

            pattern = (
                r'(?<!\w)'
                + re.escape(skill.lower())
                + r'(?!\w)'
            )

            if re.search(pattern, cleaned_text):

                found_skills.append(skill)

        return sorted(set(found_skills))


    # Detect soft skills
    def extract_soft_skills(self, text):

        cleaned_text = self.clean_text(text)

        found_skills = []

        for skill in self.soft_skills:

            pattern = (
                r'(?<!\w)'
                + re.escape(skill.lower())
                + r'(?!\w)'
            )

            if re.search(pattern, cleaned_text):

                found_skills.append(skill)

        return sorted(set(found_skills))


    # Detect action verbs
    def extract_action_verbs(self, text):

        cleaned_text = self.clean_text(text)

        found_verbs = []

        for verb in self.action_verbs:

            pattern = (
                r'\b'
                + re.escape(verb)
                + r'\b'
            )

            if re.search(pattern, cleaned_text):

                found_verbs.append(verb)

        return sorted(set(found_verbs))


    # Extract frequently used keywords
    def extract_keywords(self, text):

        cleaned_text = self.clean_text(text)

        words = re.findall(
            r'\b[a-zA-Z]{3,}\b',
            cleaned_text
        )

        common_words = {
            "the", "and", "for", "with", "from",
            "this", "that", "are", "was", "were",
            "have", "has", "had", "you", "your",
            "our", "their", "they", "will", "can",
            "job", "work", "working", "resume"
        }

        filtered_words = [
            word for word in words
            if word not in common_words
        ]

        keyword_counts = Counter(filtered_words)

        return keyword_counts.most_common(20)


    # Perform complete resume analysis
    def analyze_resume(self, text):

        cleaned_text = self.clean_text(text)

        sections = self.extract_sections(text)

        technical_skills = self.extract_skills(text)

        soft_skills = self.extract_soft_skills(text)

        action_verbs = self.extract_action_verbs(text)

        keywords = self.extract_keywords(text)

        return {

            "cleaned_text": cleaned_text,

            "sections": sections,

            "technical_skills": technical_skills,

            "soft_skills": soft_skills,

            "action_verbs": action_verbs,

            "keywords": keywords

        }