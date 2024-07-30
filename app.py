"""
This is a Streamlit user interface to the local RAG that is exposed through fastapi's.
The data available in the RAG today is limited to a couple of sample board game manuals.
The intent is to expand the rag to chain
"""
import os
import requests
from streamlit import streamlit as st

from models.rag_query_model import QueryInput, QueryOutput

CHATBOT_URL = os.getenv(
    "CHATBOT_URL2", "http://localhost:8000/rag-query"
)
print(CHATBOT_URL)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a local LLM that is 
        designed to answer questions about the board games Monopoly and Ticket-to-Ride
        The agent uses  retrieval-augment generation (RAG) embeddings that have been 
        loaded into a local Chroma database.
        """
    )

    st.header("Example Questions")
    st.markdown("- How do I get out of jail in Monopoly?")
    st.markdown(
        """- Can I buy and sell property when I'm in jail?"""
    )
    st.markdown(
        """- What is the objective of the game named Ticket to Ride?"""
    )
    st.markdown(
        """- What are train car cards?"""
    )


st.title("RAG Chatbot")
st.info(
    """Ask me questions about the games Monopoly or Ticket-To_Ride!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    # data = QueryInput(query=prompt).model_dump_json()
    query_input = QueryInput(query=prompt)
    # question = {"query": "How do I get out of jail in Monopoly?"}
    question = query_input.model_dump_json()

    # data = {"input": prompt}
    print(f"API Request Data - {question}")
    data = {"query": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["response"]
            sources = response.json()["sources"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            sources = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(sources)
   # st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": sources,
        }
    )
