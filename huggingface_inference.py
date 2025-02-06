import os
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face token from environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Check if the token is available
if not HUGGINGFACE_TOKEN:
    raise ValueError("Hugging Face token not found in .env file")

# Define the model name
model_name = "HarleyCooper/GRPOtuned"

# Load model directly
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)

    # Example usage (replace with your desired input)
    inputs = tokenizer("Hello, how are you?", return_tensors="pt")
    outputs = model.generate(**inputs)
    generated_text = tokenizer.decode(outputs[0])
    print("Direct Model Response:", generated_text)

except Exception as e:
    print(f"Error loading model directly: {e}")
