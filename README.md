# AI ATS Resume Checker

## 🚀 Live Demo

Try the application here: https://ai-ats-resume-checker-tdqr.onrender.com

## Project Overview

The AI ATS Resume Checker is a Python-based web application that analyzes resumes and evaluates their compatibility with Applicant Tracking Systems (ATS).

It helps users identify resume issues, understand their ATS score, and improve their resumes through actionable recommendations.

## Features

- Supports PDF, DOCX, and TXT resume formats.
- Extracts and processes resume text.
- Identifies technical skills, soft skills, and keywords.
- Checks important resume sections.
- Evaluates contact information and action verbs.
- Identifies quantifiable achievements.
- Checks basic resume formatting.
- Calculates an overall ATS compatibility score.
- Provides personalized improvement recommendations.
- Identifies missing skills based on job requirements.
- Generates downloadable PDF analysis reports.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- Natural Language Processing (NLP)
- PyMuPDF
- python-docx
- ReportLab

## Project Structure

```text
AI_ATS_RESUME_CHECKER/
│
├── app.py
├── resume_parser.py
├── nlp_processor.py
├── ats_checker.py
├── scoring.py
├── recommendations.py
├── report_generator.py
├── ats_rules.json
├── keywords.json
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── uploads/
└── reports/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kusumagowda1013-star/AI_ATS_RESUME_CHECKER.git
```

### 2. Open the project folder

```bash
cd AI_ATS_RESUME_CHECKER
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

Visit:

http://127.0.0.1:5000

## How to Use

1. Open the application in your browser.
2. Upload your resume in PDF, DOCX, or TXT format.
3. Enter the relevant job description or required job skills if prompted.
4. Submit the resume for analysis.
5. View your ATS score and detailed evaluation.
6. Review the improvement recommendations.
7. Download the generated PDF report.

## Important Note

The ATS score is an indicative evaluation based on the checks implemented in this project. It does not guarantee selection by an employer or compatibility with every ATS platform.

Users should include only skills and experience they genuinely possess.

## Author

Kusuma

## Internship Project

**Organization:** Data Alcott Systems  
**Project:** AI ATS Resume Checker  
**Task Code:** AI-RP-003
