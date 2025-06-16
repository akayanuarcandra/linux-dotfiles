#!/usr/bin/env python3

from pyquery import PyQuery  # install using `pip install pyquery`
import json


################################### CONFIGURATION ###################################

# set your location_id
# This is the correct ID for Shenyang from the URL you provided.
location_id = "12ab11eb28d2b00c29aea4aabf8c1486763593def5bb869a7f8eac04a02366ed"

# celcius or fahrenheit
unit = "metric"  # metric or imperial

# forcase type
forecast_type = "Daily" # Hourly or Daily

########################################## MAIN ##################################

# weather icons
weather_icons = {
    "sunnyDay": "󰃠",
    "clearNight": "󰽥",
    "cloudyFoggyDay": " ",
    "cloudyFoggyNight": " ",
    "rainyDay": " ",
    "rainyNight": " ",
    "snowyIcyDay": "",
    "snowyIcyNight": "",
    "severe": "",
    "default": " ",
}

# --- Start of Changes ---

# This sets the correct region code from your working URL.
_l = "en-SG"
url = f"https://weather.com/{_l}/weather/today/l/{location_id}"

# This makes the script look like a real browser to prevent being blocked.
html_data = PyQuery(
    url=url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    },
)

# --- End of Changes ---


# current temperature
temp = html_data("span[data-testid='TemperatureValue']").eq(0).text()

# current status phrase
status = html_data("div[data-testid='wxPhrase']").text()
status = f"{status[:16]}.." if len(status) > 17 else status

# status code
status_code_class = html_data("#regionHeader").attr("class")
status_code = str(status_code_class).split(" ")[2].split("-")[2]

# status icon
icon = (
    weather_icons[status_code]
    if status_code in weather_icons
    else weather_icons["default"]
)

# temperature feels like
temp_feel = html_data(
    "div[data-testid='FeelsLikeSection'] > span > span[data-testid='TemperatureValue']"
).text()
temp_feel_text = f"Feels like {temp_feel}{'c' if unit == 'metric' else 'f'}"

# min-max temperature
temp_min = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(1)
    .text()
)
temp_max = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(0)
    .text()
)
temp_min_max = f"  {temp_min}\t\t  {temp_max}"

# wind speed
wind_speed = str(html_data("span[data-testid='Wind']").text())
wind_text = f"  {wind_speed}"

# humidity
humidity = html_data("span[data-testid='PercentageValue']").text()
humidity_text = f"  {humidity}"

# visibility
visbility = html_data("span[data-testid='VisibilityValue']").text()
visbility_text = f"  {visbility}"

# air quality index
air_quality_index = html_data("text[data-testid='DonutChartValue']").text()

# rain prediction
r_prediction_text = html_data(f"section[aria-label='{forecast_type} Forecast']")(
    "div[data-testid='SegmentPrecipPercentage'] > span"
).text()
r_prediction = str(r_prediction_text).replace("Chance of Rain", "")
r_prediction = f"  ({forecast_type}) {r_prediction}"
# if len(r_prediction) > 0 else r_prediction

# temperature prediction
t_prediction_text = html_data(f"section[aria-label='{forecast_type} Forecast']")(
    "div[data-testid='SegmentHighTemp'] > span"
).text()
t_prediction = str(t_prediction_text).replace(" /", "/")
t_prediction = f"  ({forecast_type}) {t_prediction}" 
# if len(t_prediction) > 0 else t_prediction

# tooltip text
tooltip_text = str.format(
    "\t\t{}\t\t\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}",
    f'<span size="xx-large">{temp}</span>',
    f"<big>{icon}</big>",
    f"<big>{status}</big>",
    f"<small>{temp_feel_text}</small>",
    f"<big>{temp_min_max}</big>",
    f"{wind_text}\t{humidity_text}",
    f"{visbility_text}\tAQI {air_quality_index}",
    f"<i>{r_prediction}</i>",
    f"<i>{t_prediction}</i>"
)

# print waybar module data
out_data = {
    "text": f"<span size='medium'>{temp}</span>C  <span size='large' color='#ffcfb8'>{icon}</span>",
    "alt": status,
    "tooltip": tooltip_text,
    "class": status_code,
}
print(json.dumps(out_data))