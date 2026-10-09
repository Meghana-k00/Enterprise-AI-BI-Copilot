from langchain_ollama import ChatOllama


class SQLAnswerGenerator:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0
        )

    def generate_answer(self, question, sql_query, results):

        prompt = f"""
You are an enterprise business intelligence assistant.

Answer the user's business question using ONLY the SQL query and SQL results provided below.

Business Question:
{question}

SQL Query:
{sql_query}

SQL Results:
{results}

Rules:
- Give a concise business-friendly answer.
- Mention important numbers from the results.
- If the results contain categories or regions, compare them when useful.
- Do not invent information.
- Do not mention that you are an AI.
- Do not explain the SQL query unless necessary.

Provide only the final business answer.
"""

        response = self.llm.invoke(prompt)

        return response.content.strip()