import os
import json
import asyncio
import aiohttp
from dotenv import load_dotenv
from gemini_api import GeminiAPIWrapper  # Import the Gemini API wrapper
from function_registry import registry #Import Registry
from smolagent import Agent
from tools import web_search, calculate, web_scraper, summarize_text


load_dotenv()


#Extend the Agent class to call the function registry
class GeminiAgent(Agent):

    def __init__(self, llm):
        super().__init__(llm = llm)

    #Override the default execution to call external APIs if provided
    async def step(self, objective:str) -> str:
        gemini_api = GeminiAPIWrapper()
        action = await gemini_api.call_gemini_api(prompt=f'{objective}\\n what function should I call?  return in JSON format like this:\\n{{\"function_name\": <one of the keys in function registry>, \"params\":{{\"appropriate JSON \"}}}}.\\n if you cannot fulfil objective, function_name = None')
        #Use the function name and the dictionary for call!
        try:
            action_json = json.loads(action)
            function_name = action_json.get('function_name')
            params = action_json.get('params')

            if function_name in registry.functions:
                result = await registry.call_function(function_name, params)
                #If external API is called, add content here, return to Agent step
                return f'function call:{function_name}, with the following result: {result}'
            else:
                print("Action returned None, calling LLM to take action instead of calling external function.")
                #If None is returned, call LLM to take action instead!
                #This adds flexibiltiy
                return super().step(objective)

        except json.JSONDecodeError as e:
            return f'Error when calling tool: {e}'


        return super().step(objective)


async def main():
    # Create an agent that uses Gemini 2.0 as its LLM backend
    gemini_api = GeminiAPIWrapper()
    agent = GeminiAgent(llm = gemini_api.call_gemini_api)
    #The functions are registered!
    # Define a task that the agent will attempt to solve
    task = "I want to travel from New York to Paris with a budget of $3000 for 7 days and with interests on seeing some museums.  Create the itinerary for me and search for travel dates next month. \n    "
    print("\nUsing smolagent to plan a task...")
    try:
        agent_response = await agent.run(task)
        print("Agent response:")
        print(agent_response)
    except Exception as e:
        print(f"An error occurred while running the agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
import os
import json
import asyncio
import aiohttp
from dotenv import load_dotenv
from gemini_api import GeminiAPIWrapper  # Import the Gemini API wrapper
from function_registry import registry #Import Registry
from smolagent import Agent
from tools import web_search, calculate, web_scraper, summarize_text


load_dotenv()


#Extend the Agent class to call the function registry
class GeminiAgent(Agent):

    def __init__(self, llm):
        super().__init__(llm=llm)

    #Override the default execution to call external APIs if provided
    async def step(self, objective: str) -> str:
        gemini_api = GeminiAPIWrapper()
        action = await self.llm(f'{objective}\\n what function should I call?  return in JSON format like this:\\n{{\"function_name\": <one of the keys in function registry>, \"params\":{{\"appropriate JSON \"}}}}.\\n if you cannot fulfil objective, function_name = None')
        # Use the function name and the dictionary for call!
        try:
            action_json = json.loads(action)
            function_name = action_json.get('function_name')
            params = action_json.get('params')

            if function_name in registry.functions:
                result = registry.call_function(function_name, params)
                # If external API is called, add content here, return to Agent step
                return f'function call:{function_name}, with the following result: {result}'
            else:
                print("Action returned None, calling LLM to take action instead of calling external function.")
                # If None is returned, call LLM to take action instead!
                # This adds flexibiltiy
                return super().step(objective)

        except json.JSONDecodeError as e:
            return f'Error when calling tool: {e}'

        return super().step(objective)


async def main():
    # Create an agent that uses Gemini 2.0 as its LLM backend
    gemini_api = GeminiAPIWrapper()
    agent = GeminiAgent(llm = gemini_api.call_gemini_api)
    #The functions are registered!
    # Define a task that the agent will attempt to solve
    task = "I want to travel from New York to Paris with a budget of $3000 for 7 days and with interests on seeing some museums.  Create the itinerary for me and search for travel dates next month. \n    "
    print("\nUsing smolagent to plan a task...")
    try:
        agent_response = await agent.run(task)
        print("Agent response:")
        print(agent_response)
    except Exception as e:
        print(f"An error occurred while running the agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())
