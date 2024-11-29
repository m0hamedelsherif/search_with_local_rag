from ollama_wrapper import creativeLLm
from langchain_core.messages import HumanMessage , SystemMessage

def simple_generation(state):
    """
    Generate answer using LLM
    """
    print("---SIMPLE GENERATION---")
    loop_step = state.get("loop_step", 0)
    query= state["question"]
    system_prompt = """You are a helpful assistant. Your task is to:
    1- follow the prompt and provide a conversational response to the user query.
    """

    prompt = """Respond conversationally to the following query:\n\n{query}"""

    # LLM generation
    generation = creativeLLm.invoke([SystemMessage(content=system_prompt)]
            + [HumanMessage(content=prompt.format(query=query))])
    return {"generation": generation.content, "loop_step": loop_step + 1}