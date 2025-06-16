#!/usr/bin/env python

# credits to: https://gist.github.com/bjesus/f8db49e1434433f78e5200dc403d58a3
# made some changes to the original script to support greek

import json
import requests
import time  # <-- 1. IMPORT THE TIME LIBRARY
from datetime import datetime

localization = {
    "en": {
        "feels_like": "Feels like",
        "wind": "Wind",
        "humidity": "Humidity",
        "today": "Today",
        "tomorrow": "Tomorrow",
        "day_after_tomorrow": "Day after tomorrow", # Added for consistency
        "weatherDesc": "weatherDesc",
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }
}

lang = "en"
text = localization[lang]
TEMP_COLOR = "#FFFFFF"  # Example: White for temperature
ICON_COLOR = "#E6CEFF"  # Example: Yellow for the icon

WEATHER_CODES = {
    '113': '󰃠', '116': '', '119': '󰅟', '122': '󰅟', '143': '',
    '176': '', '179': '', '182': '', '185': '', '200': '',
    '227': '', '230': '', '248': '', '260': '', '263': '',
    '266': '', '281': '', '284': '', '293': '', '296': '',
    '299': '', '302': '', '305': '', '308': '', '311': '',
    '314': '', '317': '', '320': '', '323': '', '326': '',
    '329': '', '332': '', '335': '', '338': '', '350': '',
    '353': '', '356': '', '359': '', '362': '', '365': '',
    '368': '', '371': '', '374': '', '377': '', '386': '',
    '389': '🌩', '392': '', '395': ''
}

data = {}

try:
    # --- Start of Changes ---
    # 2. GET A UNIQUE NUMBER (THE CURRENT TIME AS AN INTEGER)
    timestamp = int(time.time())

    # 3. ADD THE TIMESTAMP TO THE URL TO MAKE IT UNIQUE FOR EACH REQUEST
    weather_url = f"https://{lang}.wttr.in/Shenyang?format=j1&_={timestamp}"
    # --- End of Changes ---
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    weather = requests.get(weather_url, headers=headers).json()

    def format_time(time_str):
        # time_str is like "0", "100", "1200", "2300"
        if len(time_str) < 3: # "0"
             return "00"
        return time_str[:-2].zfill(2) # "1200" -> "12", "100" -> "01"

    def format_temp(temp_str):
        return (temp_str + "°").ljust(4)

    def format_chances(hour_data):
        chance_keys = [
            "chanceoffog", "chanceoffrost", "chanceofovercast",
            "chanceofrain", "chanceofsnow", "chanceofsunshine",
            "chanceofthunder", "chanceofwindy"
        ]
        probs = {
            text[event_key]: int(hour_data.get(event_key, "0"))
            for event_key in chance_keys
            if int(hour_data.get(event_key, "0")) > 0
        }
        sorted_probs = dict(sorted(probs.items(), key=lambda item: (-item[1], item[0])))
        conditions = [f"{event_name} {prob_val}%" for event_name, prob_val in sorted_probs.items()]
        return ", ".join(conditions)

    current_condition = weather['current_condition'][0]
    data['text'] = f"<span color='{TEMP_COLOR}'>{current_condition['FeelsLikeC']}°C</span> <span size='10.5pt' color='{ICON_COLOR}'>{WEATHER_CODES[current_condition['weatherCode']]}</span> <span>" "</span>"

    weather_desc_key = text['weatherDesc']
    
    current_desc_val = current_condition[weather_desc_key]
    if isinstance(current_desc_val, list):
        current_desc_display = current_desc_val[0]['value']
    else:
        current_desc_display = current_desc_val

    data['tooltip'] = f"<b>{current_desc_display} {current_condition['temp_C']}°</b>\n"
    data['tooltip'] += f"{text['feels_like']}: {current_condition['FeelsLikeC']}°\n"
    data['tooltip'] += f"{text['wind']}: {current_condition['windspeedKmph']}Km/h\n"
    data['tooltip'] += f"{text['humidity']}: {current_condition['humidity']}%\n"

    for i, day in enumerate(weather['weather']):
        data['tooltip'] += f"\n<b>"
        if i == 0:
            data['tooltip'] += f"{text['today']}, "
        elif i == 1:
            data['tooltip'] += f"{text['tomorrow']}, "
        elif i == 2 and 'day_after_tomorrow' in text:
            data['tooltip'] += f"{text['day_after_tomorrow']}, "
        
        data['tooltip'] += f"{day['date']}</b>\n"
        data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
        data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
        
        for hour_entry in day['hourly']:
            hour_time_int = int(hour_entry['time']) // 100 # Corrected division
            
            if i == 0 and hour_time_int < datetime.now().hour:
                continue
            
            hourly_desc_val = hour_entry[weather_desc_key]
            if isinstance(hourly_desc_val, list):
                hourly_desc_display = hourly_desc_val[0]['value']
            else:
                hourly_desc_display = hourly_desc_val

            data['tooltip'] += (
                f"{format_time(hour_entry['time'])}:00 "
                f"{WEATHER_CODES[hour_entry['weatherCode']]} "
                f"{format_temp(hour_entry['FeelsLikeC'])} "
                f"{hourly_desc_display}, {format_chances(hour_entry)}\n"
            )

except requests.exceptions.RequestException as e:
    data['text'] = "NW"
    data['tooltip'] = f"Error fetching weather: {e}"
except KeyError as e:
    data['text'] = "PE"
    data['tooltip'] = f"Error parsing weather data: {e}\nURL: {weather_url if 'weather_url' in locals() else 'Unknown'}"
except Exception as e:
    data['text'] = "ERR"
    data['tooltip'] = f"An unexpected error occurred: {e}"

print(json.dumps(data))