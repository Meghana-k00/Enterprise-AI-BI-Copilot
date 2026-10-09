from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma


class RAGEngine:

    def __init__(self):

        # Local embedding model
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        # Local Chroma vector database
        self.vectorstore = Chroma(
            collection_name="business_policies",
            embedding_function=self.embeddings,
            persist_directory="chroma_db"
        )

        # Local LLM
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0
        )

    def answer(self, question):

        # Retrieve relevant documents
        documents = self.vectorstore.similarity_search(
            question,
            k=2
        )

        # Combine retrieved content
        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        # Prompt the local LLM
        prompt = f"""
You are an enterprise business intelligence assistant.

Answer the user's question using ONLY the provided business policy context.

If the answer is not available in the context, say:
"I could not find this information in the available business policies."

Business Policy Context:
{context}

User Question:
{question}

Give a concise and accurate answer.
"""

        # Generate answer
        response = self.llm.invoke(prompt)

        # Collect sources
        sources = list(
            dict.fromkeys(
                document.metadata["source"]
                for document in documents
            )
        )

        return {
            "answer": response.content,
            "sources": sources
        }
