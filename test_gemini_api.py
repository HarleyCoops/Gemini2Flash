import os
import json
import requests
from dotenv import load_dotenv
from gemini_api import GeminiAPIWrapper

load_dotenv()  # Load environment variables from .env file

def test_gemini_api_wrapper():
    """
    Tests the GeminiAPIWrapper class.  Demonstrates different use cases including tools.
    """

    gemini_api = GeminiAPIWrapper()  # Uses API key from environment

    # Test case 1: Basic prompt
    prompt = "What is the capital of France?"
    result = gemini_api.call_gemini_api(prompt=prompt)
    print(f"Test 1 Result: {result}")

    # Test case 2: With different prompt & model. Note API is initalized to gemini-2.0-flash;  no change is needed to the object to test flash
    prompt = "What is the meaning of life?"
    result = gemini_api.call_gemini_api(prompt=prompt) #already using flash due to initialization
    print(f"Test 2 Result: {result}")


    # Test case 3: With tools - web search
    prompt = "Search for the current weather in London, and then summarise into one short sentence for me, including Celcius, use very minimal wordage please"
    tools = [
        {
            "functionDeclarations": [
                {
                    "name": "web_search",
                    "description": "Searches the web for information.  Use this to provide users up-to-date information on the internet.",
                    "parameters": {
                      "type": "OBJECT",
                      "properties": {
                         "query":{
                           "type": "STRING",
                            "description": "The query to search for."
                         }
                      },
                      "required": ["query"]
                    }
                }
            ]
        }
    ]


    # Example of crafting the structured payload correctly (critical for tool use):
    # Properly format the prompt as a turn in a conversation

    result = gemini_api.call_gemini_api(prompt=prompt, tools=tools)
    print(f"Test 3 Result (Tool Use, Web Search): {result}")

    #If tool call was successful (is not none), take tool and put that output back into gemini
    if result and result.get("functionCall"):
       tool_call_id = result["functionCall"]["name"] # 'web_search', since that's all that's configured

       tool_args=result["functionCall"].get("args")

       if tool_args is None or not isinstance(tool_args, dict):
            print("tool args not found")
            return
       tool_query = tool_args.get("query") #Correct arg key
       if tool_query is None:
            print("Query not found within the function call args. Returning")
            return


       # Fake Web Search implementation for testing -- REPLACE THIS WITH ACTUAL TOOL
       def fake_web_search(query):
            print("Executing (fake) web search for query:", query)
            if "weather" in query.lower() and "london" in query.lower():
                return "The current weather in London is 15 degrees Celsius and sunny."
            else:
                return "No relevant information found."

       web_search_results = fake_web_search(tool_query)  #Use web_search_query

       # Package the results back for Gemini
       tool_response = {
            "tool_name": tool_call_id,  # Must match tool "name" above
            "response": web_search_results,  # Response data from tool.
        }

       # Submit tool's resposne BACK into Gemini -- NEW prompt based on search outcome
       # Reframe based on the output from web_search! This can sometimes improve the output from the re-invocation with Flash

       second_prompt = f"Web Search found this about {tool_query}: {web_search_results}.  The user's original question was: {prompt}. Please use the information and their original question to answer"

       #This final API Call returns the FULL answer, using knowledge and framing we provided.   NO tools included (they were ALREADY USED)

       final_result = gemini_api.call_gemini_api(prompt=second_prompt, tools=None)

       print(f"Final result of Re-invocation for synthesis and framing by model: {final_result}")

    else:
       print("No function call detected, skipping the response and secondary invokation.")

if __name__ == "__main__":
    test_gemini_api_wrapper()
