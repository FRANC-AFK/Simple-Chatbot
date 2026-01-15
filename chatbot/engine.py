from chatbot.rules import RULES
from chatbot.nlp import normalize
from chatbot.ai.generator import generate_ai_response

USE_AI = True  # master switch

def get_response(message: str) -> dict:
    """
    Get chatbot response with metadata.
    
    Returns:
        dict: {
            "reply": str,
            "type": "rule" | "ai" | "fallback"
        }
    """
    words = normalize(message)

    best_match = None
    highest_score = 0

    for rule in RULES.values():
        score = len(words & rule["keywords"])
        if score > highest_score:
            highest_score = score
            best_match = rule

    if best_match and highest_score > 0:
        base_response = best_match["response"]

        if USE_AI:
            reply, response_type = generate_ai_response(base_response)
            return {
                "reply": reply,
                "type": response_type  # "ai" or "rule" (fallback)
            }

        return {
            "reply": base_response,
            "type": "rule"
        }

    return {
        "reply": "Sorry, I can only help with specific inquiries like hours, pricing, contact details, or location.",
        "type": "fallback"
    }
