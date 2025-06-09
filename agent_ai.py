from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import Tool
import os
from wiki_tool import wiki_tool
from weather_tool import weather_tool
import streamlit as st

# Load API Key dari secrets
openai_api_key = st.secrets["api_keys"]["openai"]

# Model
llm = ChatOpenAI(temperature=0.2, openai_api_key=openai_api_key)

# Tools untuk agent
tools = [wiki_tool, weather_tool]

# Inisialisasi Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def jalankan_agent(prompt: str) -> str:
    try:
        hasil = agent_executor.run(prompt)
        return hasil
    except Exception as e:
        return f"Terjadi kesalahan saat menjalankan agent: {str(e)}"
