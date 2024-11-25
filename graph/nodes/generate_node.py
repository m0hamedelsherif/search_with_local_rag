from ollama_wrapper import llm
from langchain_core.messages import HumanMessage , SystemMessage

def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    loop_step = state.get("loop_step", 0)

    # RAG generation
    docs_txt = format_docs(documents)
    rag_prompt_formatted = prompt.format(context=docs_txt, question=question)
    generation = llm.invoke([SystemMessage(content=system_prompt)]
            + [HumanMessage(content=rag_prompt_formatted)])
    return {"generation": generation, "loop_step": loop_step + 1}

### Generate

system_prompt = """You are a research synthesis expert. Your task is to:
1. Analyze the provided source materials
2. Synthesize the information into a coherent Answer/Summary
3. Focus on key findings and insights
4. Maintain objectivity and accuracy
5. Highlight any conflicting information or perspectives"""

prompt = """Based on the following sources, provide a comprehensive Answer/Summary of the topic: {question} 

{context}

Please provide a well-structured Answer/Summary that synthesizes the key information and insights from all sources."""

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)