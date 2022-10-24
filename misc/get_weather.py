from datetime import datetime

import requests

from data.config import WEATHER_TOKEN

city_id = {'Минск': 625144,
           'Брест': 629634,
           'Витебск': 620127,
           'Гомель': 627907,
           'Гродно': 627904,
           'Могилев': 625665
           }


def get_weather(city: str) -> str:
    """Get request from OpenWeatherMap API and return parsed string"""
    params = {'id': city_id[city],
              'units': 'metric',
              'lang': 'ru',
              'appid': WEATHER_TOKEN}
    data = requests.get('https://api.openweathermap.org/data/2.5/weather?', params=params).json()
    # Parsing json
    time = datetime.fromtimestamp(data['dt']).time()
    temp = round(data['main']['temp'])
    feels_like = round(data['main']['feels_like'])
    pressure = round(data['main']['pressure'] / 1.333)
    city = data['name']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).time()
    sunset = datetime.fromtimestamp(data['sys']['sunset']).time()
    weather_desc = data['weather'][0]['description'].capitalize()
    wind_speed = data['wind']['speed']

    text = f"<u>В городе {city} по состоянию на {time}</u>:\n" \
           f"{weather_desc}.\n" \
           f"Температура {temp}°C, ощущается как {feels_like}°C\n" \
           f"Ветер: {wind_speed} м/с.\n" \
           f"Атмосферное давление: {pressure} мм. рт. ст.\n" \
           f"\n" \
           f"Восход: {sunrise}\n" \
           f"Закат: {sunset}"

    return text
