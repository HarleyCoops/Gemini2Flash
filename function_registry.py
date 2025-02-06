from typing import Callable, Dict, Any
from tools import web_search, calculate, web_scraper, summarize_text, deepseek_chat, huggingface_tool  # Import your tool functions here

FunctionType = Callable[[Dict[str, Any]], str]

class FunctionRegistry:
    def __init__(self):
        self.functions: Dict[str, FunctionType] = {}

    def register_function(self, name: str, func: FunctionType, description: str, parameters: Dict[str, str]) -> None:
        self.functions[name] = func
        func.__description__ = description  # type: ignore
        func.__parameters__ = parameters  # type: ignore

    def call_function(self, name: str, args: Dict[str, Any]) -> str:
        if name not in self.functions:
            return f"Error: Function '{name}' not found in the registry."
        try:
            func = self.functions[name]
            # Check if the incoming args match the parameters definition.
            expected_params = getattr(func, '__parameters__', {})
            # check for missing parameters:
            missing_params = set(expected_params.keys()) - set(args.keys())

            if missing_params:
                return f"Error: Missing required parameters: {', '.join(missing_params)} for function {name}"

            # Call the function
            return func(**args)
        except Exception as e:
            return f"Error: An error occurred while calling function '{name}': {e}"

# Create a global function registry instance
registry = FunctionRegistry()

# Register the tool functions (replace examples with real descriptions and parameters)
registry.register_function("web_search", web_search, description="Searches the web for information.", parameters={"query": "The search query"})
registry.register_function("calculate", calculate, description="Calculates a mathematical expression.", parameters={"expression": "The mathematical expression to calculate"})
registry.register_function("web_scraper", web_scraper, description="Scrapes the content of a webpage.", parameters={"url": "The URL of the webpage to scrape"})
registry.register_function("summarize_text", summarize_text, description="Summarizes the given text.", parameters={"text": "The text to be summarized"})
registry.register_function(
    "deepseek_chat",
    deepseek_chat,
    description="Makes a call to the DeepSeek API to get AI-generated responses.",
    parameters={
        "prompt": "The text prompt to send to DeepSeek",
        "model": "The model to use ('deepseek-chat' for V3 or 'deepseek-reasoner' for R1)"
    }
)
registry.register_function(
    "huggingface_tool",
    huggingface_tool,
    description="Runs inference using a Hugging Face model.",
    parameters={
        "prompt": "The prompt to send to the Hugging Face model"
    }
)
