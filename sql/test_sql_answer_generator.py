from sql.sql_answer_generator import SQLAnswerGenerator


def test_sql_answer_generator():
    generator = SQLAnswerGenerator()

    question = "What is the total sales revenue by region?"

    sql_query = """
    SELECT
        region,
        SUM(sales_amount) AS total_revenue
    FROM dbo.Sales
    GROUP BY region
    ORDER BY total_revenue DESC;
    """

    results = [
        {"region": "East", "total_revenue": 3160.00},
        {"region": "North", "total_revenue": 6060.00},
        {"region": "South", "total_revenue": 3800.00},
        {"region": "West", "total_revenue": 3350.00}
    ]

    answer = generator.generate_answer(
        question,
        sql_query,
        results
    )

    assert answer is not None
    assert isinstance(answer, str)
    assert answer.strip() != ""

    assert "North" in answer
    assert "6,060.00" in answer