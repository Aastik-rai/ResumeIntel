from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename  #(to change filename to a safe filename)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024    #maximum uploaod size(file)
ALLOWED_EXTENSIONS = {"pdf", "docx"}     #allowed filetypes is only document and pdf

# Allow our frontend to communicate with the backend
CORS(app)

def allowed_file(filename):   #it passes extension of filename to ALLOWEDextension query to check true or false 
    return(
        "." in filename
        and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "ResumeIntel backend is running!"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data =request.get_json()
    if not data:
        return jsonify({
            "success":False,
            "message":"Request body is required"
        }), 400
   
    company=data.get("company")
    role=data.get("role")
    if not company:
        return jsonify({
            "success":False,
            "message":"Company is required"
        }), 400

    if not role:
        return jsonify({
            "success":False,
            "message":"role is required"
        }), 400

    return jsonify({
        "success": True,
        "company": company,
        "role": role,
        "message": "Analysis request received"
    }),200


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({
            "success":False,
            "message":"Resmue file is required"
        }),400
    file=request.files["resume"]
    if file.filename=="":
        return jsonify({
            "success":False,
            "message":"No file selected"
        }),400


    if not allowed_file(file.filename):
        return jsonify({
            "success":False,
            "message":"only PDF and DOCX files are allowed"
        }),400
    filename=secure_filename(file.filename)

    if not filename:
        return jsonify({
            "success":False,
            "message":"Invalid filename"
        }),400

    upload_folder="uploads"
    os.makedirs(upload_folder,exist_ok=True)


    file_path=os.path.join(upload_folder,filename)

    file.save(file_path)
    return jsonify({
        "success": True,
        "message": "Resume uploaded successfully",
        "filename": filename
    }),200



if __name__ == "__main__":
    app.run(debug=True)