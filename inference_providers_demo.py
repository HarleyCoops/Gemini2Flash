import sys
import json
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

def generate_with_provider(prompt, provider="sambanova", max_tokens=6000):
    """
    Uses Hugging Face's InferenceClient to generate a math problem solution
    by routing through a specified Inference Provider.
    
    The model used is 'HarleyCooper/GRPOtuned', and this function sends a chat message
    to the model through the provider's API. The generated output is expected to contain
    both the reasoning and final answer, formatted in XML.
    
    Parameters:
      prompt (str): The math problem prompt.
      provider (str): The inference provider to use. Default is "sambanova".
      max_tokens (int): Maximum number of tokens to generate. Default is 6000.
      
    Returns:
      dict: The full API response from the provider.
    """
    # Load the API key for sambanova from environment variable.
    api_key = os.getenv("SAMBANOVA_API_KEY")
    if not api_key:
        raise ValueError("SAMBANOVA_API_KEY not found in environment variables.")
    # Initialize the inference client.
    client = InferenceClient(provider=provider, api_key=api_key)
    
    # Set up the chat message for the prompt.
    messages = [{"role": "user", "content": prompt}]
    
    # Call the provider's chat completion endpoint.
    response = client.chat.completions.create(
        model="HarleyCooper/GRPOtuned",
        messages=messages,
        max_tokens=max_tokens
    )
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter a math problem: ")
    output = generate_with_provider(prompt)
    # Print the JSON response in a formatted manner.
    print("Response from Inference Provider:")
    print(json.dumps(output, indent=2))
    
    # Optionally, you can save the result to a JSONL file.
    result = {
        "prompt": prompt,
        "inference_provider_response": output
    }
    with open("provider_math_results.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")
    print("Result saved to provider_math_results.jsonl")
