class ScoringEngine:

    def __init__(self):

        self.weights = {
            "resume_length": 15,
            "required_sections": 20,
            "contact_information": 15,
            "action_verbs": 10,
            "quantifiable_achievements": 10,
            "format_compliance": 15,
            "keywords": 15
        }

    def calculate_score(self, ats_report):

        results = ats_report["results"]

        total_score = 0
        breakdown = {}

        for check_name, weight in self.weights.items():

            if check_name not in results:
                raise ValueError(
                    f"Missing ATS check: {check_name}"
                )

            passed = results[check_name]["passed"]

            earned_score = weight if passed else 0

            total_score += earned_score

            breakdown[check_name] = {
                "weight": weight,
                "earned_score": earned_score,
                "status": "PASS" if passed else "FAIL"
            }

        score = round(total_score, 2)

        if score >= 90:
            grade = "Excellent"
        elif score >= 75:
            grade = "Good"
        elif score >= 60:
            grade = "Average"
        elif score >= 40:
            grade = "Needs Improvement"
        else:
            grade = "Poor"

        return {
            "ats_score": score,
            "grade": grade,
            "breakdown": breakdown,
            "total_possible_score": 100
        }