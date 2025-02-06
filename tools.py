import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

def process_stream(response):
    """Process streaming response and return accumulated content."""
    content_parts = []
    try:
        for line in response.iter_lines():
            if line:
                try:
                    # Remove 'data: ' prefix if present
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        line_text = line_text[6:]

                    # Skip [DONE] message
                    if line_text == '[DONE]':
                        continue

                    json_line = json.loads(line_text)
                    if 'choices' in json_line and json_line['choices']:
                        content = json_line['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            print(content, end='', flush=True)  # Print each chunk as it comes
                            content_parts.append(content)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"\nError during streaming: {str(e)}")
    return ''.join(content_parts)

def deepseek_chat(prompt: str, model: str = "deepseek-chat") -> str:
    """
    Makes a call to the DeepSeek API using OpenAI-compatible format and logs the interaction.

    Args:
        prompt: The text prompt to send to DeepSeek
        model: The model to use ('deepseek-chat' for V3 or 'deepseek-reasoner' for R1)

    Returns:
        The model's response as a string
    """
    api_key = os.environ.get("DeepSeek_API_Key")
    if not api_key:
        return "Error: DEEPSEEK_API_KEY not found in environment variables"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    train_of_thought = None
    final_answer = None
    try:
        # First, get the streaming train of thought
        print(f"\nGetting train of thought for: {prompt[:50]}...")
        stream_data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Think step by step and show your reasoning. Be thorough but concise."},
                {"role": "user", "content": prompt}
            ],
            "stream": True,
            "temperature": 0.7,  # Add some randomness for creative thinking
            "max_tokens": 1000  # Ensure we get a full response
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=stream_data,
            timeout=90,  # Increased timeout
            stream=True
        )

        train_of_thought = process_stream(response)
        print("\n")  # Add newline after train of thought

        # Now get the final answer
        print("Getting final answer...")
        final_data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Based on the previous reasoning, provide a clear and concise final answer."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": train_of_thought},
                {"role": "user", "content": "Now provide a clear and concise final answer based on your reasoning."}
            ],
            "stream": False,
            "temperature": 0.3,  # Lower temperature for more focused final answer
            "max_tokens": 500  # Shorter limit for final answer
        }

        final_response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=final_data,
            timeout=90  # Increased timeout
        )

        if final_response.status_code != 200:
            error_detail = final_response.json() if final_response.text else "No error details available"
            error_msg = f"Error calling DeepSeek API (Status {final_response.status_code}): {error_detail}"
            final_answer = None
        else:
            final_result = final_response.json()
            final_answer = final_result["choices"][0]["message"]["content"]

        # Only log as successful if we have both train of thought and final answer
        success = bool(train_of_thought and final_answer)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": {
                "prompt": prompt,
                "model": model
            },
            "train_of_thought": train_of_thought if train_of_thought else None,
            "final_answer": final_answer if final_answer else None,
            "success": success
        }

        with open('deepseek_calls.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

        return final_answer

    except requests.exceptions.RequestException as e:
        error_msg = f"Error calling DeepSeek API: {str(e)}\nTrain of thought captured so far: {train_of_thought if train_of_thought else 'None'}"
        # Log error to JSONL file
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": {
                "prompt": prompt,
                "model": model
            },
            "error": error_msg,
            "train_of_thought": train_of_thought,  # Include partial train of thought if available
            "final_answer": None,
            "success": False
        }
        with open('deepseek_calls.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        return error_msg
    except (KeyError, IndexError) as e:
        error_msg = f"Error parsing DeepSeek API response: {str(e)}"
        # Log error to JSONL file
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": {
                "prompt": prompt,
                "model": model
            },
            "error": error_msg,
            "train_of_thought": train_of_thought,  # Include partial train of thought if available
            "final_answer": None,
            "success": False
        }
        with open('deepseek_calls.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        return error_msg

import subprocess

def huggingface_tool(prompt: str) -> str:
    """
    Runs inference using a Hugging Face model.
    """
    try:
        command = ["python", "huggingface_inference.py", prompt]
        process = subprocess.run(command, capture_output=True, text=True, timeout=60)
        process.check_returncode()
        return process.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running Hugging Face inference: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Hugging Face inference timed out."
    except Exception as e:
        return f"Error during Hugging Face inference: {e}"

def web_search(query: str) -> str:
    """Searches DuckDuckGo and returns a summarized snippet of results."""
    try:
        response = requests.get("https://api.duckduckgo.com/", params={
            'q': query,
            'format': 'json'
        })
        response.raise_for_status()
        ddg_data = response.json()
        summary = ddg_data.get("AbstractText")
        if not summary:
            return f"No results found for '{query}'."
        return summary
    except requests.exceptions.RequestException as e:
        return f'Error during web search: {e}'

def calculate(expression: str) -> str:
    """
    Safely calculates the result of a mathematical expression using ast.
    Supports basic arithmetic operations (+, -, *, /, **) and numbers only.
    """
    # Define allowed operators
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,  # Unary minus
    }

    def eval_expr(node):
        """Recursively evaluate an AST node."""
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in operators:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = eval_expr(node.left)
            right = eval_expr(node.right)
            return operators[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, ast.USub):
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return operators[ast.USub](eval_expr(node.operand))
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        if not isinstance(tree.body, (ast.BinOp, ast.Num, ast.UnaryOp)):
            raise ValueError("Invalid expression: only basic arithmetic operations are supported")

        # Evaluate the expression
        result = eval_expr(tree.body)
        return str(result)
    except Exception as e:
        return f'Error during calculation: {e}'

def web_scraper(url: str) -> str:
    """Scrapes content from a given URL and returns the text."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all text from the webpage
        text = ' '.join(soup.stripped_strings)
        return text
    except requests.exceptions.RequestException as e:
        return f'Error during web scraping: {e}'

def summarize_text(text: str) -> str:
    """Returns a simple summary of the text (simplified version without transformers)."""
    try:
        # Simple summary - just return first 200 characters for demonstration
        return text[:200] + "..." if len(text) > 200 else text
    except Exception as e:
        return f'Error during summarization: {e}'
