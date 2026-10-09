TEST_CASES = [

    {
        "question": "What is the maximum standard discount allowed?",
        "expected_route": "RAG",
        "expected_keyword": "10%"
    },

    {
        "question": "What is the total sales revenue by region?",
        "expected_route": "SQL",
        "expected_keyword": "North"
    },

    {
        "question": "What is the forecast for next month's revenue?",
        "expected_route": "ANALYTICS",
        "expected_keyword": "5,456.67"
    },

    {
        "question": "What is the total sales revenue?",
        "expected_route": "SQL",
        "expected_keyword": "16,370"
    },

    {
        "question": "What is the refund policy?",
        "expected_route": "RAG",
        "expected_keyword": "refund"
    },

    {
        "question": "Which month had the highest revenue?",
        "expected_route": "ANALYTICS",
        "expected_keyword": "March"
    }
]