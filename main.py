import re
import streamlit as st
from vector_store import add_web_documents
from graph.control_flow import graph
import pprint

def build_context(query):
    documents = []
    links = re.findall(r'(https?://\S+)', query)
    print(f"Links in query: {links}")  # Debug print
    for link in links:
        # push the documents to the list
        added = add_web_documents(link)
        documents.append(added)

# Streamlit application layout
st.title("Chat with Llama")
st.write("Enter your message below:")

# User input
user_input = st.text_input("Your message:")

if st.button("Send"):
    if user_input:
        # Get response from the model
        build_context(user_input)

        # Test on current events
        inputs = {
            "question": user_input,
            "max_retries": 1,
        }
        for event in graph.stream(inputs):
            print(event)
            for key, value in event.items():
            # Create  expandable UI block with the node name
                with st.expander(f"Node '{key}':"):
                    # detailed information of nodes in expander
                    st.text(pprint.pformat(value, indent=2, width=80, depth=None))

        final_generation = value.get('generation', 'No final generation produced.')
        st.subheader("Final Generation:")
        st.write(final_generation)

    else:
        st.write("Please enter a message.")


