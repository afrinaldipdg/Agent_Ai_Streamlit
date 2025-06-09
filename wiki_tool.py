import wikipedia
from langchain.tools import Tool

# Fungsi untuk mengambil ringkasan dari Wikipedia
def cari_di_wikipedia(pertanyaan: str) -> str:
    try:
        hasil = wikipedia.summary(pertanyaan, sentences=2, auto_suggest=True)
        return hasil
    except Exception as e:
        return f"Gagal mengambil informasi dari Wikipedia: {str(e)}"

# Tool LangChain
wiki_tool = Tool(
    name="Wikipedia",
    func=cari_di_wikipedia,
    description="Gunakan ini untuk mencari informasi dari Wikipedia berdasarkan kata kunci."
)
