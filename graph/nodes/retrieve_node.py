from vector_store import similarity_search

def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Write retrieved documents to documents key in state
    try:
        documents = similarity_search(question)
        print("Retrieved documents:", documents)
        return {"documents": documents}
    except Exception as e:
        print(f"Error retrieving documents for question '{question}': {e}")
        return {"documents": []}