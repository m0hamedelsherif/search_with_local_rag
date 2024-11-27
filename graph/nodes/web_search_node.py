# from web_search import web_search_tool
# from langchain.schema import Document
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from vector_store import add_web_documents, similarity_search
from duck_research import duck_search_and_scrape
from ollama_helper import generate_search_queries

web_search_tool = DuckDuckGoSearchRun(k=3)

def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")

    question = state["question"]

    documents = state.get('documents',[])

    queries = generate_search_queries(question,format_docs(documents))
    print("Search queries:", queries)
    search_results = duck_search_and_scrape(queries[:2],2)

    for result in search_results:
        metaData = {"title":result.get('title'),"content":result.get('content'),"link": result.get('link'), "query": result.get('query')}
        print("Web search results:", metaData)
        add_web_documents(result.get('link'),metaData)

    search_queries = []
    for query in queries:
        search_queries.append(query)
    
    return {"documents": documents , "search_queries": search_queries}

# Post-processing
def format_docs(docs):
    """Format documents for Ollama input
        Remove
    Args:
        docs (list): List of Document objects
    """
    return "\n\n".join(doc.page_content for doc in docs)