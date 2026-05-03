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

    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        timezone_offset = data.get("timezone", 0)

        def fmt_time(timestamp):
            return time.strftime("%H:%M:%S", time.gmtime(timestamp + timezone_offset))

        weather = {
            "city": f'{data.get("name", "Unknown")}, {data.get("sys", {}).get("country", "?")}',
            "description": data.get("weather", [{}])[0].get("description", "N/A"),
            "temperature": f'{data.get("main", {}).get("temp", "N/A")} °C',
            "feels like": f'{data.get("main", {}).get("feels_like", "N/A")} °C',
            "humidity": f'{data.get("main", {}).get("humidity", "N/A")} %',
            "wind": f'{data.get("wind", {}).get("speed", "N/A")} m/s',
            "visibility": f'{data.get("visibility", 0) / 1000:.1f} km',
            "sunrise": fmt_time(data.get("sys", {}).get("sunrise", 0)),
            "sunset": fmt_time(data.get("sys", {}).get("sunset", 0)),
        }
        return weather

    except requests.exceptions.ConnectionError:
        print("No internet connection!")
    except requests.exceptions.Timeout:
        print("Request timed out!")
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            print(f"City '{city}' not found!")
        elif response.status_code == 401:
            print("Invalid API key — check your .env!")
        else:
            print(f"API error: {response.status_code}")
    return None


def display_weather(weather):
    print("_" * 50)
    print(f'| {weather["city"]}')
    print(f'| {weather["description"].title()}')
    print("-" * 50)
    for k, v in weather.items():
        if k not in ("city", "description"):
            print(f"| {k.title():<12}: {v}")
    print("_" * 50)


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
