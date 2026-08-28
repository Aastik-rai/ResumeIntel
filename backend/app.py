from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow our frontend to communicate with the backend
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "ResumeIntel backend is running!"
    })


if __name__ == "__main__":
    app.run(debug=True)