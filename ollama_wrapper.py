from langchain_ollama import ChatOllama

local_llm = "llama3.2"
creativeLLm = ChatOllama(base_url="http://localhost:11434",model=local_llm)
llm = ChatOllama(base_url="http://localhost:11434",model=local_llm,temperature=0)
llm_json_mode = ChatOllama(base_url="http://localhost:11434",model=local_llm, temperature=0, format="json")