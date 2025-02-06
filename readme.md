# Gemini Powerhouse: Unleashing Tool-Augmented AI

Welcome to the Gemini Powerhouse, a robust and flexible framework designed to supercharge your applications with the intelligence and versatility of Google's Gemini models. This codebase provides a clean, efficient, and well-documented way to leverage the Gemini API, specifically optimized for tool usage and fine-tuned for the speed and efficiency of Gemini 2 Flash. Think of this as your Swiss Army knife for interacting with Gemini, whether you're building a sophisticated chatbot, automating complex workflows, or exploring the cutting edge of AI research.

## What Problems Does This Solve?

This codebase addresses the common challenges developers face when integrating large language models (LLMs) like Gemini into their projects. Specifically, it tackles:

*   **Complexity of API Interaction:** Interacting directly with the Gemini API can be cumbersome, requiring careful formatting of requests, handling authentication, and dealing with potential errors. This codebase abstracts away these complexities, providing a simple and intuitive interface.
*   **Tool Integration:**  Unlocking the true potential of LLMs requires the ability to integrate them with external tools and APIs. This codebase provides a robust mechanism for defining and utilizing tools, allowing Gemini to access real-world information and perform actions beyond its inherent knowledge.
*   **Optimization for Gemini 2 Flash:** The Gemini 2 Flash model offers a compelling combination of speed and cost-effectiveness. This codebase is pre-configured to leverage the strengths of Gemini 2 Flash, providing sensible defaults and clear instructions for optimal performance.
*   **Error Handling and Reliability:** API calls can be unreliable due to network issues or API availability hiccups. This codebase incorporates robust error handling and retry logic, ensuring that your application can gracefully handle these situations.
*   **Code Organization and Maintainability:** The codebase is structured with a clear class structure, promoting modularity, testability, and reusability. This makes it easy to integrate into existing projects and maintain over time.

## Core Components: Your Toolkit for Gemini Mastery

This project comprises the following key components, each playing a vital role in orchestrating the interaction between your application and the Gemini API:

*   **`GeminiAPIWrapper` Class (gemini_api.py): The Central Command**

    This class is the heart of the project, encapsulating all the logic for interacting with the Gemini API. It handles:

    *   **Authentication:** Securely manages your API key, retrieved from the environment variable `GEMINI_API_KEY`. *Remember to set this before running the code!*
    *   **API Call Construction:** Formats the API requests according to the Gemini API specifications, including prompts, tool definitions, and generation configuration.
    *   **Error Handling:** Implements robust error handling and retry logic to ensure reliable API communication.
    *   **Response Parsing:** Parses the API response, extracting the generated text or tool calls.
    *   **Parameter Tuning:** Provides direct access to key generation parameters like `temperature`, `top_p`, `top_k`, and `max_output_tokens`, allowing you to fine-tune the behavior of the Gemini model.  The sensible defaults are optimized for Gemini 2 Flash, but feel free to experiment! A `temperature` of 0.0 provides the most predictable results for tool use.
    *  **Built for Tool Use:** The class methods are designed to facilitate complex tool interactions with the Gemini API.

*   **`test_gemini_api.py`: Your Testing Ground and Example Showcase**

    This file provides comprehensive test cases that demonstrate how to use the `GeminiAPIWrapper` class in various scenarios, including:

    *   **Basic Prompting:** Sending a simple text prompt to the Gemini API and receiving a generated response.
    *   **Tool Calling:** Defining and utilizing tools to enable Gemini to access external information and perform actions.  A `fake_web_search` function is provided to simulate a web search tool.
    *   **Iterative Re-injection:** Demonstrating the powerful technique of re-injecting the output of a tool back into Gemini, allowing the model to refine its understanding and provide more accurate and context-aware answers. *This is where the magic happens!* This showcases a powerful feedback loop, allowing the model to leverage external knowledge.
    *   **Error Handling:** Validating that the error handling mechanisms are working as expected.

    These test cases serve as both a testing ground for the codebase and a practical example of how to use the `GeminiAPIWrapper` class.

*   **`instructions.txt`: Your Guide to Gemini Enlightenment**

    This file contains detailed instructions and best practices for using the Gemini API effectively, with a particular focus on tool usage and optimization for Gemini 2 Flash.  Consult this file for tips on prompt engineering, tool definition, and troubleshooting.

