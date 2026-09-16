from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app)

# Latest frame
latest_data = {
    "message": "Waiting for main computer..."
}

# Keep only a small rolling history.
# This prevents Render from storing/sending hundreds of large images.
MAX_HISTORY = 15
history = deque(maxlen=MAX_HISTORY)


@app.route("/")
def home():
    return "Computer's Vision relay is running."


@app.route("/update", methods=["POST"])
def update():
    global latest_data

    data = request.json

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    # Only keep the data we actually need.
    latest_data = {
        "image": data.get("image"),
        "label": data.get("label"),
        "timestamp": data.get("timestamp")
    }

    # Add the new frame to rolling history.
    history.append(latest_data.copy())

    return jsonify({
        "success": True
    })


@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(latest_data)


@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({
        "frames": list(history)
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
