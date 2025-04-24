import streamlit as st  # type: ignore
import json
import os

ESCALATION_FILE = "escalated_queries.json"

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to escalate a user query
def escalate_query(query):
    # Load existing queries
    if os.path.exists(ESCALATION_FILE):
        with open(ESCALATION_FILE, "r") as f:
            try:
                escalated_queries = json.load(f)
            except json.JSONDecodeError:
                escalated_queries = []
    else:
        escalated_queries = []

    # Only add if not already added
    if not any(q["query"] == query for q in escalated_queries):
        escalated_queries.append({"query": query, "response": ""})

        with open(ESCALATION_FILE, "w") as f:
            json.dump(escalated_queries, f, indent=4)

# UI title
st.title("🛡️ Insurance Policy Agent")

# User input
user_input = st.chat_input("Enter your question about insurance policies:")
if user_input:
    escalate_query(user_input)
    st.session_state.chat_history.append({"user": user_input, "agent": ""})

# Load escalated queries to match admin responses
if os.path.exists(ESCALATION_FILE):
    with open(ESCALATION_FILE, "r") as f:
        try:
            escalated_queries = json.load(f)
        except json.JSONDecodeError:
            escalated_queries = []
else:
    escalated_queries = []

# Display chat messages
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])

    # Find matching admin response
    for item in escalated_queries:
        if chat["user"] == item["query"] and "admin_response" in item:
            chat["agent"] = item["admin_response"]

    if chat["agent"]:
        with st.chat_message("assistant"):
            st.markdown(chat["agent"])
