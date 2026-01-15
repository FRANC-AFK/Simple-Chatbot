
def rephrase_prompt(text: str) -> str:
    return (
        "Rewrite the following response so it sounds polite, clear, and professional.\n"
        "Do not add new information.\n"
        "Do not ask questions.\n"
        "Keep it under two sentences.\n\n"
        f"Response: {text}"
    )
