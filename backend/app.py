from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from resume_processor import (
    extract_text_from_pdf,
    extract_skills,
    extract_projects,
    extract_experience,
    extract_name,
    extract_education
)

from job_processor import extract_job_skills
from comparison import compare_skills


app = Flask(__name__)
CORS(app)

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Allowed resume file types
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# FILE VALIDATION
# --------------------------------------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "ResumeIntel backend is running!"
    })


# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

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

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Extract resume information
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


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

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

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    return jsonify({
        "success": True,
        "message": "Resume uploaded successfully",
        "filename": filename
    }), 200


# --------------------------------------------------
# JOB DESCRIPTION ANALYSIS
# --------------------------------------------------

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

    job_text = file.read().decode("utf-8")

    skills = extract_job_skills(job_text)

    return jsonify({
        "status": "success",
        "required_skills": skills
    })


# --------------------------------------------------
# FULL RESUME + JOB ANALYSIS
# --------------------------------------------------

@app.route("/full-analyze", methods=["POST"])
def full_analyze():

    if "resume" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No resume file uploaded"
        }), 400

    if "job" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No job description uploaded"
        }), 400

    resume_file = request.files["resume"]
    job_file = request.files["job"]

    if resume_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No resume selected"
        }), 400

    if job_file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No job description selected"
        }), 400

    # -------------------------------
    # RESUME PROCESSING
    # -------------------------------

    resume_filename = secure_filename(resume_file.filename)

    if not resume_filename:
        return jsonify({
            "status": "error",
            "message": "Invalid resume filename"
        }), 400

    resume_path = os.path.join(
        UPLOAD_FOLDER,
        resume_filename
    )

    resume_file.save(resume_path)

    resume_text = extract_text_from_pdf(resume_path)

    resume_skills = extract_skills(resume_text)
    projects = extract_projects(resume_text)
    experience = extract_experience(resume_text)
    name = extract_name(resume_text)
    education = extract_education(resume_text)

    # -------------------------------
    # JOB PROCESSING
    # -------------------------------

    job_text = job_file.read().decode("utf-8")

    job_skills = extract_job_skills(job_text)

    # -------------------------------
    # COMPARISON
    # -------------------------------

    comparison = compare_skills(
        resume_skills,
        job_skills
    )

    # -------------------------------
    # FINAL RESPONSE
    # -------------------------------

    return jsonify({
        "status": "success",

        "name": name,
        "education": education,
        "skills": resume_skills,
        "projects": projects,
        "experience": experience,

        "required_skills": job_skills,

        "matched_skills": comparison["matched_skills"],
        "missing_skills": comparison["missing_skills"],
        "fit_score": comparison["fit_score"]
    })


# --------------------------------------------------
# RUN FLASK SERVER
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080
    )