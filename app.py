import streamlit as st
from agent_ai import jalankan_agent

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
        st.session_state.riwayat.append(("Kamu", prompt))
        with st.spinner("Sedang diproses oleh Agent..."):
            hasil = jalankan_agent(prompt)
            st.session_state.riwayat.append(("Agent", hasil))

# Tampilkan riwayat percakapan
for pengirim, isi in reversed(st.session_state.riwayat):
    if pengirim == "Kamu":
        st.chat_message("user").write(isi)
    else:
        st.chat_message("assistant").write(isi)
