
import pytest

from sql.sql_generator import SQLGenerator


@pytest.mark.parametrize(
    ("question", "required_sql_terms"),
    [
        (
            "How much revenue did we generate overall?",
            ["SUM", "SALES_AMOUNT"],
        ),
        (
            "Show total sales revenue by region",
            ["SUM", "SALES_AMOUNT", "GROUP BY", "REGION"],
        ),
    ],
)
def test_sql_generator_handles_paraphrases(question, required_sql_terms):
    generator = SQLGenerator()
    sql_query = generator.generate_sql(question).upper()

    for term in required_sql_terms:
        assert term in sql_query, (
            f"Question: {question!r}; "
            f"expected SQL to contain {term!r}; got: {sql_query}"
        )
