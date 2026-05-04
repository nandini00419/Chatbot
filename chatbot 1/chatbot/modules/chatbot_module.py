"""
Chatbot Module - Groq API Integration
======================================
This module handles conversation with the AI chatbot using Groq API.
It maintains conversation context for multi-turn dialogues.

Features:
- Multi-turn conversation handling
- Context memory across exchanges
- Groq API integration for fast inference
"""

from groq import Groq
import os

# Initialize Groq client with API key
# The API key is stored as an environment variable or can be set directly
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not found in environment variables.")
client = Groq(api_key=GROQ_API_KEY)

# Model to use - you can change this to other Groq models like "llama-3.1-70b-versatile"
MODEL_NAME = "llama-3.1-8b-instant"  # Fast and efficient model

# Conversation history storage
# Format: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
conversation_history = []

# System prompt to guide the chatbot's behavior
SYSTEM_PROMPT = """You are NEXUS-7, a friendly and helpful AI assistant. 
Keep your responses concise, conversational, and to the point (typically 2-4 sentences).
Avoid lengthy documentation-style explanations unless specifically requested.
Be helpful, engaging, and maintain a natural conversation flow."""


def get_chat_response(user_input, reset_context=False):
    """
    Get chatbot response using Groq API with multi-turn conversation support.
    
    Args:
        user_input (str): The user's text input
        reset_context (bool): If True, clears conversation history and starts fresh
    
    Returns:
        str: The chatbot's response text
    
    Example:
        >>> response = get_chat_response("Hello, how are you?")
        >>> print(response)
        "Hello! I'm doing well, thank you for asking..."
    """
    global conversation_history
    
    # Reset conversation history if requested
    if reset_context:
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        return "Conversation context has been reset. How can I help you?"
    
    # Initialize conversation history with system prompt if empty
    if not conversation_history:
        conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add user message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    try:
        # Create chat completion request with full conversation history
        # This allows the model to maintain context across multiple turns
        chat_completion = client.chat.completions.create(
            messages=conversation_history,  # Pass entire conversation history
            model=MODEL_NAME,
            temperature=0.7,  
            max_tokens=300,   
            top_p=0.9,        
        )
        
        # Extract the assistant's response
        assistant_response = chat_completion.choices[0].message.content
        
        # Add assistant response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # Limit conversation history to prevent token limit issues
        # Keep system prompt + last 10 exchanges (1 system + 20 messages: 10 user + 10 assistant = 21 total)
        if len(conversation_history) > 21:
            # Keep system prompt and last 20 messages
            system_msg = conversation_history[0]  
            recent_messages = conversation_history[-20:]
            conversation_history = [system_msg] + recent_messages
        
        return assistant_response
    
    except Exception as e:
        error_message = f"Error getting chat response: {str(e)}"
        print(error_message)
        return "I'm sorry, I encountered an error. Please try again."


def reset_conversation():
    """
    Reset the conversation history.
    
    Returns:
        str: Confirmation message
    """
    global conversation_history
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return "Conversation history cleared."


def get_conversation_history():
    """
    Get the current conversation history.
    
    Returns:
        list: List of conversation messages
    """
    return conversation_history.copy()


# Optional: Function to use a different Groq model
def set_model(model_name):
    """
    Change the Groq model being used.
    
    Available models:
    - llama-3.1-8b-instant (fast, efficient)
    - llama-3.1-70b-versatile (more capable, slower)
    - mixtral-8x7b-32768 (good balance)
    
    Args:
        model_name (str): Name of the model to use
    """
    global MODEL_NAME
    MODEL_NAME = model_name
    print(f"Model changed to: {MODEL_NAME}")
