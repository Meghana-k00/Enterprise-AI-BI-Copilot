from graph.router import QueryRouter


router = QueryRouter()


def test_rag_question():
    result = router.route(
        "What is the maximum standard discount allowed?"
    )

    assert result == "RAG"


def test_sql_question():
    result = router.route(
        "What is the total sales revenue by region?"
    )

    assert result == "SQL"


def test_analytics_question():
    result = router.route(
        "What is the forecast for next month's revenue?"
    )

    assert result == "ANALYTICS"