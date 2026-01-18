import requests
from chatbot.logger import setup_logger
from config import config

logger = setup_logger(__name__)

def call_huggingface(prompt: str, max_tokens: int = 64) -> str:
    """
    Call HuggingFace model using the new router chat completions API.
    
    Args:
        prompt: The prompt to send to the model
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text from the model
    """
    if not config.HF_API_TOKEN:
        logger.error("HF_API_TOKEN is not set")
        raise RuntimeError("HF_API_TOKEN is not set")

    try:
        # Use the new router endpoint with chat completions format
        API_URL = "https://router.huggingface.co/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {config.HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Chat completions format
        payload = {
            "model": "meta-llama/Llama-3.2-1B-Instruct:fastest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        logger.info(f"Calling HF API with prompt length: {len(prompt)}")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=config.AI_TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"API Error ({response.status_code}): {response.text}")
            raise RuntimeError(f"API Error ({response.status_code}): {response.text}")
        
        result = response.json()
        
        # Extract message content from chat completions response
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0].get("message", {})
            content = message.get("content", "")
            logger.info(f"Successfully generated response: {len(content)} chars")
            return content
        
        return str(result)
            
    except Exception as e:
        logger.error(f"HF Error: {type(e).__name__}: {str(e)}")
        raise RuntimeError(f"{type(e).__name__}: {str(e)}")