## Enhanced Agent Capabilities with Smolagents

This project leverages `smolagents`, a powerful framework for building and managing AI agents. Here's how smolagents enhances our Gemini implementation:

### Multi-Step Agent Architecture

The integration uses smolagents' multi-step agent architecture, which enables:

- **Strategic Task Decomposition**: Agents break down complex tasks into manageable subtasks
- **Tool Integration**: Seamless integration with various tools and APIs
- **Memory Management**: Efficient handling of conversation context and previous actions
- **Error Recovery**: Robust error handling and retry mechanisms

### Available Agent Types

1. **CodeAgent**: Writes tool calls in Python code format
   - More flexible and composable than JSON
   - Better object management
   - Leverages existing code patterns in LLM training data

2. **ToolCallingAgent**: Uses JSON-like tool calls
   - Simpler structure for basic tasks
   - Direct integration with API tool calling capabilities

### Tool Management

The project includes a sophisticated tool registry system that:

- Manages available functions and their implementations
- Documents tool purposes and parameters
- Provides error handling and validation
- Enables dynamic tool loading and configuration

### Key Features

- **Asynchronous Operations**: Support for async/await patterns
- **Planning Capabilities**: Periodic planning steps for better task management
- **Telemetry**: Integration with OpenTelemetry for monitoring and debugging
- **Extensibility**: Easy addition of new tools and capabilities

### Example Usage

```python
from smolagents import CodeAgent, HfApiModel
from function_registry import registry

# Initialize the agent
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(
    tools=[registry.get_tool("web_search"), registry.get_tool("calculate")],
    model=model,
    add_base_tools=True
)

# Run a task
result = await agent.run(
    "Research the latest developments in quantum computing and calculate their potential impact"
)
```

## SmolAgent: A Lightweight Tool-Augmented Assistant

The SmolAgent is a lightweight yet powerful implementation that demonstrates the practical application of tool-augmented AI using the Gemini API. It serves as a bridge between natural language requests and concrete actions through its tool integration capabilities.

### Core Features

* **Asynchronous Design:** Built with modern async/await patterns for optimal performance
* **Tool Registry Integration:** Seamlessly connects with the function registry for dynamic tool discovery
* **Safe Calculation Engine:** Implements secure mathematical operations using Python's ast module
* **Web Interaction:** Includes web search, scraping, and content summarization capabilities
* **Natural Language Processing:** Intelligently interprets user requests and selects appropriate tools
* **Error Handling:** Robust error recovery and informative feedback

### Architecture

The SmolAgent comprises several key components:

1. **GeminiAPIWrapper Integration:**
   * Optimized for Gemini 2 Flash
   * Handles API authentication and request formatting
   * Manages response parsing and error handling

2. **Tool Management:**
   * Dynamic tool discovery from function registry
   * Automatic tool description generation
   * Parameter validation and type checking

3. **Request Processing Pipeline:**
   * Natural language understanding
   * Tool selection and execution
   * Result synthesis and formatting

### Example Usage

