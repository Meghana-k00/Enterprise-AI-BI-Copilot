from sql.sql_validator import validate_sql


def test_sql_validator():
    valid_query = """
    SELECT
        region,
        SUM(sales_amount) AS total_revenue
    FROM dbo.Sales
    GROUP BY region;
    """

    result = validate_sql(valid_query)

    assert result is not None