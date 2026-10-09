from sql.sql_generator import SQLGenerator


def test_sql_generator():
    generator = SQLGenerator()

    question = "What is the total sales revenue by region?"

    sql_query = generator.generate_sql(question)

    assert sql_query is not None
    assert isinstance(sql_query, str)
    assert sql_query.strip() != ""

    assert "SELECT" in sql_query.upper()
    assert "SALES" in sql_query.upper()