```python
from smol_agent import SmolAgent
import asyncio

async def main():
    # Initialize the agent
    agent = SmolAgent()
    
    # Process different types of requests
    requests = [
        "Calculate 15 * 24 + 3",  # Mathematical operations
        "Search for the latest AI news",  # Web search
        "Summarize https://example.com",  # Web scraping
    ]
    
    for request in requests:
        response = await agent.process_request(request)
        print(f"Request: {request}\nResponse: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### Extending SmolAgent

The SmolAgent is designed for extensibility. You can add new tools by:

1. Implementing the tool function in `tools.py`
2. Registering it in the function registry
3. The agent will automatically discover and incorporate new tools

This architecture makes it easy to expand the agent's capabilities while maintaining a clean and maintainable codebase.

## Getting Started: From Zero to Gemini Hero

Follow these steps to get up and running with the Gemini Powerhouse:

1.  **Clone the Repository:** Clone this repository to your local machine using `git clone <repository_url>`.
2.  **Install Dependencies:**  Install the necessary Python packages using `pip install -r requirements.txt`. This will install the `requests` library for making API calls and `python-dotenv` for managing environment variables.
3.  **Set Your API Key:** Obtain an API key from Google's Generative AI platform and set it as the environment variable `GEMINI_API_KEY`. You can do this by adding the following line to a `.env` file in the root of the project:

    ```
    GEMINI_API_KEY=YOUR_API_KEY
    ```

    *Remember to replace `YOUR_API_KEY` with your actual API key.*
4.  **Run the Tests:** Run the test suite using `pytest test_gemini_api.py` to ensure that the codebase is working correctly.
5.  **Explore the Examples:**  Examine the test cases in `test_gemini_api.py` to learn how to use the `GeminiAPIWrapper` class in different scenarios.
6.  **Start Building!**  Integrate the `GeminiAPIWrapper` class into your own projects and start building amazing applications powered by the Gemini API.

## Unleashing the Power: Advanced Tool Usage and Beyond

This codebase provides a solid foundation for building tool-augmented AI applications. Here are some ideas for taking your projects to the next level:

*   **Expanding Tool Selection:**  Implement a more sophisticated mechanism for selecting the appropriate tool based on the user's prompt. This could involve using an LLM to analyze the prompt and generate a list of candidate tools.
*   **Dynamic Tool Definition:**  Allow users to define their own tools at runtime, providing greater flexibility and customization.
*   **Integrating with Real-World APIs:**  Replace the `fake_web_search` function with a real web search API or other external API.  The public-apis/public-apis repository is a fantastic resource for discovering publicly available APIs. *Be mindful of API usage costs!*
*   **Building a Chatbot:**  Create a chatbot that can answer questions, perform tasks, and engage in natural conversations using the Gemini API and a variety of tools.
*   **Automating Workflows:**  Automate complex workflows by chaining together multiple tool calls and using the Gemini API to orchestrate the process.

## PhD-Level Musings: Towards Universal API Access

The current implementation uses a placeholder for a real web search API. To expand this to search for *any* API call, consider these key steps:

1.  **Semantic API Discovery:** Automatically identify relevant APIs based on a user's natural language prompt, moving beyond keyword searches to semantic understanding.
    *   **LLM-Powered API Suggestion:**  Fine-tune an LLM on API descriptions to rank candidate APIs based on semantic similarity.
    *   **Knowledge Graph Integration:**  Use knowledge graphs (e.g., Wikidata, DBpedia) to connect user intents with API capabilities.
2.  **Automated Schema Extraction & Transformation:**  Extract and standardize API schemas (OpenAPI, GraphQL, custom formats) for compatibility with the Gemini API's tool parameter. Enrich these schemas with semantic information (data types, value ranges).
3.  **Intelligent Tool Definition Generation:**  Craft clear and concise tool descriptions and parameter mappings from the extracted schemas. Allow for dynamic tool configuration based on context.
4.  **Context-Aware Tool Selection & Invocation:**  Use reinforcement learning to optimize tool selection based on user feedback and task success. Implement a dialogue manager to guide the LLM toward relevant tools in multi-turn conversations.
5.  **Robust Response Handling & Re-injection:**  Validate API responses against expected schemas. Implement error handling with informative messages. Craft prompts that effectively integrate API responses into the LLM's knowledge.

**Production Considerations:**

*   **Security:** Implement robust input validation, output sanitization, and access control.
*   **Scalability & Performance:** Cache API responses, optimize database queries, and distribute workloads.
*   **Monitoring & Logging:** Track API usage, identify bottlenecks, and detect threats.
*   **Cost Optimization:** Implement rate limiting, caching, and select cost-effective API providers.

By tackling these challenges, we can create a truly universal API access system, significantly expanding the Gemini API's capabilities and moving towards more intelligent and versatile AI assistants.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## Next Steps: Resolving Dependency Conflicts with vLLM

We are currently working on integrating vLLM for faster inference. However, we've encountered several dependency conflicts, primarily related to incompatible versions of NumPy and other libraries.

Here's a summary of the steps we've taken:

1.  Attempted to install vLLM directly using `pip install vllm`.
2.  Encountered TensorFlow-related ImportErrors.
3.  Tried explicitly specifying the PyTorch framework.
4.  Attempted to upgrade and downgrade NumPy to resolve version conflicts.

The current approach involves using a Dockerfile to create an isolated environment with the correct versions of all necessary libraries. This should provide a more reliable and reproducible setup for running vLLM.

## Acknowledgements

This project was inspired by the amazing work of the Google AI team and the vibrant community of AI developers. We are grateful for their contributions to the field.

**Now go forth and build amazing things with the Gemini Powerhouse!**
