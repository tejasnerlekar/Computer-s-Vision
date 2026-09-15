from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_data = {
    "message": "Waiting for main computer..."
}

@app.route("/")
def home():
    return "Computer's Vision relay is running."

@app.route("/update", methods=["POST"])
def update():
    global latest_data
    latest_data = request.json
    return jsonify({"success": True})


@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
