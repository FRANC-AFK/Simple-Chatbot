from chatbot.ai.hf_client import call_huggingface
from chatbot.ai.prompts import rephrase_prompt

def generate_ai_response(base_response: str) -> tuple:
    """
    Generate AI-polished response.
    
    Returns:
        tuple: (response_text, response_type)
        - response_type: "ai" if AI succeeded, "rule" if fallback to base
    """
    try:
        prompt = rephrase_prompt(base_response)
        ai_text = call_huggingface(prompt)
        return ai_text.strip(), "ai"
    except Exception as e:
        # Fail safe: return original rule response
        print(f"AI generation failed: {e}")
        return base_response, "rule"
