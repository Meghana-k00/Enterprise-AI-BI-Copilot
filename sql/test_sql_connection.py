from sql.sql_connection import get_connection


def test_sql_server_connection():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")
        database_name = cursor.fetchone()[0]

        assert database_name == "EnterpriseBI"

        cursor.close()

    finally:
        connection.close()