import json


import requests

def get_data(location):
    TOKEN = "156d754bf9a6f2fe5e9464886ab39463bdf88a06"

    URL = f"https://api.waqi.info/feed/{location}/?token={TOKEN}"
    print("Getting Data...")
    response = requests.get(URL)
    data = response.text
    get_data = json.loads(data)
    print(get_data)
    print("Loading Data...")
    try:
        air_quality_index = get_data['data']['aqi']
        station_name = get_data['data']['city']['name']
        station_id = get_data['data']['idx']
        last_update = get_data['data']['time']['s']
        if 'pm25' in get_data.keys():
            pm25 = get_data['data']['iaqi']['pm25']['v']
        if 'pm10' in get_data.keys():
            pm10 = get_data['data']['iaqi']['pm10']['v']
        check_aqi(air_quality_index)
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



