from fastmcp import FastMCP
import httpx
from pydantic import BaseModel

app = FastMCP(name="multi-api-server")


# ==========================================================
# 1) TOOL – Cat Facts API
# ==========================================================

class CatFactResponse(BaseModel):
    fact: str

@app.tool()
def get_cat_fact() -> CatFactResponse:
    """
    Retorna um fato aleatório sobre gatos.
    """
    url = "https://catfact.ninja/fact"
    response = httpx.get(url, timeout=10)
    data = response.json()

    return CatFactResponse(fact=data["fact"])


# ==========================================================
# 2) TOOL – Open-Meteo Weather API
# ==========================================================

class WeatherInput(BaseModel):
    latitude: float
    longitude: float

class WeatherResponse(BaseModel):
    temperature: float
    windspeed: float
    winddirection: float

@app.tool()
def get_weather(input: WeatherInput) -> WeatherResponse:
    """
    Retorna a previsão do tempo atual para uma coordenada.
    Usa Open-Meteo (gratuita e sem API key).
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude={lat}&longitude={lon}&current_weather=true"
    ).format(lat=input.latitude, lon=input.longitude)

    response = httpx.get(url, timeout=10)
    weather = response.json()["current_weather"]

    return WeatherResponse(
        temperature=weather["temperature"],
        windspeed=weather["windspeed"],
        winddirection=weather["winddirection"]
    )


# ==========================================================
# 3) TOOL – Chuck Norris Jokes (terceira API opcional)
# ==========================================================

class JokeResponse(BaseModel):
    joke: str

@app.tool()
def chuck_norris_joke() -> JokeResponse:
    """
    Retorna uma piada aleatória do Chuck Norris.
    """
    url = "https://api.chucknorris.io/jokes/random"
    response = httpx.get(url, timeout=10)
    data = response.json()

    return JokeResponse(joke=data["value"])


# ==========================================================
# Iniciar MCP Server
# ==========================================================

if __name__ == "__main__":
    app.run(transport="http", host="127.0.0.1", port=8000)
