from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Load policy documents
documents = []

for file_path in Path("documents").glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": file_path.name
            }
        )
    )

print(f"Documents loaded: {len(documents)}")


# 2. Split documents into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")


# 3. Create local embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 4. Create Chroma vector database
vectorstore = Chroma(
    collection_name="business_policies",
    embedding_function=embeddings,
    persist_directory="chroma_db"
)


# 5. Store document chunks in Chroma
vectorstore.add_documents(chunks)

print("RAG knowledge base created successfully!")
print("Vector database: chroma_db")