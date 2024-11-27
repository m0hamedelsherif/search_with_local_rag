import re
from flask import Flask, request, jsonify, render_template
from graph.control_flow import graph
from vector_store import add_web_documents

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/research', methods=['POST'])
def research():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    # check if the query contains links and scrape the links context before generating search queries for better context and extract them
    build_context(query)

    # Test on current events
    inputs = {
        "question": query,
        "max_retries": 1,
    }

    final_state = graph.invoke(inputs)

    documents = final_state.get('documents',[])
    print(f"Documents: {documents}")  # Debug print
    # Prepare sources list
    sources = [{
        'title': doc.metadata['title'],
        'link': doc.metadata['source'],
        'description': doc.metadata['description']
    } for doc in documents]
    
    return jsonify({
        'queries': final_state.get('search_queries', []),
        'summary': final_state["generation"],
        'sources': sources
    })

def build_context(query):
    documents = []
    links = re.findall(r'(https?://\S+)', query)
    print(f"Links in query: {links}")  # Debug print
    for link in links:
        # push the documents to the list
        added = add_web_documents(link)
        documents.append(added)
    return documents

if __name__ == '__main__':
    app.run(debug=True)