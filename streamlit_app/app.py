import streamlit as st
from utils import send_query

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    chat_name = st.text_input("Input a chat name")
    create_chat_button = st.button("New", use_container_width=True, key="create_chat_button")
    if create_chat_button:
        if chat_name:
            st.session_state.messages.append({chat_name: []})
        else:
            st.warning("Input a chat name")
    current_chat = st.radio(
        label="Conversation",
        options=[key for d in st.session_state.messages for key in d.keys()],
        label_visibility="collapsed",
        index=0,
        key="current_chat"
    )

if current_chat:
    prompt = st.chat_input("Say something")
    if prompt:
        for page in st.session_state.messages:
            if current_chat in page:
                page[current_chat].append({"role": "user", "content": prompt})
                
                assistant_response, sources = send_query(prompt)
                
                if assistant_response:
                    sources_text = ""
                    if sources:
                        sources_text = "\n\nSources:\n" + "\n".join([f"- {source}" for source in sources])
                    
                    page[current_chat].append({"role": "assistant", "content": assistant_response + sources_text})
                else:
                    st.error("An error occurred while processing your query.")
    
    for page in st.session_state.messages:
        if current_chat in page:
            for message in page[current_chat]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
else:
    st.warning("Please create a Conversation to start")
