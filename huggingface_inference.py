import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face token from environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Check if the token is available
if not HUGGINGFACE_TOKEN:
    raise ValueError("Hugging Face token not found in .env file")

def generate_text(prompt, model_name="HarleyCooper/GRPOtuned", max_length=50):
    """
    Generate text using Hugging Face's Inference API with Qwen2 parameters
    """
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    
    # Proper formatting for Qwen2 model
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_length,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False,
            "stop": ["</s>"]  # Qwen2 end token
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Handle the Qwen2 response format
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                return result[0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during Hugging Face API call: {e}")
        return None

if __name__ == "__main__":
    # Get prompt from command line arguments
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello, how are you?"
    
    # Generate text
    generated_text = generate_text(prompt)
    if generated_text:
        print("Generated Text:", generated_text)
