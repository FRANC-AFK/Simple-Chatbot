from flask import Flask, request, jsonify, render_template
from chatbot.engine import get_response
from chatbot.rate_limiter import rate_limiter
from chatbot.logger import setup_logger
from config import config
import os

app = Flask(__name__)
logger = setup_logger(__name__)

# Initialize rate limiter with config
rate_limiter.max_requests = config.RATE_LIMIT_MAX_REQUESTS
rate_limiter.window = __import__('datetime').timedelta(seconds=config.RATE_LIMIT_WINDOW_SECONDS)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Rate limiting by IP
    client_ip = request.remote_addr
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return jsonify({
            "reply": "Too many requests. Please wait a moment.",
            "type": "error"
        }), 429
    
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({
            "reply": "Please enter a message.",
            "type": "error"
        }), 400
    
    logger.info(f"Processing message from {client_ip}: {user_message[:50]}...")
    
    # Get response with type metadata
    response_data = get_response(user_message)
    
    return jsonify({
        "reply": response_data["reply"],
        "type": response_data["type"]
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for container orchestration."""
    return jsonify({
        "status": "healthy",
        "ai_enabled": config.USE_AI,
        "cache_enabled": config.ENABLE_CACHE,
        "hf_configured": bool(config.HF_API_TOKEN)
    }), 200

@app.route("/debug/hf", methods=["GET"])
def debug_hf():
    """
    Test endpoint to verify HuggingFace API is working.
    Returns API status and a test response.
    """
    if not config.HF_API_TOKEN:
        return jsonify({
            "status": "error",
            "message": "HF_API_TOKEN not set",
            "hf_working": False
        }), 400
    
    try:
        from chatbot.ai.hf_client import call_huggingface
        test_prompt = "Rewrite this: We are open 9 AM to 5 PM"
        result = call_huggingface(test_prompt, max_tokens=32)
        
        logger.info("HF API test successful")
        return jsonify({
            "status": "success",
            "message": "HuggingFace API is working!",
            "hf_working": True,
            "test_output": str(result),
            "token_present": True
        })
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Debug HF Error: {error_msg}")
        return jsonify({
            "status": "error",
            "message": error_msg,
            "hf_working": False,
            "token_present": bool(config.HF_API_TOKEN)
        }), 500

if __name__ == "__main__":
    # Listen on 0.0.0.0 for Docker/Podman compatibility
    logger.info(f"Starting Flask app on {config.HOST}:{config.PORT}")
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
