from .sql_agent import SQLAgent


agent = SQLAgent()

question = "What is the total sales revenue by region?"

result = agent.run(question)

print("\nBusiness Question:")
print(result["question"])

print("\nGenerated SQL:")
print(result["sql"])

if result["error"]:
    print("\nError:")
    print(result["error"])
else:
    print("\nSQL Results:")
    for row in result["results"]:
        print(row)

    print("\nBusiness Answer:")
    print(result["answer"])