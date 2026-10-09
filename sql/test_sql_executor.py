from sql.sql_executor import execute_sql


def test_execute_sql():
    sql_query = """
    SELECT
        region,
        SUM(sales_amount) AS total_revenue
    FROM dbo.Sales
    GROUP BY region
    ORDER BY total_revenue DESC;
    """

    results = execute_sql(sql_query)

    assert results is not None
    assert len(results) > 0

    assert results[0]["region"] == "North"
    assert float(results[0]["total_revenue"]) == 6060.00