from langgraph.graph import StateGraph
from .graph_state import GraphState
from .nodes.retrieve_node import retrieve
from .nodes.web_search_node  import web_search
from .nodes.grade_documents_node import grade_documents
from .nodes.generate_node import generate
from .edges.decide_to_generate_edge import decide_to_generate
from .edges.grade_generation_v_documents_and_question_edge import grade_generation_v_documents_and_question
from langgraph.graph import END

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("retrieve", retrieve) # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generate

# Build graph
# workflow.set_conditional_entry_point( 
#     route_question,
#     {
#         "websearch": "websearch",
#         "vectorstore": "retrieve",
#     },
# )
# workflow.set_entry_point("retrieve")
workflow.set_entry_point("websearch")
workflow.add_edge("websearch", "retrieve")
workflow.add_edge("retrieve", "grade_documents")
# workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
        "max retries": END,
    },
)

# Compile
print("Compiling graph", workflow)
graph = workflow.compile()