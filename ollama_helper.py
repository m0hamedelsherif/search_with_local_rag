# import requests
import json
from ollama_wrapper import llm , llm_json_mode
    
def generate_search_queries(topic, context=""):
    """Use Ollama to generate multiple relevant search queries for the topic/question"""
    system_prompt = """You are a search query optimization expert. Your task is to:
    1. Analyze the given topic/question
    2. Generate a 2-3 specific search queries that will help gather comprehensive information
    3. Format the output as a JSON array of strings
    4. Order the queries in the order of importance
    Make queries specific and targeted to different aspects of the topic."""
    
    prompt = f"""Generate optimal search queries for the topic/question: "{topic}"
    Consider different angles and aspects of the topic/question.
    Respond with only a JSON with a key `queries` as array of strings containing the search queries."""
    
    if context:
        prompt += f"\n\nContext:\n{context}"
    
    response = llm_json_mode.invoke(prompt, system_prompt=system_prompt)
    print("Search Queries Response: ", response.content)
    result = [topic]
    try:
        result = json.loads(response.content)['queries']
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        result = [response.content]
    return result
    
def create_summary(query, all_content):
    # Create prompt for final summary
    system_prompt = """You are a research synthesis expert. Your task is to:
    1. Analyze the provided source materials
    2. Synthesize the information into a coherent summary
    3. Focus on key findings and insights
    4. Maintain objectivity and accuracy
    5. Highlight any conflicting information or perspectives"""
    
    prompt = f"""Based on the following sources, provide a comprehensive summary of the topic/question: "{query}"

    {all_content}

    Please provide a well-structured summary that synthesizes the key information and insights from all sources."""
    
    # Get summary from Ollama
    response = llm.invoke(prompt, system_prompt=system_prompt)

    return response.content.strip()

def handle_response(response):
    try:
        response = response.strip()
        if response.startswith("```"):
            response = response[response.find("["):response.rfind("]")+1]
        return json.loads(response)
    except:
        return response