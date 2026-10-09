from typing import TypedDict


class BusinessState(TypedDict, total=False):

    question: str

    route: str

    answer: str

    sources: list[str]

    messages: list[dict]

    sql_query: str

    sql_results: list