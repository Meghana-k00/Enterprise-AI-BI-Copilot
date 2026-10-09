
import sys

from graph.supervisor import app
from evaluation.test_cases import TEST_CASES


def run_evaluation():
    total = len(TEST_CASES)

    if total == 0:
        print("No evaluation test cases found.")
        return 1

    route_passed_count = 0
    keyword_passed_count = 0
    fully_passed_count = 0
    failures = []

    print("\n" + "=" * 70)
    print("ENTERPRISE AI BI COPILOT - EVALUATION")
    print("=" * 70)

    for i, test_case in enumerate(TEST_CASES, start=1):
        question = test_case["question"]
        expected_route = test_case["expected_route"]
        expected_keyword = test_case["expected_keyword"]

        try:
            result = app.invoke({
                "question": question,
                "route": "",
                "answer": "",
                "sources": [],
                "sql_query": "",
                "sql_results": [],
                "messages": [],
            })

            actual_route = result["route"]
            answer = str(result["answer"])

            route_ok = actual_route == expected_route
            normalized_answer = answer.replace(",", "").replace("$", "").casefold()
            normalized_keyword = (
                expected_keyword.replace(",", "").replace("$", "").casefold()
            )

            keyword_ok = normalized_keyword in normalized_answer

            route_passed_count += int(route_ok)
            keyword_passed_count += int(keyword_ok)
            test_passed = route_ok and keyword_ok

            if test_passed:
                fully_passed_count += 1
                status = "PASS"
            else:
                status = "FAIL"
                failures.append({
                    "question": question,
                    "expected_route": expected_route,
                    "actual_route": actual_route,
                    "expected_keyword": expected_keyword,
                    "answer": answer,
                })

            print(f"\nTest {i}: {status}")
            print(f"Question: {question}")
            print(f"Route: expected={expected_route}, actual={actual_route}")
            print(f"Expected keyword: {expected_keyword}")
            print(f"Answer: {answer}")

        except Exception as exc:
            failures.append({
                "question": question,
                "error": str(exc),
            })
            print(f"\nTest {i}: ERROR")
            print(f"Question: {question}")
            print(f"Error: {exc}")

    route_accuracy = route_passed_count / total * 100
    keyword_accuracy = keyword_passed_count / total * 100
    overall_accuracy = fully_passed_count / total * 100

    print("\n" + "=" * 70)
    print(f"Questions evaluated: {total}")
    print(f"Routing accuracy: {route_accuracy:.1f}% "
          f"({route_passed_count}/{total})")
    print(f"Answer keyword pass rate: {keyword_accuracy:.1f}% "
          f"({keyword_passed_count}/{total})")
    print(f"Overall pass rate: {overall_accuracy:.1f}% "
          f"({fully_passed_count}/{total})")
    print(f"Failed cases: {len(failures)}")

    if failures:
        print("\nFAILURE DETAILS")
        for failure in failures:
            print(f"- Question: {failure['question']}")
            if "error" in failure:
                print(f"  Error: {failure['error']}")
            else:
                print(f"  Expected route: {failure['expected_route']}")
                print(f"  Actual route: {failure['actual_route']}")
                print(f"  Expected keyword: {failure['expected_keyword']}")
                print(f"  Actual answer: {failure['answer']}")

    print("=" * 70)

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(run_evaluation())
