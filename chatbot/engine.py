from chatbot.rules import RULES
from chatbot.nlp import normalize

def get_response(message: str) -> str:
    words = normalize(message)

    best_match = None
    highest_score = 0

    for rule in RULES.values():
        score = len(words & rule["keywords"])
        if score > highest_score:
            highest_score = score
            best_match = rule

    if best_match and highest_score > 0:
        return best_match["response"]

    return "Sorry, I didn't quite understand that. Try asking for help."
