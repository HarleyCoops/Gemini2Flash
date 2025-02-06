import asyncio
from typing import List, Dict, Any, Optional
from gemini_api import GeminiAPIWrapper
from function_registry import registry

class SmolAgent:
    """
    A lightweight agent that connects Gemini's intelligence with tool execution capabilities.
    Optimized for Gemini 2 Flash and designed for efficient tool use.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent with a Gemini API wrapper and access to registered tools.
        
        Args:
            api_key: Optional API key for Gemini. If not provided, will use environment variable.
        """
        self.gemini = GeminiAPIWrapper(api_key=api_key)
        self.available_tools = self._get_tool_descriptions()

    def _get_tool_descriptions(self) -> List[Dict[str, Any]]:
        """
        Generate tool descriptions in Gemini's expected format from the function registry.
        """
        tools = []
        for name, func in registry.functions.items():
            tool = {
                "functionDeclarations": [{
                    "name": name,
                    "description": getattr(func, '__description__', ''),
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            param_name: {
                                "type": "STRING",
                                "description": param_desc
                            }
                            for param_name, param_desc in getattr(func, '__parameters__', {}).items()
                        },
                        "required": list(getattr(func, '__parameters__', {}).keys())
                    }
                }]
            }
            tools.append(tool)
        return tools

    async def process_request(self, user_request: str) -> str:
        """
        Process a user request through the following steps:
        1. Send request to Gemini with available tools
        2. If Gemini suggests a tool, execute it
        3. Send tool results back to Gemini for final response
        
        Args:
            user_request: The user's natural language request
            
        Returns:
            Final response incorporating tool results if applicable
        """
        # First Gemini call to understand request and potentially select a tool
        result = await self.gemini.call_gemini_api(
            prompt=f"User Request: {user_request}\nPlease help fulfill this request using available tools if needed.",
            tools=self.available_tools,
            temperature=0.0  # Use 0.0 for more predictable tool selection
        )

        if not result:
            return "I apologize, but I was unable to process your request."

        # Check if Gemini wants to use a tool
        if isinstance(result, dict) and result.get('functionCall'):
            function_call = result['functionCall']
            tool_name = function_call['name']
            tool_args = function_call.get('args', {})

            # Execute the tool
            tool_result = registry.call_function(tool_name, tool_args)

            # Send results back to Gemini for final response
            final_prompt = (
                f"Tool '{tool_name}' returned the following result: {tool_result}\n"
                f"Based on the original request: {user_request}\n"
                "Please provide a final response incorporating this information."
            )
            
            final_result = await self.gemini.call_gemini_api(
                prompt=final_prompt,
                temperature=0.0
            )
            
            return final_result if final_result else "I apologize, but I was unable to process the tool results."
        
        # If no tool was needed, return Gemini's direct response
        return result if isinstance(result, str) else "I apologize, but I was unable to generate a response."

async def main():
    """Example usage of the SmolAgent"""
    agent = SmolAgent()
    
    # Example requests that demonstrate different tool usage scenarios
    requests = [
        "Use DeepSeek to create a short joke. Think about what makes a good joke - setup, punchline, and wordplay - then create one.",  # Test DeepSeek-V3 with creative reasoning
        "Use DeepSeek Reasoner to solve this puzzle step by step: If today is Monday, what day was it two days ago? Show your calendar reasoning.",  # Test DeepSeek-R1 with explicit reasoning steps
    ]
    
    for request in requests:
        print(f"\nProcessing request: {request}")
        response = await agent.process_request(request)
        print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
