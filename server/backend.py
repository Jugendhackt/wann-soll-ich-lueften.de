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
    pm25 = None
    pm10 = None
    no2 = None
    air_quality_index = get_data['data']['aqi']
    station_name = get_data['data']['city']['name']
    station_id = get_data['data']['idx']
    last_update = get_data['data']['time']['s']
    forecast_1_pm25_day = get_data['data']['forecast']['daily']['pm25']
    forecast_1_pm25_avg = get_data['data']['forecast']['daily']['pm25']
    forecast_1_pm10_day = get_data['data']['forecast']['daily']['pm10']
    forecast_1_pm10_avg = get_data['data']['forecast']['daily']['pm10']
    forecast_1_pm10_avg = forecast_1_pm10_avg[1]['avg']
    forecast_1_pm10_day = forecast_1_pm10_day[1]['day']
    forecast_1_pm25_avg = forecast_1_pm25_avg[1]['avg']
    forecast_1_pm25_day = forecast_1_pm25_day[1]['day']
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
    try:
        no2 = get_data['data']['iaqi']['no2']['v']
    except Exception as error:
        pass
    index = check_aqi(air_quality_index)
    air_quality_data = {
        "AQI": air_quality_index,
        "Air Quality": index,
        "Station Name": station_name,
        "Station ID": station_id,
        "Last Update": last_update,
        "PM2.5": pm25,
        "PM10": pm10,
        "No2": no2,
        "Forecast PM2.5 Day": forecast_1_pm25_day,
        "Forecast PM2.5 Avg": forecast_1_pm25_avg,
        "Forecast PM10 Day": forecast_1_pm10_day,
        "Forecast PM10 Avg": forecast_1_pm10_avg
    }
    print(air_quality_data)
    return air_quality_data



def check_aqi(aqi):
    index = "Not defined"
    if aqi <= 50:
        index = "Gut"
    elif 51 <= aqi <= 100:
        index = "Mäßig"
    elif 101 <= aqi <= 150:
        index = 'Ungesund für empfindliche Personengruppen'
    elif 151 <= aqi <= 200:
        index = "Ungesund"
    elif 201 <= aqi <= 300:
        index = 'Sehr Ungesund'
    elif aqi > 300:
        index = "Gesundheitsgefährdend"
    return index


def average_germany(value):
    try:
        data = 0
        cities = open("cities/cities", "r")
        city_list = cities.readlines()
        city_list_len = len(city_list)
        for n in range(city_list_len):
            city_list[n] = city_list[n].replace("\n", "")
        for city in range(city_list_len):
            city_to_get_data_of = city_list[city]
            city_data = get_data(city_to_get_data_of)[value]
            if not city_data == None:
                data = data + city_data
            else:
                city_list_len -= 1
        data = data / city_list_len
        return data
    except:
        return None


def scale_germany(aqi_avg, no2_avg, pm25_avg, pm10_avg, data):
    points = 0
    max_points = 10
    index = ""
    points_forecast = 0
    forecast_day1_index = ""
    city_no2 = data['No2']
    city_pm25 = data['PM2.5']
    city_pm10 = data['PM10']
    city_aqi = data['AQI']
    forecast_day1_pm25 = data['Forecast PM2.5 Avg']
    forecast_day1_pm10 = data['Forecast PM10 Avg']

    if not city_no2 == None:
        if city_no2 < no2_avg:
            points += 2
    else:
        max_points -= 2
    if not city_pm10 == None:
        if city_pm10 < pm10_avg:
            points += 2
    else:
        max_points -= 2
    if not city_pm25 == None:
        if city_pm25 < pm25_avg:
            points += 2
    else:
        max_points -= 2
    if not city_aqi == None:
        if city_aqi < aqi_avg:
            points += 4

    if forecast_day1_pm10 < pm10_avg:
        points_forecast += 2
    if forecast_day1_pm25 < pm25_avg:
        points_forecast += 2

    if points_forecast == 0:
        forecast_day1_index = "Morgen scheint kein guter Tag für's lüften zu sein!"
    elif points_forecast == 2:
        forecast_day1_index = "Morgen kannst du lüften!"
    elif points_forecast == 4:
        forecast_day1_index = "Morgen ist der perfekte Tag zum lüften!"

    if max_points == 10:
        if points <= 2:
            index = "Erst morgen wieder!"
        if points == 4:
            index = "Demnächst!"
        if points == 6:
            index = "Jetzt, wenn du es eilig hast"
        if points == 8:
            index = "Jetzt"
        if points == 10:
            index = "Jetzt sofort"
    elif max_points == 8:
        if points == 0:
            index = "Erst morgen wieder!"
        if points == 2:
            index = "Demnächst!"
        if points == 4:
            index = "Jetzt, wenn du es eilig hast"
        if points == 6:
            index = "Jetzt"
        if points == 8:
            index = "Jetzt sofort"
    elif max_points == 6:
        if points == 0:
            index = "Erst morgen wieder!"
        if points == 2:
            index = "Jetzt, wenn du es eilig hast"
        if points == 4:
            index = "Jetzt"
        if points == 6:
            index = "Jetzt sofort"

    return max_points, points, index, forecast_day1_index


if __name__ == '__main__':
    data = get_data("Köln")

