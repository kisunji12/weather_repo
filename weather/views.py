from django.conf import settings
import requests
from django.shortcuts import render

def index(request):
    weather_data = None
    error = None
    api_key = settings.OPENWEATHERMAP_API_KEY  # Loaded from settings or env

    if request.method == "POST":
        if request.POST.get('city'):
            city = request.POST.get('city')
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q' : city,
                'units':'metric',
                'appid': api_key
                }
        
        else:
            error = "Please enter a city."
        
        if not error:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data.get('name'),
                    'temperature': data.get('main', {}).get('temp'),
                    'description': data.get('weather')[0].get('description'),
                    'icon': data.get('weather')[0].get('icon'),
                }
            else:
                error = "Unable to get weather data. Please try again."
    
    return render(request, 'weather/index.html', {'weather': weather_data, 'error': error})
