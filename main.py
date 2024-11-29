import re
import streamlit as st
from vector_store import add_web_documents
from graph.control_flow import graph

def build_context(query):
    documents = []
    links = re.findall(r'(https?://\S+)', query)
    print(f"Links in query: {links}")  # Debug print
    for link in links:
        # push the documents to the list
        added = add_web_documents(link)
        documents.append(added)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Streamlit application layout
st.title("Chat with Llama")

chat_placeholder = st.empty()

# Display chat history
def render_chat():
    with chat_placeholder.container():
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Llama:** {chat['llama']}")
            if "sources" in chat:
                st.markdown("**Sources:**")
                for source in chat["sources"]:
                    st.markdown(f"- [{source['title']}]({source['link']})")
                    if 'description' in source:
                        st.markdown(f"  *{source['description']}*")

# Initial render of chat history
render_chat()

# User input
user_input = st.text_area("Your message:", height=100)

# JavaScript to detect Ctrl+Enter and trigger the button click
st.components.v1.html("""
<script>
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        document.querySelector('button[aria-label="Send"]').click();
    }
});
</script>
""")

def generate_chat_response(build_context, render_chat, user_input):
    build_context(user_input)

    inputs = {
                "question": user_input,
                "max_retries": 1,
            }

            # Placeholder response for loading feedback
    result = {"user": user_input, "llama": "Analyzing your query..."}
    st.session_state["chat_history"].append(result)
    render_chat()  # Update chat to show placeholder
    final_state = graph.invoke(inputs)
    documents = final_state.get('documents', [])
            
            # Prepare sources list
    sources = [{
                'title': doc.metadata['title'],
                'link': doc.metadata['source'],
                'description': doc.metadata['description']
            } for doc in documents]

            # Update final response and sources
    st.session_state["chat_history"].pop()
    result["llama"] = final_state.get("generation", "No response generated.")
    result["sources"] = sources
    st.session_state["chat_history"].append(result)

if st.button("Send"):
    if user_input:
        with st.spinner("Llama is thinking..."):
            generate_chat_response(build_context, render_chat, user_input)
            render_chat()  # Update chat with final result
    else:
        st.warning("Please enter a message.")
