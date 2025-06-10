# agent_ai.py

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI  # Tidak deprecated
from langchain_core.tools import Tool                   # Bukan dari agent_toolkits!
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st

from wiki_tool import wiki_tool
from weather_tool import weather_tool

# ===============================================
# Inisialisasi Model & Tools
# ===============================================

def buat_agent_executor() -> AgentExecutor:
    """
    Membuat agent executor menggunakan ReAct (LangChain core terbaru).
    Returns:
        AgentExecutor: Objek agent yang siap menerima prompt.
    """

    openai_api_key = st.secrets["api_keys"]["openai"]

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        api_key=openai_api_key,
    )

    tools: list[Tool] = [wiki_tool, weather_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Kamu adalah asisten AI yang cerdas dan membantu."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor

# ===============================================
# Fungsi Utama
# ===============================================

def jalankan_agent(prompt: str) -> str:
    """
    Menjalankan prompt pengguna menggunakan AgentExecutor.
    Args:
        prompt (str): Input atau pertanyaan dari user.
    Returns:
        str: Jawaban dari AI atau error message.
    """
    try:
        agent = buat_agent_executor()
        hasil = agent.invoke({"input": prompt})
        return hasil["output"]
    except Exception as e:
        return f"❌ Terjadi kesalahan saat menjalankan agent:\n{str(e)}"
