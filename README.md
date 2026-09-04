# ResumeIntel 🚀

**ResumeIntel** is an AI-powered resume intelligence platform that helps candidates understand how well their resume matches a specific company and job role.

Instead of relying only on generic ATS keyword checking, ResumeIntel combines resume analysis, job-description matching, ATS checks, company-specific job intelligence, and actionable improvement insights.

## ✨ Features

- 📄 **Resume Parsing** — Extracts relevant information from uploaded resumes.
- 🎯 **Job Description Matching** — Compares resume skills with the target job description.
- 🏢 **Company Intelligence** — Provides company-specific job insights.
- 🤖 **AI-Powered Analysis** — Generates contextual resume insights.
- 📊 **Fit Score** — Calculates how well the resume matches the target opportunity.
- 🧩 **Skill Gap Analysis** — Shows matched and missing skills.
- 🔍 **ATS Compatibility** — Evaluates ATS-related resume factors.
- 💡 **Actionable Insights** — Helps candidates identify areas for improvement.

## 🧠 How It Works

ResumeIntel follows a two-stage analysis approach.

### 1. Deterministic Analysis

The system performs:

- Resume parsing
- Skill extraction
- Job-description matching
- ATS checks
- Experience evaluation
- Project evaluation
- Score calculation

### 2. AI-Assisted Analysis

AI is used for:

- Company intelligence
- Contextual resume analysis
- Role-specific insights
- Understanding the relationship between the candidate's resume and the target opportunity

This approach keeps the core scoring transparent while using AI where contextual reasoning adds value.

## 📊 Scoring System

The overall score is calculated using four major components:

| Component | Weight |
|---|---:|
| Skills Match | 40% |
| Experience | 25% |
| Projects | 20% |
| ATS Compatibility | 15% |

The final score is calculated out of **100**.

### Resume Grades

| Score | Grade | Description |
|---|---|---|
| 80–100 | Excellent Resume | Your resume is strongly aligned with this opportunity. |
| 60–79.99 | Good Resume | Your resume has a solid foundation with a few areas to strengthen. |
| 40–59.99 | Good Foundation | Your resume has relevant strengths, but improving a few key areas could increase your match. |
| 0–39.99 | Room to Grow | Your resume has a foundation to build on. Focus on the recommended improvements to strengthen your match. |

## 🏗️ Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask
- Gunicorn

### Resume Processing

- PDF parsing
- python-docx
- Resume text extraction

### Job Intelligence

- Greenhouse Jobs API

### AI

- Google Gemini API

### Deployment

- Vercel
- Render

## 📁 Project Structure

```text
ResumeIntel/
│
├── backend/
│   ├── ai/
│   ├── jobs/
│   ├── scoring/
│   ├── uploads/
│   ├── app.py
│   ├── pipeline.py
│   ├── resume_processor.py
│   └── ...
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── uploads/
│
├── requirements.txt
├── README.md
└── .gitignore
