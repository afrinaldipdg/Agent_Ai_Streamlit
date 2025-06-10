# agent_ai.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage # Import BaseMessage for type hinting
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

    # Menambahkan {tools} dan {tool_names} ke dalam prompt sistem
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Kamu adalah asisten AI yang cerdas dan membantu. Kamu memiliki akses ke alat-alat berikut: {tools}. Gunakan alat-alat ini sebagai berikut: {tool_names}"),
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

def jalankan_agent(prompt: str, chat_history: list[BaseMessage] = None) -> str:
    """
    Menjalankan prompt pengguna menggunakan AgentExecutor.
    Args:
        prompt (str): Input atau pertanyaan dari user.
        chat_history (list[BaseMessage]): Histori percakapan sebelumnya dalam format LangChain messages.
    Returns:
        str: Jawaban dari AI atau error message.
    """
    if chat_history is None:
        chat_history = []
    try:
        agent = buat_agent_executor()
        # Pass both the current prompt and the chat history
        hasil = agent.invoke({"input": prompt, "chat_history": chat_history})
        return hasil["output"]
    except Exception as e:
        return f"❌ Terjadi kesalahan saat menjalankan agent:\n{str(e)}"
