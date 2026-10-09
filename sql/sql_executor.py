from .sql_connection import get_connection


def execute_sql(sql_query):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(sql_query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    results = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    connection.close()

    return results