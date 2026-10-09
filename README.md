# Enterprise AI Business Intelligence Copilot

An AI-powered business intelligence application that answers natural-language business questions using **Retrieval-Augmented Generation (RAG), Text-to-SQL, and Python-based analytics**.

The project uses LangGraph to orchestrate specialized workflows and FastAPI to expose the application through an API.

## Key Features

- **Intelligent Query Routing:** Routes questions to SQL, RAG, or analytics workflows.
- **Text-to-SQL:** Converts business questions into SQL queries for structured data retrieval.
- **RAG-Based Question Answering:** Retrieves information from business policy documents.
- **Business Analytics:** Calculates sales metrics and summarizes revenue patterns.
- **Revenue Forecasting:** Implements a baseline forecast using historical monthly revenue.
- **Conversational Context:** Supports follow-up questions using conversation history.
- **Evaluation and Testing:** Includes automated tests for routing, SQL, analytics, retrieval, and answer quality.

## Technology Stack

- **Language:** Python
- **AI Orchestration:** LangGraph, LangChain
- **LLM Runtime:** Ollama
- **Database:** Microsoft SQL Server
- **Retrieval:** RAG, vector search, Chroma
- **Analytics:** Pandas, NumPy
- **API:** FastAPI
- **Testing:** Pytest

## Architecture

1. **User Query:** Receives a natural-language business question.
2. **Query Router:** Determines whether the request requires SQL, document retrieval, or analytics.
3. **Specialized Workflow:** Executes the selected SQL, RAG, or analytics component.
4. **Response Generation:** Produces a response based on the retrieved data or computed result.
5. **Evaluation:** Uses automated tests to check routing and component behavior.

## Project Structure

```text
Enterprise-AI-BI-Copilot/
├── analytics/       # Business metrics and forecasting
├── api/             # FastAPI application
├── data/            # Sample business datasets
├── documents/       # Business policy documents
├── evaluation/      # Evaluation cases and tests
├── graph/           # LangGraph workflow and routing
├── rag/              # Retrieval and policy question answering
├── sql/              # SQL generation, validation, and execution
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.11 or a compatible version supported by the dependencies
- Microsoft SQL Server
- Ollama with the configured language model
- Required Python packages

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Meghana-k00/Enterprise-AI-BI-Copilot.git
   cd Enterprise-AI-BI-Copilot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the project dependencies, if a dependency file is provided:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection and Ollama model according to the project configuration. Prepare the database, datasets, and document index as required by the application.

5. Start the API:

   ```bash
   uvicorn api.api:api --reload
   ```

6. Open the interactive API documentation:

   http://127.0.0.1:8000/docs

> Setup note: Confirm the dependency file, database configuration, model name, and data/index preparation steps before treating these instructions as a verified fresh-install procedure.

## Testing

Run the automated test suite from the project root:

```bash
python -m pytest -q
```

The test suite covers routing, SQL components, analytics, retrieval, and evaluation-related behavior. Test results may vary depending on local database, model, and environment configuration.

## Project Scope

This project demonstrates the integration of language models with structured business data, policy-document retrieval, deterministic analytics, workflow orchestration, and automated testing.

**Author:** Meghana Kuppani  
**Repository:** https://github.com/Meghana-k00/Enterprise-AI-BI-Copilot
