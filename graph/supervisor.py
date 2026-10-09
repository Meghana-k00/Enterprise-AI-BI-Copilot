from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

from graph.state import BusinessState
from graph.router import QueryRouter

from sql.sql_agent import SQLAgent
from sql.sql_answer_generator import SQLAnswerGenerator

from rag.rag_engine import RAGEngine

from analytics.analytics_agent import AnalyticsAgent


# =========================================================
# AGENTS
# =========================================================

router = QueryRouter()

sql_agent = SQLAgent()
sql_answer_generator = SQLAnswerGenerator()

rag_agent = RAGEngine()

analytics_agent = AnalyticsAgent()


context_llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# =========================================================
# CONTEXT RESOLUTION
# =========================================================


def resolve_context(question, messages):
    if not messages:
        return question

    q = question.lower().strip()

    follow_up_phrases = {
        "what about it?",
        "what about that?",
        "what about this?",
        "and what about it?",
        "tell me more about it",
        "what about them?",
        "what about those?"
    }
    reference_words = {
        "it", "its", "they", "them", "that", "those",
        "these", "this", "same", "previous", "above", "earlier",
        "second", "third", "fourth", "highest", "lowest",
        "first", "next", "another", "more"
    }


    words = set(q.replace("?", "").replace(".", "").split())

    if q not in follow_up_phrases and not words.intersection(reference_words):
        return question

    # Find the most recent user question from the conversation.
    previous_question = next(
        (
            message["content"]
            for message in reversed(messages)
            if message.get("role") == "user"
            and message.get("content", "").strip()
        ),
        None
    )

    if not previous_question:
        return question

    # For this ambiguous follow-up, retain the previous topic explicitly.
    if q in follow_up_phrases:
        return (
            f"Regarding the previous question: {previous_question} "
            f"Please provide further information."
        )

    recent_messages = messages[-8:]

    conversation = "\n".join(
        f'{message["role"]}: {message["content"]}'
        for message in recent_messages
    )

    prompt = f"""
You resolve follow-up questions for a Business Intelligence application.

Conversation:
{conversation}

Current question:
{question}

Rewrite the current question as one standalone question.
Preserve its intent and the previous topic.
Do not answer the question or invent facts.
Return only the standalone question.
"""

    try:
        response = context_llm.invoke(prompt)
        resolved = response.content.strip()

        if resolved and len(resolved) > 5:
            return resolved
    except Exception:
        pass

    return question



# =========================================================
# ROUTER NODE
# =========================================================

def route_question(state: BusinessState):

    original_question = state["question"].strip()

    messages = state.get("messages", [])

    question = resolve_context(
        original_question,
        messages
    )

    route = router.route(question)

    updated_messages = messages + [
        {
            "role": "user",
            "content": original_question
        }
    ]

    return {
        "question": question,
        "route": route,
        "messages": updated_messages
    }


# =========================================================
# SQL NODE
# =========================================================

def run_sql(state: BusinessState):

    result = sql_agent.run(
        state["question"]
    )

    if result["error"]:

        answer = result["error"]

        return {
            "answer": answer,
            "sources": [],
            "sql_query": result.get("sql"),
            "sql_results": [],
            "messages": state.get("messages", []) + [
                {
                    "role": "assistant",
                    "content": answer
                }
            ]
        }

    answer = sql_answer_generator.generate_answer(
        question=result["question"],
        sql_query=result["sql"],
        results=result["results"]
    )

    return {
        "answer": answer,
        "sources": [
            "SQL Server - EnterpriseBI database"
        ],
        "sql_query": result["sql"],
        "sql_results": result["results"],
        "messages": state.get("messages", []) + [
            {
                "role": "assistant",
                "content": answer
            }
        ]
    }


# =========================================================
# RAG NODE
# =========================================================

def run_rag(state: BusinessState):

    result = rag_agent.answer(
        state["question"]
    )

    answer = result["answer"]

    return {
        "answer": answer,
        "sources": result.get("sources", []),
        "messages": state.get("messages", []) + [
            {
                "role": "assistant",
                "content": answer
            }
        ]
    }


# =========================================================
# ANALYTICS NODE
# =========================================================

def run_analytics(state: BusinessState):

    result = analytics_agent.run(
        state["question"]
    )

    answer = result["answer"]

    return {
        "answer": answer,
        "sources": [
            "Python Analytics Engine - sales.csv"
        ],
        "messages": state.get("messages", []) + [
            {
                "role": "assistant",
                "content": answer
            }
        ]
    }


# =========================================================
# CONDITIONAL ROUTING
# =========================================================

def choose_agent(state: BusinessState):

    route = state["route"]

    if route == "SQL":
        return "sql"

    if route == "RAG":
        return "rag"

    if route == "ANALYTICS":
        return "analytics"

    return END


# =========================================================
# LANGGRAPH
# =========================================================

workflow = StateGraph(BusinessState)

workflow.add_node(
    "router",
    route_question
)

workflow.add_node(
    "sql",
    run_sql
)

workflow.add_node(
    "rag",
    run_rag
)

workflow.add_node(
    "analytics",
    run_analytics
)

workflow.set_entry_point(
    "router"
)

workflow.add_conditional_edges(
    "router",
    choose_agent,
    {
        "sql": "sql",
        "rag": "rag",
        "analytics": "analytics",
        END: END
    }
)

workflow.add_edge(
    "sql",
    END
)

workflow.add_edge(
    "rag",
    END
)

workflow.add_edge(
    "analytics",
    END
)

app = workflow.compile()