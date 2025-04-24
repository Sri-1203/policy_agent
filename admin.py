import streamlit as st # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
import json
import os

ESCALATION_FILE = "escalated_queries.json"
# with open(ESCALATION_FILE, "w") as f:
#     json.dump([], f)
st_autorefresh(interval=5000, key="auto-refresh")

st.title("🛠️ Admin Descalation Dashboard")

# Load escalated queries
if os.path.exists(ESCALATION_FILE):
    with open(ESCALATION_FILE, "r") as f:
        try:
            escalated_queries = json.load(f)
        except json.JSONDecodeError:
            escalated_queries = []
else:
    escalated_queries = []

if not escalated_queries:
    st.info("No escalated queries at the moment.")
else:
    for idx, item in enumerate(escalated_queries):
        st.subheader(f"Escalated Query {idx + 1}")
        st.markdown(f"**User Query:** {item['query']}")
        st.markdown(f"**Chatbot Response:** {item['response']}")
        admin_response = st.text_area(f"Admin Response for Query {idx + 1}", key=f"response_{idx}")
        if st.button(f"Submit Response for Query {idx + 1}", key=f"submit_{idx}"):
            # Implement logic to handle the admin response
            escalated_queries[idx]["admin_response"] = admin_response  # Save response
            # Optionally, remove the handled query from the list
            #escalated_queries.pop(idx)
            with open(ESCALATION_FILE, "w") as f:
                json.dump(escalated_queries, f, indent=4)
            st.success(f"Response for Query {idx + 1} submitted.")
            st.rerun()
