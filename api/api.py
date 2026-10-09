import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any

from graph.supervisor import app


api = FastAPI(
    title="Enterprise AI Business Intelligence Copilot",
    description="GenAI Business Intelligence API using RAG, SQL, Analytics and LangGraph",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    messages: list[dict[str, Any]] = []

@api.get("/")
def home():
    return {
        "message": "Enterprise AI Business Intelligence Copilot API is running"
    }


@api.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        result = app.invoke({
    "question": request.question,
    "route": "",
    "answer": "",
    "sources": [],
    "sql_query": "",
    "sql_results": [],
    "messages": request.messages
})
        return {
    "answer": result["answer"],
    "route": result["route"],
    "sources": result.get("sources", []),
    "sql_query": result.get("sql_query", ""),
    "sql_results": result.get("sql_results", []),
    "messages": result.get("messages", [])
}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Unable to process the request: {str(e)}"
        )