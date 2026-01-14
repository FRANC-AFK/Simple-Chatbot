from flask import Flask, request, jsonify, render_template
from chatbot.engine import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    reply = get_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
