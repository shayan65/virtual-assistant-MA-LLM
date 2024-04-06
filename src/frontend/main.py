import streamlit as st
import requests

API_URL = "http://0.0.0.0:8000/agents"

def get_agents():
    try:
        response = requests.get(f"{API_URL}/get-agents")
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch agents: {e}")
    return []

def get_conversations(agent_id: str):
    try:
        response = requests.get(f"{API_URL}/get-conversations", params={"agent_id": agent_id})
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch conversations: {e}")
    return []

def get_messages(conversation_id: str):
    try:
        response = requests.get(f"{API_URL}/get-messages", params={"conversation_id": conversation_id})
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch messages: {e}")
    return []

def send_message(conversation_id, message):
    try:
        payload = {"conversation_id": conversation_id, "message": message}
        response = requests.post(f"{API_URL}/chat-agent", json=payload)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to send message: {e}")
    return {"response": "Error"}

def main():
    st.set_page_config(page_title="🤗💬 AIChat")

    with st.sidebar:
        st.title("Conversational Agent Chat")

        agents = get_agents()
        agent_ids = [agent["id"] for agent in agents]
        selected_agent = st.selectbox("Select an Agent:", agent_ids, index=0)

        conversations = get_conversations(selected_agent)
        conversation_ids = [conversation["id"] for conversation in conversations]
        selected_conversation = st.selectbox("Select a Conversation:", conversation_ids, index=0)

    if selected_conversation:
        st.title("Chat")
        st.write("This is a chat interface for the selected agent and conversation. You can send messages to the agent and see its responses.")

        messages = get_messages(selected_conversation)
        
        if messages:
            for message in messages:
                with st.chat_message("user"):
                    st.write(message["user_message"])
                with st.chat_message("assistant"):
                    st.write(message["agent_message"])

        # User-provided prompt
        prompt = st.text_input("Send a message:", key="prompt")
        if st.button("Send", key="send"):
            response = send_message(selected_conversation, prompt)
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                st.write(response["response"])
    else:
        st.write("Please select a conversation from the dropdown.")

if __name__ == "__main__":
    main()
