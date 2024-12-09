import requests
from django.shortcuts import render

def index(request):
    ciudad = request.GET.get('ciudad', 'Bogotá')
    fastapi_url = f"http://127.0.0.1:8001/weather/{ciudad}"

    try:
        response = requests.get(fastapi_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        data = {"error": "No se pudo obtener el clima. Inténtalo de nuevo."}

    return render(request, 'index.html', {'data': data, 'ciudad': ciudad})
