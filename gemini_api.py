import os
import json
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class GeminiAPIWrapper:
    """
    A wrapper for interacting with the Gemini API. Handles authentication,
    API calls, and basic error handling.  Designed for enhanced tool use and efficiency.

    Optimized for Gemini 2 Flash through parameter defaults and specific prompt engineering guidance.
    """

    def __init__(self, api_key=None, model_name="gemini-2.0-flash", max_retries=3):
        """
        Initializes the GeminiAPIWrapper.

        Args:
            api_key (str, optional): The API key for the Gemini API. Defaults to the
                                       'GEMINI_API_KEY' environment variable.
            model_name (str, optional): The name of the Gemini model to use. Defaults to "gemini-2.0-flash".
            max_retries (int, optional): Maximum number of retries for API calls. Defaults to 3.

        Raises:
            ValueError: If API key is not provided and 'GEMINI_API_KEY'
                        environment variable is not set.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided. Set GEMINI_API_KEY environment variable.")
        self.model_name = model_name
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        self.max_retries = max_retries

    async def _make_api_request(self, payload):
        """
        Makes the API request with retry logic using aiohttp for asynchronous calls.
        Private method.

        Args:
            payload (dict): The payload to send to the API.

        Returns:
            dict: The JSON response from the API, or None if the request fails after retries.
        """
        headers = {'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.api_url, json=payload, timeout=20, headers=headers) as response:
                        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                        return await response.json()
            except aiohttp.ClientError as e:
                print(f"API request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt == self.max_retries - 1:
                    print(f"API request failed after {self.max_retries} retries.")
                    return None  # Handle retry logic

    async def call_gemini_api(self, prompt, tools=None, temperature=0.0, top_p=1.0, top_k=1, max_output_tokens=200): #tuned for flash. Added tuning parameters

        """
        Calls the Gemini API.

        Args:
            prompt (str): The prompt to send to the API.
            tools (list, optional): A list of tools to use.  Each tool should be a dictionary
                                      following the Gemini API's tool format. Defaults to None.
            temperature (float, optional):  Controls randomness: Lowering results in more predictable responses.
                                            Use a value of 0.0 or close to 0 for predictable output from tool use.
            top_p (float, optional):  Nucleus sampling.  The model considers the results of the tokens with top_p
                                       probability mass. Defaults to 1.0
            top_k (int, optional): Top-k sampling: Consider only the k most likely next tokens. Defaults to 1.
            max_output_tokens (int, optional): The maximum number of tokens to generate. Defaults to 200.
                                            Set appropriately depending on typical length of tool-based responses.
        Returns:
            str: The response from the Gemini API, or None if an error occurs.  Returns the
                 `candidates[0].content.parts[0].text` if the API call is successful, and
                 `None` otherwise.   Also handles parsing tool calls, if present in the API response.
        """
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "topP": top_p,
                "topK": top_k,
                "maxOutputTokens": max_output_tokens
            }
        }

        if tools:
            payload["tools"] = tools
        api_response = await self._make_api_request(payload)
        if not api_response:
            return None  # Indicate failure clearly

        try:
            # Extract text content, properly handling potentially empty results. Check for tool calls.
            candidates = api_response.get("candidates")

            if candidates and len(candidates) > 0:
                 first_candidate = candidates[0]
                 content = first_candidate.get("content")

                 if content and content.get("parts"):
                     first_part = content["parts"][0]  # Assuming a single part

                     #Check for tool calls and return that if that is what's in content['parts']
                     if first_part.get('functionCall'):
                         return first_part  #Return the full function call dict
                     else:
                         return first_part.get("text", "")  # Or empty string if 'text' missing

            return None  # No candidate with content, parts, or text.  This should rarely happen, but guard.
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error parsing API response: {e}")
            print(f"API Response (for debugging): {api_response}")
            return None
