from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(base_url="http://localhost:11434", model="llama3.2")

# Add to vectorDB
vectorstore = InMemoryVectorStore(embedding=embeddings)


def add_document(text, metadata=None):
    """Add a document to the SKLearnVectorStore vector store."""
    try:
        result = vectorstore.add_texts([text], metadatas=[metadata])
        print(f"Added document to vector store: {result}")
    except Exception as e:
        print(f"Error adding document to vector store: {e}")

def add_web_documents(url, metadatas=None):
    """Add documents from a web page to the SKLearnVectorStore vector store."""
    try:
        docs = WebBaseLoader(url).load()
        # docs_list = [item for sublist in docs for item in sublist]
        # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        # chunk_size=1000, chunk_overlap=200
        # )
        # doc_splits = text_splitter.split_documents(docs_list)
        for doc in docs:
            vectorstore.add_documents([doc], metadata=metadatas)
        # result = vectorstore.add_documents(docs)
        # print(f"Added {result} documents from {url}")
        return docs
    except Exception as e:
        print(f"Error adding documents from {url}: {e}")
        return []

# Create retriever
retiver = vectorstore.as_retriever(k=3)


def similarity_search(query):
    """Retrieve documents from the SKLearnVectorStore vector store."""
    try:
        return vectorstore.search(query,search_type="mmr")
    except Exception as e:
        print(f"Error retrieving documents for query '{query}': {e}")
        return []

