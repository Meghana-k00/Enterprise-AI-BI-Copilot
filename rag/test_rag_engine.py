from rag_engine import RAGEngine


rag = RAGEngine()

question = "What is the maximum standard discount allowed?"

result = rag.answer(question)

print("\nQuestion:")
print(question)

print("\nAI Answer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print("-", source)