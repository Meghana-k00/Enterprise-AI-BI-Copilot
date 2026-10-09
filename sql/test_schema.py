from sql.schema import get_database_schema


def test_get_database_schema():
    result = get_database_schema()

    assert result is not None
    assert isinstance(result, str)
    assert "DATABASE: EnterpriseBI" in result
    assert "TABLE: Customers" in result
    assert "TABLE: Products" in result
    assert "TABLE: Sales" in result
    assert "RELATIONSHIPS:" in result