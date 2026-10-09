from .sql_generator import SQLGenerator
from .sql_validator import validate_sql
from .sql_executor import execute_sql
from .sql_answer_generator import SQLAnswerGenerator


class SQLAgent:

    def __init__(self):
        self.generator = SQLGenerator()
        self.answer_generator = SQLAnswerGenerator()

    def run(self, question):

        # 1. Generate SQL
        sql_query = self.generator.generate_sql(question)

        # 2. Validate SQL
        valid, message = validate_sql(sql_query)

        if not valid:
            return {
                "question": question,
                "sql": sql_query,
                "results": [],
                "answer": None,
                "error": message
            }

        # 3. Execute SQL
        results = execute_sql(sql_query)

        # 4. Generate business-friendly answer
        answer = self.answer_generator.generate_answer(
            question,
            sql_query,
            results
        )

        return {
            "question": question,
            "sql": sql_query,
            "results": results,
            "answer": answer,
            "error": None
        }