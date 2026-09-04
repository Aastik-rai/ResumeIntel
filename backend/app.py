from flask import Flask, jsonify, request
from backend.scoring.scorer import calculate_score
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from backend.scoring.scorer import calculate_ats_score

from backend.resume_processor import (
    extract_text_from_pdf,
    extract_skills,
    extract_projects,
    extract_experience,
    extract_name,
    extract_education
)

from backend.job_processor import extract_job_skills
from backend.comparison import compare_skills
from backend.pipeline import analyze_resume_for_company


app = Flask(__name__)
CORS(app)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Allowed resume file types
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Store uploads inside backend/uploads
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "ResumeIntel backend is running!"
    })


@app.route("/analyze", methods=["POST"])
def analyze_resume():

    company = request.form.get("company")
    role = request.form.get("role")
    file = request.files.get("resume")

    if not company:
        return jsonify({
            "success": False,
            "message": "Company is required"
        }), 400

    if not role:
        return jsonify({
            "success": False,
            "message": "Role is required"
        }), 400

    if not file:
        return jsonify({
            "success": False,
            "message": "Resume file is required"
        }), 400

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only PDF and DOCX files are allowed"
        }), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({
            "success": False,
            "message": "Invalid filename"
        }), 400

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(file_path)

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)
    projects = extract_projects(text)
    experience = extract_experience(text)
    name = extract_name(text)
    education = extract_education(text)

    return jsonify({
        "status": "success",
        "company": company,
        "role": role,
        "name": name,
        "education": education,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "filename": filename
    })


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "message": "Resume file is required"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Only PDF and DOCX files are allowed"
        }), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({
            "success": False,
            "message": "Invalid filename"
        }), 400

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(file_path)

    return jsonify({
        "success": True,
        "message": "Resume uploaded successfully",
        "filename": filename
    }), 200


@app.route("/job-analyze", methods=["POST"])
def analyze_job():

    if "job" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No job description uploaded"
        }), 400

    file = request.files["job"]

    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    job_text = file.read().decode(
        "utf-8",
        errors="replace"
    )

    skills = extract_job_skills(job_text)

    return jsonify({
        "status": "success",
        "required_skills": skills
    })


@app.route("/full-analyze", methods=["POST"])
def full_analyze():

    # -----------------------------
    # Validate company and role
    # -----------------------------

    company = request.form.get("company", "").strip()
    role = request.form.get("role", "").strip()

    if not company:
        return jsonify({
            "status": "error",
            "message": "Company is required"
        }), 400

    if not role:
        return jsonify({
            "status": "error",
            "message": "Role is required"
        }), 400

    # -----------------------------
    # Validate resume
    # -----------------------------

    if "resume" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No resume file uploaded"
        }), 400

    resume_file = request.files["resume"]

    if resume_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No resume selected"
        }), 400

    if not allowed_file(resume_file.filename):
        return jsonify({
            "status": "error",
            "message": "Only PDF and DOCX files are allowed"
        }), 400

    resume_filename = secure_filename(
        resume_file.filename
    )

    if not resume_filename:
        return jsonify({
            "status": "error",
            "message": "Invalid resume filename"
        }), 400

    # -----------------------------
    # Save resume
    # -----------------------------

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        resume_filename
    )

    resume_file.save(resume_path)

    # -----------------------------
    # Extract resume information
    # -----------------------------

    resume_text = extract_text_from_pdf(
        resume_path
    )
    job_text = ""

    if "job" in request.files:
        job_file = request.files["job"]
        job_text = job_file.read().decode(
            "utf-8",
            errors="replace"
        )

    resume_data = {
        "skills": extract_skills(resume_text),
        "projects": extract_projects(resume_text),
        "experience": extract_experience(resume_text),
        "name": extract_name(resume_text),
        "education": extract_education(resume_text)
    }
    ats_score = calculate_ats_score(
    resume_text,
    resume_data
    )
    

    # -----------------------------
    # Run company intelligence
    # -----------------------------

    try:

        result = analyze_resume_for_company(
            company,
            role,
            resume_data,
            job_text
        )

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": "Company analysis failed",
            "error": str(e)
        }), 500

    # -----------------------------
    #          Calculate final score
    # -----------------------------

    skills_score = result["fit_score"]
    experience_count = len(resume_data.get("experience", []))
    experience_score = min(experience_count * 50, 100)

    projects_count = len(resume_data.get("projects", []))
    projects_score = min(projects_count * 25, 100)

    overall_score = calculate_score(
        skills_score,
        experience_score,
        projects_score,
        ats_score
    )
    
    

    # -----------------------------
    # Return final result
    # -----------------------------

    return jsonify({
        "status": "success",

        "company": company,
        "role": role,

        "name": resume_data["name"],
        "education": resume_data["education"],
        "skills": resume_data["skills"],
        "projects": resume_data["projects"],
        "experience": resume_data["experience"],

        "fit_score": result["fit_score"],
        "company_fit_score": result["company_fit_score"],
        "jd_fit_score": result["jd_fit_score"],
        "ats_score": ats_score,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "projects_score": projects_score,
        "overall_score": overall_score,
        "jd_skills": result["jd_skills"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "company_profile": result["company_profile"],
        "matching_jobs": result["matching_jobs"]
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080
    )