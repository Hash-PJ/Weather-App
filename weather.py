from dotenv import load_dotenv as load_env
import os
import requests
import sys
import time

load_env()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Error: WEATHER_API_KEY missing from .env!")
        return None
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = {
            "city": f'{data.get("name")}, {data.get("sys").get("country")}',
            "description": data.get("weather")[0].get("description"),
            "temperature": f'{data.get("main").get("temp")} °C',
            "feels like": f'{data.get("main").get("feels_like")} °C',
            "humidity": f'{data.get("main").get("humidity")} %',
            "wind": f'{data.get("wind").get("speed")} m/s',
            "visibility": f'{data.get("visibility")} km',
            "sunrise": f'{time.strftime("%H:%M:%S", time.localtime(data.get("sys").get("sunrise")))} {time.tzname[0]}',
            "sunset": f'{time.strftime("%H:%M:%S", time.localtime(data.get("sys").get("sunset")))} {time.tzname[0]}',
            "time now": f'{time.strftime("%H:%M:%S")} {time.tzname[0]}'
            }
        return weather
    except requests.exceptions.ConnectionError:
        print("No internet connection!")
    except requests.exceptions.Timeout:
        print("Request timed out - server took too long!")
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(f"city '{city}' not found!")
        elif response.status_code == 401:
            print("Invalid API key - Check your .env file!")
        else:
            print(f'API error: {response.status_code}')
    return None


def display_weather(weather):
    print('_'*50)
    print(f'|{weather.pop("city")}|')
    print(f'|{weather.pop('description')}|')
    print('-'*50)
    for k, v in weather.items():
        print(f"|{k.title()}: {v}|")
    print('_'*50)


def main():
    if len(sys.argv) < 2:
        print("Usage: Python weather.py <city>")
        sys.exit(1)
    city = " ".join(sys.argv[1:])
    weather = get_weather(city)
    if weather:
        display_weather(weather)

if __name__ == "__main__":
    main()
