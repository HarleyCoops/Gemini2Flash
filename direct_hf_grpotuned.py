import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

def generate_math_solution_direct(prompt, max_new_tokens=12000, temperature=1.5):
    """
    Uses a direct model loading approach to generate a math problem solution using the GRPOtuned model.
    
    The GRPOtuned model is expected to output reasoning steps and a final answer in an XML format.
    
    Parameters:
      prompt (str): The input text prompt containing the math problem.
      max_new_tokens (int): Maximum number of tokens to generate. Default is 12000.
      temperature (float): Temperature for generation. Default is 1.5.
    
    Returns:
      str: The generated output.
    """
    model_name = "HarleyCooper/GRPOtuned"
    # Load the tokenizer and model directly.
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Tokenize the prompt.
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate output tokens from the model.
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, temperature=temperature)
    
    # Decode the tokens to string.
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter a math problem: ")
    solution = generate_math_solution_direct(prompt)
    print("Generated Output:")
    print(solution)
    
    # Save the prompt and solution to math_results.jsonl, preserving all reasoning and answer
    result = {
        "prompt": prompt,
        "generated_output": solution
    }
    with open("math_results.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")
    print("Result saved to math_results.jsonl")
