import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


class ReportGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = ParagraphStyle(
            "ReportTitle",
            parent=self.styles["Title"],
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=20
        )

        self.heading_style = ParagraphStyle(
            "SectionHeading",
            parent=self.styles["Heading2"],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10
        )

        self.normal_style = self.styles["BodyText"]

    def generate_report(
        self,
        score_report,
        ats_report,
        recommendations_report,
        output_path
    ):

        output_folder = os.path.dirname(output_path)

        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

        document = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        content = []

        # Report title
        content.append(
            Paragraph(
                "AI ATS RESUME ANALYSIS REPORT",
                self.title_style
            )
        )

        content.append(
            Paragraph(
                f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                self.normal_style
            )
        )

        content.append(Spacer(1, 20))

        # ATS Score
        content.append(
            Paragraph("1. ATS SCORE SUMMARY", self.heading_style)
        )

        score_data = [
            ["ATS Score", "Grade"],
            [
                f"{score_report['ats_score']} / 100",
                score_report["grade"]
            ]
        ]

        score_table = Table(
            score_data,
            colWidths=[230, 230]
        )

        score_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, 1), colors.lightblue),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("PADDING", (0, 0), (-1, -1), 10)
            ])
        )

        content.append(score_table)
        content.append(Spacer(1, 15))

        # ATS Rule Results
        content.append(
            Paragraph("2. ATS RULE CHECK RESULTS", self.heading_style)
        )

        rule_data = [
            ["ATS Rule", "Status", "Weight", "Earned"]
        ]

        for check_name, details in score_report["breakdown"].items():

            rule_data.append([
                check_name.replace("_", " ").title(),
                details["status"],
                str(details["weight"]),
                str(details["earned_score"])
            ])

        rule_table = Table(
            rule_data,
            colWidths=[200, 80, 80, 80]
        )

        rule_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("PADDING", (0, 0), (-1, -1), 7)
            ])
        )

        content.append(rule_table)

        # ATS Recommendations
        content.append(
            Paragraph("3. IMPROVEMENT RECOMMENDATIONS", self.heading_style)
        )

        ats_recommendations = recommendations_report.get(
            "ats_recommendations", []
        )

        if ats_recommendations:

            for item in ats_recommendations:

                content.append(
                    Paragraph(
                        f"<b>{item['category'].replace('_', ' ').title()}</b>",
                        self.normal_style
                    )
                )

                content.append(
                    Paragraph(
                        item["suggestion"],
                        self.normal_style
                    )
                )

                content.append(Spacer(1, 8))

        else:

            content.append(
                Paragraph(
                    "No ATS recommendations available.",
                    self.normal_style
                )
            )

        # Missing Skills
        content.append(
            Paragraph("4. SKILL GAP ANALYSIS", self.heading_style)
        )

        skill_report = recommendations_report.get(
            "skill_recommendations", {}
        )

        missing_skills = skill_report.get(
            "missing_skills", []
        )

        if missing_skills:

            content.append(
                Paragraph(
                    "Skills not found in the resume:",
                    self.normal_style
                )
            )

            for skill in missing_skills:

                content.append(
                    Paragraph(
                        f"- {skill.title()}",
                        self.normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No missing skills identified.",
                    self.normal_style
                )
            )

        content.append(Spacer(1, 10))

        content.append(
            Paragraph(
                skill_report.get("suggestion", ""),
                self.normal_style
            )
        )

        # Final Summary
        content.append(
            Paragraph("5. FINAL SUMMARY", self.heading_style)
        )

        content.append(
            Paragraph(
                f"Total ATS checks: {ats_report['total_checks']}",
                self.normal_style
            )
        )

        content.append(
            Paragraph(
                f"Passed checks: {ats_report['passed_checks']}",
                self.normal_style
            )
        )

        content.append(
            Paragraph(
                f"Failed checks: {ats_report['failed_checks']}",
                self.normal_style
            )
        )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Note: This report provides an estimated ATS "
                "compatibility assessment. Actual ATS results "
                "may vary depending on the employer's software "
                "and job-specific requirements.",
                self.normal_style
            )
        )

        document.build(content)

        return output_path