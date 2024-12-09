from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = "API_Key"  # Reemplaza con tu clave de API
BASE_URL_CURRENT = "http://api.weatherapi.com/v1/current.json"
BASE_URL_FORECAST = "http://api.weatherapi.com/v1/forecast.json"

# Inicializa la app FastAPI
app = FastAPI(
    title="Clima con FastAPI",
    description="API para consultar datos climáticos avanzados",
    version="1.1"
)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API del Clima Avanzado con FastAPI"}

@app.get("/weather/{city}")
def get_weather(city: str):
    """
    Obtiene el clima actual y pronósticos avanzados de una ciudad.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key no configurada.")

    # Clima actual
    params_current = {"key": API_KEY, "q": city, "lang": "es"}
    response_current = requests.get(BASE_URL_CURRENT, params=params_current)

    if response_current.status_code != 200:
        raise HTTPException(
            status_code=response_current.status_code,
            detail=f"Error al obtener los datos del clima: {response_current.json().get('error', {}).get('message', 'Error desconocido')}"
        )

    # Pronóstico extendido
    params_forecast = {"key": API_KEY, "q": city, "days": 3, "lang": "es"}
    response_forecast = requests.get(BASE_URL_FORECAST, params=params_forecast)

    if response_forecast.status_code != 200:
        raise HTTPException(
            status_code=response_forecast.status_code,
            detail=f"Error al obtener el pronóstico: {response_forecast.json().get('error', {}).get('message', 'Error desconocido')}"
        )

    # Procesar respuestas
    current_data = response_current.json()
    forecast_data = response_forecast.json()

    return {
        "clima_actual": {
            "ciudad": current_data.get("location", {}).get("name"),
            "pais": current_data.get("location", {}).get("country"),
            "temperatura": current_data.get("current", {}).get("temp_c"),
            "humedad": current_data.get("current", {}).get("humidity"),
            "sensacion_termica": current_data.get("current", {}).get("feelslike_c"),
            "uv": current_data.get("current", {}).get("uv"),
            "viento": {
                "velocidad_kph": current_data.get("current", {}).get("wind_kph"),
                "direccion": current_data.get("current", {}).get("wind_dir"),
            },
            "condiciones": {
                "descripcion": current_data.get("current", {}).get("condition", {}).get("text"),
                "icono": current_data.get("current", {}).get("condition", {}).get("icon"),
            },
        },
        "pronostico": [
            {
                "fecha": day.get("date"),
                "temperatura": {
                    "maxima": day.get("day", {}).get("maxtemp_c"),
                    "minima": day.get("day", {}).get("mintemp_c"),
                },
                "condiciones": day.get("day", {}).get("condition", {}).get("text"),
                "icono": day.get("day", {}).get("condition", {}).get("icon"),
                "lluvia_probabilidad": day.get("day", {}).get("daily_chance_of_rain"),
            }
            for day in forecast_data.get("forecast", {}).get("forecastday", [])
        ],
    }
