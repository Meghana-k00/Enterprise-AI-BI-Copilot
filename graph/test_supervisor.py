from graph.supervisor import app


questions = [
    "What is the maximum standard discount allowed?",
    "What is the total sales revenue by region?",
    "What is the forecast for next month's revenue?"
]


for question in questions:

    result = app.invoke({
        "question": question,
        "route": "",
        "answer": "",
        "sources": [],
        "sql_query": "",
        "sql_results": []
    })

    print("\nQuestion:")
    print(question)

    print("\nRoute:")
    print(result["route"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result.get("sources", []):
        print("-", source)

    print("=" * 60)