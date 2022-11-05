import json


import requests

def get_data(location):
    TOKEN = "156d754bf9a6f2fe5e9464886ab39463bdf88a06"

    URL = f"https://api.waqi.info/feed/{location}/?token={TOKEN}"
    print("Getting Data...")
    response = requests.get(URL)
    response_data = response.text
    get_data = json.loads(response_data)
    print(get_data)
    print("Loading Data...")
    try:
        pm25 = None
        pm10 = None
        air_quality_index = get_data['data']['aqi']
        station_name = get_data['data']['city']['name']
        station_id = get_data['data']['idx']
        last_update = get_data['data']['time']['s']
        try:
            # Emission von Feinstaub der Patikelgröße PM2.5
            pm25 = get_data['data']['iaqi']['pm25']['v']
        except:
            pass
        try:
            # Emission von Feinstaub der Patikelgröße PM10
            pm10 = get_data['data']['iaqi']['pm10']['v']
        except:
            pass
        index = check_aqi(air_quality_index)
        data = {
            "AQI": air_quality_index,
            "Air Quality": index,
            "Station Name": station_name,
            "Station ID": station_id,
            "Last Update": last_update,
            "PM2.5": pm25,
            "PM10": pm10

        }
        return data
    except TypeError:
        status = get_data['status']
        context = get_data['data']

def check_aqi(aqi):
    index = "Not defined"
    if aqi <= 50:
        index = "Gut"
    elif aqi >= 51 and aqi <= 100:
        index = "Mäßig"
    elif aqi >= 101 and aqi <=150:
        index = 'Ungesund für empfindliche Personengruppen'
    elif aqi >= 151 and aqi <=200:
        index = "Ungesund"
    elif aqi >= 201 and aqi <= 300:
        index = 'Sehr Ungesund'
    elif aqi > 300:
        index = "Gesundheitsgefährdend"
    return index


get_data("Köln")
