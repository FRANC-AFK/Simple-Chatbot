import os
import traceback
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "google/flan-t5-base"

def call_huggingface(prompt: str, max_tokens: int = 64) -> str:
    """
    Call HuggingFace model using the modern InferenceClient.
    
    Args:
        prompt: The prompt to send to the model
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text from the model
    """
    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN is not set")

    try:
        client = InferenceClient(api_key=HF_API_TOKEN)
        
        # text_generation returns a TextGenerationResponse object
        response = client.text_generation(
            model=HF_MODEL,
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=0.3
        )
        
        # Convert response to string if needed
        if hasattr(response, 'generated_text'):
            return response.generated_text
        else:
            return str(response)
            
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"HF Error: {error_msg}")
        print(traceback.format_exc())
        raise RuntimeError(error_msg)
