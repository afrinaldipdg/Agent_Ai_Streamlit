# agent_ai.py

from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
import streamlit as st

from wiki_tool import wiki_tool
from weather_tool import weather_tool

# ===============================================
# Inisialisasi LLM & Agent Tools
# ===============================================

def buat_agent_executor() -> object:
    """
    Menginisialisasi agent LangChain dengan LLM dan daftar tools.
    Returns:
        agent_executor (AgentExecutor): Agent yang siap menjalankan perintah.
    """
    openai_api_key = st.secrets["api_keys"]["openai"]

    # Inisialisasi model ChatOpenAI
    llm = ChatOpenAI(
        temperature=0.2,
        model="gpt-3.5-turbo",
        openai_api_key=openai_api_key
    )

    # Daftar tools eksternal yang bisa digunakan oleh agent
    tools: list[Tool] = [wiki_tool, weather_tool]

    # Agent zero-shot dengan reAct
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent_executor

# ===============================================
# Fungsi Eksekusi Prompt
# ===============================================

def jalankan_agent(prompt: str) -> str:
    """
    Menjalankan prompt pengguna ke agent dan mengembalikan hasil jawaban.
    
    Args:
        prompt (str): Input atau pertanyaan dari pengguna.

    Returns:
        str: Jawaban dari agent atau pesan error jika terjadi kesalahan.
    """
    try:
        agent = buat_agent_executor()
        hasil = agent.run(prompt)
        return hasil

    except Exception as e:
        return f"❌ Terjadi kesalahan saat menjalankan agent:\n{str(e)}"
