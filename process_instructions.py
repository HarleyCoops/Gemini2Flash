import json
import re
import os

def extract_file_data(snippet: str):
    """
    Extracts the intended file name and code content from a given code snippet.
    Expected format in the snippet:
    
    "Create a file called `filename`: ... ```python
    <code here>
    ```"
    
    Returns a tuple (filename, code_content) if successfully extracted.
    Otherwise, returns (None, None).
    """
    # Look for the file name in the snippet. This regex looks for a phrase like:
    # Create a file called `filename`:
    file_match = re.search(r'Create a file called [`]?([^\n`]+)[`]?[:]', snippet)
    if file_match:
        filename = file_match.group(1).strip()
    else:
        return None, None
    
    # Look for the code block delimited by triple backticks.
    # We assume that the code block starts with ```python or ``` and ends with ``` on a separate line.
    code_block_match = re.search(r'```(?:\w+)?\n(.*?)\n```', snippet, re.DOTALL)
    if code_block_match:
        code_content = code_block_match.group(1)
        return filename, code_content
    return None, None

def process_instructions(instruction_path: str):
    with open(instruction_path, 'r') as f:
        data = json.load(f)
    
    # Navigate to the coding instructions steps.
    steps = data.get("project_outline", {}).get("coding_instructions", {}).get("steps", [])
    
    for step in steps:
        # Each step might include one or more code snippets.
        snippets = step.get("code", [])
        for snippet in snippets:
            filename, code_content = extract_file_data(snippet)
            if filename and code_content:
                # Ensure the directory exists or simply write to the current directory.
                print(f"Writing code to file: {filename}")
                with open(filename, 'w') as fout:
                    fout.write(code_content)
            else:
                # If no file info is found, it might be an instruction for environment setup (like pip commands).
                print("Note: The following snippet does not specify a file creation and may be setup instructions:")
                print(snippet)
                    
if __name__ == "__main__":
    # Adjust the path to match your JSON file name, e.g., "@Instructions.json"
    process_instructions("Instructions.json")
