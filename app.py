import streamlit as st
from chatbot.assistant import HiringAssistant
import time
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_assistant():
    """Cache the assistant instance to prevent reinitialization"""
    logger.info("Initializing HiringAssistant")
    return HiringAssistant()

@st.cache_data(ttl=3600)
def get_initial_message():
    """Cache the initial message"""
    return get_assistant().start_conversation()

def initialize_session_state():
    """Initialize session state variables"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = get_assistant()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'initial_message_shown' not in st.session_state:
        st.session_state.initial_message_shown = False

@st.cache_data(ttl=60)
def format_message(message: Dict[str, Any]) -> str:
    """Format a message for display with caching"""
    return message["content"]

def display_chat():
    """Display chat messages with optimized rendering"""
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(format_message(message), unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Sidebar for additional controls
    with st.sidebar:
        st.title("Controls")
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.initial_message_shown = False
            st.rerun()
    
    # Main chat interface
    st.title("🤖 Hiring Assistant")
    
    # Display initial message if not shown
    if not st.session_state.initial_message_shown:
        initial_message = get_initial_message()
        st.session_state.chat_history.append({"role": "assistant", "content": initial_message})
        st.session_state.initial_message_shown = True
    
    # Display chat history
    display_chat()
    
    # User input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Get assistant response
        with st.spinner("Thinking..."):
            response = st.session_state.assistant.process_input(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to update the display
        st.rerun()

if __name__ == "__main__":
    main()