# ⛅ Weather CLI

A terminal weather app built with Python. 
Get real-time weather for any city worldwide.

## Demo
<!-->
_____

## Features
- Real-time weather data via OpenWeatherMap API
- Temperature, humidity, wind, visibility
- Sunrise & sunset times in the city's local timezone
- Clean error handling for bad input & network issues

## Setup

1. Clone the repo
   git clone https://github.com/Hash-PJ/Weather-App

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Get a free API key at openweathermap.org

5. Create .env file
   WEATHER_API_KEY=your_key_here

## Usage
   - python weather.py Mumbai
   - python weather.py "New York"
   - python weather.py London

## Tech
Python · Requests · python-dotenv · OpenWeatherMap API

## License
MIT
