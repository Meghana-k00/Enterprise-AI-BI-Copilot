import re


def validate_sql(sql_query):

    sql = sql_query.strip()

    # SQL must not be empty
    if not sql:
        return False, "SQL query is empty."

    # Remove leading SQL comments
    sql_without_comments = re.sub(
        r"^\s*(--.*\n|/\*.*?\*/\s*)*",
        "",
        sql,
        flags=re.DOTALL
    ).strip()

    sql_lower = sql_without_comments.lower()

    # Only SELECT queries are allowed
    if not sql_lower.startswith("select"):
        return False, "Only SELECT queries are allowed."

    # Block multiple SQL statements
    if ";" in sql_without_comments.rstrip(";"):
        return False, "Multiple SQL statements are not allowed."

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "exec",
        "execute",
        "merge",
        "grant",
        "revoke"
    ]

    for keyword in blocked_keywords:

        if re.search(
            rf"\b{keyword}\b",
            sql_lower
        ):
            return False, f"Blocked SQL operation: {keyword}"

    return True, "SQL query is safe."