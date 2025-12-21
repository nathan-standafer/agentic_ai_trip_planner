# 🌍 Agentic AI Trip Planner

Welcome to the **Agentic AI Trip Planner**! This project serves as a comprehensive resource for understanding and implementing AI Agents. It demonstrates how to build intelligent agents capable of planning complex trips by leveraging various frameworks, tools, and Large Language Models (LLMs).

Currently, this repository focuses on the **OpenAI Agents SDK**, with plans to expand into other popular frameworks like CrewAI, Langchain, and AutoGen.

---

## 🚀 Project Overview

This project takes you on a journey from building a basic agent to deploying sophisticated setups with local LLMs and custom tools.

### Key Features
- **🤖 OpenAI Agents SDK**: Deep dive into the official SDK for building agents.
- **🛠️ Custom Tools**: Learn how to give your agents abilities like saving files and searching the web.
- **🔌 Model Context Protocol (MCP)**: Implement standardized server protocols for agent-tool communication.
- **🏠 Local LLM Hosting**: Run agents completely locally using **Ollama**.
- **🔍 Web Search Integration**: Empower your local agents with real-time data using **Serper API**.

---

## 📂 Repository Structure

The core content is located in the `openai_agents_sdk/` directory, organized as a step-by-step learning path:

| File | Description |
|------|-------------|
| `1_basic_trip_planner_agent.ipynb` | **Start Here!** Builds a simple agent that plans a trip and saves it to a file. |
| `2_adding_a_custom_tool_to_save_ouput.ipynb` | Teaches how to create custom Python functions that agents can use as tools. |
| `3_use_an_mcp_server_to_save_output.ipynb` | Advanced: Connects the agent to a Model Context Protocol (MCP) server for file operations. |
| `4_refining_the_prompt.ipynb` | Techniques for prompt engineering to get better results from your agents. |
| `5_local_llm_hosting_using_ollama.ipynb` | How to swap OpenAI models for local models (like Llama 3) using **Ollama**. |
| `6_add_serper_api_for_web_search_with_ollama.ipynb` | Adds web search capabilities to your local Ollama agent using the Serper API. |

---

## 🛠️ Setup Guide for Novices

Follow these steps to set up your development environment. We use **`uv`**, a blazing fast Python package manager, to handle dependencies.

### 1. Install `uv`
If you don't have `uv` installed, open your terminal (Command Prompt on Windows) and run:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create a Virtual Environment
Navigate to the project folder in your terminal and create a clean Python environment:

```bash
# Create the environment (using Python 3.12)
uv venv -p 3.12
```

### 3. Activate the Environment
You need to "turn on" the environment to use it.

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

### 4. Install Dependencies
Install the required libraries for the project:

```bash
uv pip install openai-agents python-dotenv
```
*Note: If you are running the notebooks, you might also need Jupyter support:*
```bash
uv pip install ipykernel
```

### 5. Configure API Keys
This project requires API keys to access LLMs and search tools.

1.  Create a file named `.env` in the `openai_agents_sdk/` folder.
2.  Add your keys in the following format:

```ini
# .env file
OPENAI_API_KEY=sk-proj-...
SERPER_API_KEY=...  # Only needed for Notebook 6
```

*   **OpenAI Key**: Get it from [platform.openai.com](https://platform.openai.com/).
*   **Serper Key**: Get it from [serper.dev](https://serper.dev/) (needed for web search with local models).

---

## 🧠 Local LLM Setup (Optional)

If you want to run the agents locally (Notebooks 5 & 6), you will need **Ollama**.

1.  Download and install [Ollama](https://ollama.com/).
2.  Pull the model you want to use (e.g., `llama3` or `gpt-oss`):
    ```bash
    ollama pull llama3
    ```
3.  **Tip:** For complex tasks like trip planning, you might need a larger context window. See `openai_agents_sdk/openai_agents_sdk.md` for instructions on creating a custom model with a 131k context window.

---

## 🔮 Roadmap

I am actively working on expanding this project to include:
- [ ] **CrewAI**: Orchestrating role-playing autonomous agents.
- [ ] **LangChain**: Building context-aware reasoning applications.
- [ ] **AutoGen**: Enabling next-gen multi-agent conversation frameworks.

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).


