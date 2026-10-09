from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector = embeddings.embed_query(
    "What is the company discount policy?"
)

print("Embedding created successfully!")
print("Embedding dimensions:", len(vector))
print("First 5 values:", vector[:5])