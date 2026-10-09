import pytest

from graph.supervisor import app
from evaluation.test_cases import TEST_CASES


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
    ids=[case["question"] for case in TEST_CASES]
)
def test_business_question_evaluation(case):
    result = app.invoke({
        "question": case["question"],
        "route": "",
        "answer": "",
        "sources": [],
        "sql_query": "",
        "sql_results": [],
        "messages": []
    })

    assert result["route"] == case["expected_route"], (
        f"Route mismatch for: {case['question']}"
    )

    actual_answer = str(result["answer"]).replace(",", "")
    expected_keyword = case["expected_keyword"].replace(",", "")

    assert expected_keyword.lower() in actual_answer.lower(), (
        f"Expected '{case['expected_keyword']}' "
        f"in answer, but got: {result['answer']}"
    )