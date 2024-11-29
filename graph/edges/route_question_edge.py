from ollama_wrapper import llm_json_mode
from langchain_core.messages import HumanMessage, SystemMessage


import json


def route_question(state):
    """
    Route question to simple generation or RAG

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """

    print("---ROUTE QUESTION---")
    route_question = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content=state["question"])]
    )
    print(f"Route Question: {json.loads(route_question.content)}")
    source = json.loads(route_question.content)["datasource"]
    print(f"Source: {source}")
    return source.lower()
    
router_instructions = """You are an expert at routing a user question to a RAG System that will have web search capabilities .

use the simple approach for general prompts that do not require a deep dive into the documents or the web.
Use the RAG especially for current events or for when you doesn't have enough information to generate answer.

Must always Return JSON with single key, datasource, that is 'RAG' or 'Simple' depending on the question. """