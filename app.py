import streamlit as st
from agent_ai import jalankan_agent
from langchain_core.messages import HumanMessage, AIMessage # Import message types

st.set_page_config(page_title="Agentic AI Chatbot", layout="centered")
st.title("🧠 Agentic AI Chatbot")
st.markdown("""
Interaktif AI dengan kemampuan agent:
- 🔍 Wikipedia
- ☁️ Informasi Cuaca
""")

# Inisialisasi session state untuk menyimpan histori
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# Input pengguna
prompt = st.text_input("Ketik pertanyaan atau perintah kamu:", "Apa itu LangChain?")

if st.button("Kirim"):
    if prompt:
        # Add the current user prompt to history for display
        st.session_state.riwayat.append(("Kamu", prompt))

        # Convert history for LangChain agent:
        # LangChain expects a list of HumanMessage and AIMessage objects.
        # Exclude the current user prompt from the history being sent to the agent
        # because it's already provided in the 'input' variable.
        lc_chat_history = []
        for sender, message_content in st.session_state.riwayat[:-1]: # Exclude the current user prompt
            if sender == "Kamu":
                lc_chat_history.append(HumanMessage(content=message_content))
            else:
                lc_chat_history.append(AIMessage(content=message_content))

        with st.spinner("Sedang diproses oleh Agent..."):
            # Pass both the current prompt and the formatted chat history
            hasil = jalankan_agent(prompt, lc_chat_history)
            st.session_state.riwayat.append(("Agent", hasil))

# Tampilkan riwayat percakapan
for pengirim, isi in reversed(st.session_state.riwayat):
    if pengirim == "Kamu":
        st.chat_message("user").write(isi)
    else:
        st.chat_message("assistant").write(isi)
