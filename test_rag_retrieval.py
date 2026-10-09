from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Load the same embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 2. Connect to the existing Chroma database
vectorstore = Chroma(
    collection_name="business_policies",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)


# 3. Ask a business question
question = "What is the maximum standard discount allowed?"


# 4. Retrieve the most relevant documents
results = vectorstore.similarity_search(
    question,
    k=2
)


# 5. Display retrieved information
print("\nQuestion:")
print(question)

print("\nRetrieved Documents:\n")

for i, document in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(f"Source: {document.metadata['source']}")
    print(document.page_content)
    print()