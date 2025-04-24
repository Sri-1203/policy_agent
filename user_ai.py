import streamlit as st # type: ignore
from rag_chat import answer_query  # Ensure this module is implemented as per Step 2
import json
import os

import torch # type: ignore
torch.classes.__path__ = []  # Suppress torch.classes warning in Streamlit

ESCALATION_FILE = "escalated_queries.json"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "negative_feedback_count" not in st.session_state:
    st.session_state.negative_feedback_count = 0
if "escalated" not in st.session_state:
    st.session_state.escalated = False
    
def escalate_query(query, response):
    # Load existing escalated queries
    if os.path.exists(ESCALATION_FILE):
        with open(ESCALATION_FILE, "r") as f:
            try:
                escalated_queries = json.load(f)
            except json.JSONDecodeError:
                escalated_queries = []
    else:
        escalated_queries = []

    # Append the new escalated query
    escalated_queries.append({"query": query, "response": response})

    # Save back to the JSON file
    with open(ESCALATION_FILE, "w") as f:
        json.dump(escalated_queries, f, indent=4)

st.title("🛡️ Insurance Policy Chatbot")

user_input = st.chat_input("Enter your question about insurance policies:")
if user_input:
    # Replace this with your actual response generation logic
    response = answer_query(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})
    st.session_state.escalated = False  # Reset on new input


# Display chat history
for i, chat in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["bot"])
        
    if i == len(st.session_state.chat_history) - 1 and not st.session_state.escalated:
        if os.path.exists(ESCALATION_FILE):
            with open(ESCALATION_FILE, "r+") as f:
                try:
                    escalated_queries = json.load(f)
                    json.dump([], f)
                except json.JSONDecodeError:
                    escalated_queries = []
        if escalated_queries:
            for item in escalated_queries:
                if "admin_response" in item:
                    for chat in st.session_state.chat_history:
                        if chat["user"] == item["query"] and chat["bot"] == item["response"]:
                            with st.chat_message("assistant"):
                                st.markdown("👩‍💼 **Admin Response:**")
                                st.markdown(item["admin_response"])
        feedback = st.feedback("thumbs", key=f"feedback_{i}")
        if feedback == 0:  # 👎
            st.session_state.negative_feedback_count += 1
            if st.session_state.negative_feedback_count >= 3:
                escalate_query(chat["user"], chat["bot"])
                st.session_state.escalated = True
                st.session_state.negative_feedback_count = 0
                with st.chat_message("assistant"):
                    st.markdown("[Click here to contact support](http://192.168.29.56:8503)")

                    st.markdown("It seems you're not satisfied with the responses. Redirecting to a human agent...")
    
        elif feedback == 1:  # 👍
            st.session_state.negative_feedback_count = 0

  