from flask import Flask, request, jsonify, render_template
from chatbot.engine import get_response
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    
    # Get response with type metadata
    response_data = get_response(user_message)
    
    return jsonify({
        "reply": response_data["reply"],
        "type": response_data["type"]
    })

@app.route("/debug/hf", methods=["GET"])
def debug_hf():
    """
    Test endpoint to verify HuggingFace API is working.
    Returns API status and a test response.
    """
    hf_token = os.getenv("HF_API_TOKEN")
    
    if not hf_token:
        return jsonify({
            "status": "error",
            "message": "HF_API_TOKEN not set",
            "hf_working": False
        }), 400
    
    try:
        from chatbot.ai.hf_client import call_huggingface
        test_prompt = "Rewrite this: We are open 9 AM to 5 PM"
        result = call_huggingface(test_prompt, max_tokens=32)
        
        return jsonify({
            "status": "success",
            "message": "HuggingFace API is working!",
            "hf_working": True,
            "test_output": str(result),
            "token_present": True
        })
    except Exception as e:
        error_msg = str(e)
        print(f"Debug HF Error: {error_msg}")
        return jsonify({
            "status": "error",
            "message": error_msg,
            "hf_working": False,
            "token_present": bool(hf_token)
        }), 500

if __name__ == "__main__":
    # Listen on 0.0.0.0 for Docker/Podman compatibility
    app.run(host="0.0.0.0", port=5000, debug=False)
