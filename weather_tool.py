import requests
from langchain.tools import Tool

# Fungsi pencarian cuaca
API_KEY = "openweathermapapi"  # Ganti saat deploy dari secrets.toml
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def cuaca_di_kota(kota: str) -> str:
    try:
        params = {"q": kota, "appid": API_KEY, "units": "metric"}
        res = requests.get(BASE_URL, params=params).json()
        if res.get("cod") != 200:
            return f"Cuaca tidak tersedia untuk kota: {kota}"
        info = res["weather"][0]["description"]
        suhu = res["main"]["temp"]
        return f"Cuaca di {kota}: {info}, suhu {suhu}°C"
    except Exception as e:
        return f"Gagal mengambil informasi cuaca: {str(e)}"

# Tool LangChain
weather_tool = Tool(
    name="Cuaca",
    func=cuaca_di_kota,
    description="Gunakan ini untuk mendapatkan informasi cuaca dari nama kota."
)
