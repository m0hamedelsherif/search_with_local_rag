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

chat_placeholder = st.empty()

# Display chat history
def render_chat():
    with chat_placeholder.container():
        for chat in st.session_state["chat_history"]:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Llama:** {chat['llama']}")
            if "sources" in chat and len(chat["sources"]) > 0:
                st.markdown("**Sources:**")
                for source in chat["sources"]:
                    st.markdown(f"- [{source['title']}]({source['link']})")
                    if 'description' in source:
                        st.markdown(f"  *{source['description']}*")

def generate_chat_response(user_input):
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

# Streamlit application layout
st.title("Chat with Llama")

# Initial render of chat history
render_chat()

# User input and button state
user_input = st.text_area("Your message:", height=100, key="input_box")
send_disabled = st.session_state.get("disable_send", False)

# Send button
if st.button("Send", disabled=send_disabled):
    if user_input.strip():
        with st.spinner("Llama is thinking..."):
            # Disable button and clear input
            st.session_state["disable_send"] = True
            # st.session_state["input_box"]
            generate_chat_response(user_input)
            render_chat()

            # Re-enable the button
            st.session_state["disable_send"] = False
    else:
        st.warning("Please enter a message.")
