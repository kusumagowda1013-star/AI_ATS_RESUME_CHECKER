class RecommendationEngine:

    def __init__(self):

        self.recommendations = {
            "resume_length": (
                "Keep your resume within the recommended word "
                "limit. Include relevant education, skills, "
                "projects and experience."
            ),

            "required_sections": (
                "Add all important resume sections, such as "
                "Education, Skills, Experience and Projects."
            ),

            "contact_information": (
                "Include a valid email address and phone number "
                "in your resume."
            ),

            "action_verbs": (
                "Use strong action verbs such as Developed, "
                "Designed, Implemented, Managed and Improved "
                "to describe your work."
            ),

            "quantifiable_achievements": (
                "Include measurable achievements using numbers, "
                "percentages or statistics wherever possible."
            ),

            "format_compliance": (
                "Improve resume readability. Avoid unusual "
                "characters, excessively long lines and "
                "complicated formatting."
            ),

            "keywords": (
                "Include relevant technical skills and keywords "
                "that match your target job description."
            )
        }

    def generate_recommendations(self, ats_report):

        results = ats_report["results"]

        suggestions = []

        for check_name, result in results.items():

            if not result["passed"]:

                suggestion = self.recommendations.get(
                    check_name
                )

                if suggestion:
                    suggestions.append({
                        "category": check_name,
                        "priority": "High",
                        "suggestion": suggestion
                    })

        if not suggestions:

            suggestions.append({
                "category": "Overall",
                "priority": "Low",
                "suggestion": (
                    "Your resume meets all the basic ATS "
                    "checks. Continue tailoring it to each "
                    "job description."
                )
            })

        return suggestions

    def generate_skill_recommendations(
        self,
        resume_skills,
        job_skills
    ):

        resume_skills = {
            skill.lower() for skill in resume_skills
        }

        job_skills = {
            skill.lower() for skill in job_skills
        }

        missing_skills = sorted(
            job_skills - resume_skills
        )

        if missing_skills:

            return {
                "missing_skills": missing_skills,
                "suggestion": (
                    "Consider developing these skills and "
                    "including them in your resume only "
                    "when you genuinely possess them."
                )
            }

        return {
            "missing_skills": [],
            "suggestion": (
                "Your listed skills match the supplied "
                "job skills."
            )
        }

    def generate_full_report(
        self,
        ats_report,
        resume_skills=None,
        job_skills=None
    ):

        if resume_skills is None:
            resume_skills = []

        if job_skills is None:
            job_skills = []

        ats_suggestions = self.generate_recommendations(
            ats_report
        )

        skill_suggestions = self.generate_skill_recommendations(
            resume_skills,
            job_skills
        )

        return {
            "ats_recommendations": ats_suggestions,
            "skill_recommendations": skill_suggestions
        }