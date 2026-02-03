import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq 
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define Web Search Agent
web_search_agent = Agent(
    name='Web Agent',
    description="This is the agent for searching content from the website",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions="Always include the sources",
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

# Streamlit UI
st.title("🔍 Web Search AI Chatbot")
st.markdown("An AI-powered chatbot that searches the web and provides insightful responses with sources.")

# User Input
user_input = st.text_input("Ask me anything:")

if st.button("Search"):
    if user_input:
        with st.spinner("Searching..."):
            response = web_search_agent.print_response(user_input)
        st.write("### 🔎 AI Response:")
        st.write(response)
    else:
        st.warning("Please enter a question!")
