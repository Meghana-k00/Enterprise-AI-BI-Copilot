from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Load embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Connect to Chroma
vectorstore = Chroma(
    collection_name="business_policies",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)


# 3. Load local LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# 4. Business question
question = "What is the maximum standard discount allowed?"


# 5. Retrieve relevant policy information
results = vectorstore.similarity_search(
    question,
    k=2
)


# 6. Build context
context = "\n\n".join(
    document.page_content
    for document in results
)


# 7. Create prompt
prompt = f"""
You are a business intelligence assistant.

Answer the user's question using ONLY the provided business policy context.

If the answer is not available in the context, say:
"I could not find this information in the available business policies."

Business Policy Context:
{context}

User Question:
{question}

Give a concise and accurate business answer.
"""


# 8. Generate answer
response = llm.invoke(prompt)


print("\nQuestion:")
print(question)

print("\nAI Answer:")
print(response.content)

print("\nSources:")
for document in results:
    print("-", document.metadata["source"])