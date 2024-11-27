from ollama_wrapper import llm
from langchain_core.messages import HumanMessage , SystemMessage

def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")

    system_prompt = """You are generating questions that is well optimized for retrieval.  
            Look at the input and try to reason about the underlying semantic intent / meaning."""

    prompt = """Here is the initial question:
    -------
    {question} 
    -------
    here are the current context:
    -------
    {context}
    -------
    Provide an improved question without any preamble, only respond with the updated question: """

    question = state["question"]
    documents = state["documents"]
    docs_txt = format_docs(documents)
    rag_prompt_formatted = prompt.format(context=docs_txt, question=question)
    question = llm.invoke([SystemMessage(content=system_prompt)]
            + [HumanMessage(content=rag_prompt_formatted)])
    
    print("Transformed Question: ", question)

    return {"question": question.content}

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)