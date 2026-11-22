import re


class ATSChecker:

    def __init__(self):
        self.minimum_words = 100
        self.maximum_words = 1000

        self.required_sections = [
            "education",
            "skills",
            "experience",
            "projects"
        ]

        self.action_verbs = [
            "developed",
            "created",
            "designed",
            "implemented",
            "built",
            "managed",
            "improved",
            "increased",
            "reduced",
            "optimized",
            "achieved",
            "completed",
            "organized",
            "analyzed",
            "led"
        ]

    # 1. Check resume length
    def check_resume_length(self, text):

        words = text.split()
        word_count = len(words)

        passed = (
            self.minimum_words <= word_count <= self.maximum_words
        )

        return {
            "passed": passed,
            "word_count": word_count,
            "message": (
                "Resume length is appropriate."
                if passed
                else f"Resume should contain between "
                     f"{self.minimum_words} and "
                     f"{self.maximum_words} words."
            )
        }

    # 2. Check required resume sections
    def check_required_sections(self, text):

        text_lower = text.lower()

        found_sections = []
        missing_sections = []

        section_aliases = {
            "education": ["education", "academic background"],
            "skills": ["skills", "technical skills", "core skills"],
            "experience": [
                "experience",
                "work experience",
                "professional experience"
            ],
            "projects": ["projects", "personal projects"]
        }

        for section, aliases in section_aliases.items():

            if any(alias in text_lower for alias in aliases):
                found_sections.append(section)
            else:
                missing_sections.append(section)

        passed = len(missing_sections) == 0

        return {
            "passed": passed,
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "message": (
                "All important resume sections are present."
                if passed
                else "Add the missing resume sections."
            )
        }

    # 3. Check contact information
    def check_contact_information(self, text):

        email_pattern = (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        )

        phone_pattern = (
            r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?"
            r"(?:\d[-.\s]?){9,12}\d(?!\w)"
        )

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        passed = bool(emails and phones)

        return {
            "passed": passed,
            "email_found": bool(emails),
            "phone_found": bool(phones),
            "message": (
                "Contact information is available."
                if passed
                else "Add a valid email address and phone number."
            )
        }

    # 4. Check action verbs
    def check_action_verbs(self, text):

        text_lower = text.lower()

        found_verbs = []

        for verb in self.action_verbs:

            pattern = r"\b" + re.escape(verb) + r"\b"

            if re.search(pattern, text_lower):
                found_verbs.append(verb)

        passed = len(found_verbs) >= 2

        return {
            "passed": passed,
            "found_verbs": found_verbs,
            "verb_count": len(found_verbs),
            "message": (
                "Good use of action verbs."
                if passed
                else "Use more action verbs to describe your work."
            )
        }

    # 5. Check quantifiable achievements
    def check_quantifiable_achievements(self, text):

        text_lower = text.lower()

        achievement_verbs = (
            r"\b(?:improved|increased|reduced|decreased|saved|"
            r"generated|achieved|boosted|grew|cut|raised|lowered|"
            r"delivered|managed|led|completed|processed|served|"
            r"built|created|developed|optimized|automated|supported)\b"
        )

        measurement_units = (
            r"(?:%|percent|users|customers|members|projects|tasks|"
            r"hours|minutes|seconds|days|weeks|months|years|"
            r"records|reports|applications|employees|students|"
            r"clients|products|sales|downloads|requests|"
            r"transactions|teams|websites|features|bugs)"
        )

        number = (
            r"(?:\d+(?:\.\d+)?|"
            r"one|two|three|four|five|six|seven|eight|nine|ten|"
            r"eleven|twelve|fifteen|twenty|thirty|forty|fifty|"
            r"hundred|thousand)"
        )

        patterns = [

            # Example: Improved performance by 25%
            (
                achievement_verbs
                + r".{0,100}?"
                + number
                + r"\s*"
                + measurement_units
            ),

            # Example: Managed a team of 5 members
            (
                achievement_verbs
                + r".{0,100}?"
                + number
                + r"\s+"
                + measurement_units
            ),

            # Example: Completed two academic software projects
            # Allows up to four words between number and unit.
            (
                achievement_verbs
                + r".{0,50}?"
                + number
                + r"(?:\s+\w+){0,4}\s+"
                + measurement_units
            ),

            # Example: 20% improvement in performance
            (
                number
                + r"\s*"
                + measurement_units
                + r".{0,100}?"
                + r"(?:improvement|increase|reduction|growth)"
            )
        ]

        achievement_matches = []

        for pattern in patterns:

            matches = re.findall(pattern, text_lower)

            achievement_matches.extend(matches)

        achievement_matches = list(dict.fromkeys(
            achievement_matches
        ))

        passed = len(achievement_matches) >= 1

        return {
            "passed": passed,
            "numbers_found": achievement_matches,
            "achievement_count": len(achievement_matches),
            "message": (
                "Resume contains measurable achievements."
                if passed
                else "Add measurable achievements, such as "
                     "improving performance by 20% or completing "
                     "2 academic projects."
            )
        }

    # 6. Check resume formatting
    def check_format_compliance(self, text):

        control_characters = re.findall(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            text
        )

        long_lines = [
            line for line in text.splitlines()
            if len(line) > 250
        ]

        passed = (
            len(control_characters) == 0
            and len(long_lines) == 0
        )

        return {
            "passed": passed,
            "control_characters_found": len(control_characters),
            "long_lines_found": len(long_lines),
            "message": (
                "Resume formatting looks acceptable."
                if passed
                else "Check the resume for unusual control "
                     "characters or excessively long lines."
            )
        }

    # 7. Check job-related keywords
    def check_keywords(self, text, technical_skills=None):

        if technical_skills is None:
            technical_skills = []

        text_lower = text.lower()

        found_keywords = []
        missing_keywords = []

        technical_skills = list(dict.fromkeys(
            skill.strip().lower()
            for skill in technical_skills
            if isinstance(skill, str) and skill.strip()
        ))

        for skill in technical_skills:

            pattern = (
                r"(?<!\w)"
                + re.escape(skill)
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                found_keywords.append(skill)
            else:
                missing_keywords.append(skill)

        total_keywords = len(technical_skills)
        matched_keywords = len(found_keywords)

        passed = (
            total_keywords > 0
            and matched_keywords / total_keywords >= 0.5
        )

        match_percentage = (
            round(
                (matched_keywords / total_keywords) * 100,
                2
            )
            if total_keywords > 0 else 0
        )

        return {
            "passed": passed,
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords,
            "keyword_count": matched_keywords,
            "total_keywords": total_keywords,
            "match_percentage": match_percentage,
            "message": (
                "Good job skill matching."
                if passed
                else "Improve your resume by adding relevant "
                     "job skills you genuinely possess."
            )
        }

    # 8. Run all ATS checks
    def check_resume(self, resume_text, technical_skills=None):

        results = {}

        results["resume_length"] = self.check_resume_length(
            resume_text
        )

        results["required_sections"] = self.check_required_sections(
            resume_text
        )

        results["contact_information"] = (
            self.check_contact_information(resume_text)
        )

        results["action_verbs"] = self.check_action_verbs(
            resume_text
        )

        results["quantifiable_achievements"] = (
            self.check_quantifiable_achievements(resume_text)
        )

        results["format_compliance"] = self.check_format_compliance(
            resume_text
        )

        results["keywords"] = self.check_keywords(
            resume_text,
            technical_skills
        )

        passed_count = sum(
            1 for result in results.values()
            if result["passed"]
        )

        total_checks = len(results)

        return {
            "results": results,
            "passed_checks": passed_count,
            "total_checks": total_checks,
            "failed_checks": total_checks - passed_count
        }