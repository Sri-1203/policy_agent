# flask_server.py
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to store the conversations JSON file
CONVERSATION_FILE = "conversations.json"

# Ensure the JSON file exists and has the proper structure
def initialize_conversation_file():
    if not os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, 'w') as f:
            json.dump({"conversations": []}, f)

# Function to read conversations from the JSON file
def read_conversations():
    with open(CONVERSATION_FILE, 'r') as f:
        data = json.load(f)
    return data

# Function to write conversations to the JSON file
def write_conversations(data):
    with open(CONVERSATION_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/user_query', methods=['POST'])
def user_query():
    user_input = request.json.get('msg')
    
    if user_input:
        # Read the current conversations
        conversations = read_conversations()
        
        # Create a new conversation ID
        conversation_id = len(conversations['conversations']) + 1
        
        # Add the user's message to the conversation
        conversations['conversations'].append({
            "id": conversation_id,
            "messages": [
                {"sender": "User", "msg": user_input}
            ]
        })
        
        # Save the updated conversations
        write_conversations(conversations)
        
        return jsonify({"status": "success", "message": "User query added!"}), 200
    else:
        return jsonify({"status": "error", "message": "No query provided."}), 400

@app.route('/agent_response', methods=['POST'])
def agent_response():
    conversation_id = request.json.get('conversation_id')
    agent_msg = request.json.get('msg')
    
    if conversation_id and agent_msg:
        # Read the current conversations
        conversations = read_conversations()
        
        # Find the conversation by ID
        conversation = next((c for c in conversations['conversations'] if c['id'] == conversation_id), None)
        
        if conversation:
            # Add the agent's response
            conversation['messages'].append({"sender": "Agent", "msg": agent_msg})
            
            # Save the updated conversations
            write_conversations(conversations)
            
            return jsonify({"status": "success", "message": "Agent response added!"}), 200
        else:
            return jsonify({"status": "error", "message": "Conversation ID not found."}), 404
    else:
        return jsonify({"status": "error", "message": "Invalid data."}), 400

@app.route('/get_conversations', methods=['GET'])
def get_conversations():
    # Read and return the conversations
    conversations = read_conversations()
    return jsonify(conversations), 200

if __name__ == '__main__':
    initialize_conversation_file()
    app.run(debug=True)
