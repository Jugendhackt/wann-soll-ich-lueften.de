import json

import matplotlib
import requests
import prettytable
from pasta.augment import inline

list = prettytable.PrettyTable()
list.field_names = ["Stadt", "Aufgerufen (Mal)"]
list.set_style(prettytable.PLAIN_COLUMNS)


def get_data(location, message):
    TOKEN = "156d754bf9a6f2fe5e9464886ab39463bdf88a06"
    URL = f"https://api.waqi.info/feed/{location}/?token={TOKEN}"
    print(f"Getting Data...      Called by {message}")
    response = requests.get(URL)
    response_data = response.text
    get_data = json.loads(response_data)
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
    if "ö" in location:
        new_location = location.replace("ö", "oe")
    elif "ä" in location:
        new_location = location.replace("ä", "ae")
    elif "ü" in location:
        new_location = location.replace("ü", "ue")
    else:
        new_location = location
    try:
        with open(f"data/{new_location}", "r") as data_loc:
            loc_request = int(data_loc.read())
        with open(f"data/{new_location}", "w") as data_loc_w_n:
            new_loc_r = loc_request = loc_request + 1
            print(new_loc_r)
            data_loc_w_n.write(str(new_loc_r))
        try:
            list.sort_key(new_location)
            del_row = list.get_string(fields=["Stadt"], end=1)
            del_row2 = list.get_string(fields=["Stadt"], start=1, end=2)
            print(del_row2)
            print(del_row)
            if del_row == new_loc_r:
                if del_row2 == new_loc_r:
                    list.del_row(del_row)

        except:
            pass
    except:
        with open(f"data/{new_location}", "w") as data_loc_w:
            data_loc_w.write("1")
            new_loc_r = 1
    if message == "API":
        forecast_day = forecast_1_pm10_day
        data = [station_id, station_name, last_update, new_loc_r, pm10, pm25, no2, forecast_1_pm25_day, forecast_day,
                forecast_1_pm25_day, forecast_1_pm25_avg, forecast_1_pm10_avg]
        return data
    else:
        list.add_row([new_location, new_loc_r])
        air_quality_data = {
            "AQI": air_quality_index,
            "Air Quality": index,
            "Station Name": station_name,
            "Station ID": station_id,
            "Last Update": last_update,
            "Requests": new_loc_r,
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


def make_diagram(city, PM2_5=None, PM10=None, NO2=None, NO2_avg=None, PM10_avg=None, PM2_5_avg=None, time=None):
    import pandas
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import style

    plt.switch_backend('agg')
    print("Making Diagram...")
    time_data = {'NO2': [NO2, NO2_avg], 'PM10': [PM10, PM10_avg], 'PM2.5': [PM2_5, PM2_5_avg]}
    df = pandas.DataFrame(time_data, columns=['NO2', 'PM10', 'PM2.5'])
    #Define names of grupes on X axis
    names = [f"In {city} ({time})", f"In Deutschland (⌀)"]
    #Position of bars on X axis
    x = np.arange(len(names))
    #Define width of bars
    width = 0.25
    #Make the plot
    print("Plotting...")
    style.use('ggplot')
    plt.bar(x, df['NO2'], width, color='red', label='NO2')
    plt.bar(x + width, df['PM10'], width, color='green', label='PM10')
    plt.bar(x + width + width, df['PM2.5'], width, color='blue', label='PM2.5')
    plt.xticks(x + width / 3, names)
    plt.title(f"Wann soll ich lüften in {city}?")
    plt.xlabel("Luftqualität")
    plt.ylabel("Emissionen in µg/m³ und µm/m³")
    plt.legend(loc='best')
    print("Saving...")
    plt.savefig(f"static/diagrams/0.png")
    plt.close()
    print("Done!")
    return f"static/diagrams/0.png"



def get_list():
    with open("templates/table.html", "w") as table_write:
        table_write.write(
            list.get_html_string(attributes={"id": "my_table", "class": "red_table"}, end=10, sortby="Aufgerufen (Mal)",
                                 reversesort=True))


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
            city_data = get_data(city_to_get_data_of, message="Average Germany Function")[value]
            if not city_data == None:
                data = data + city_data
            else:
                city_list_len -= 1
        data = data / city_list_len
        print(data)
        if value == "AQI":
            with open("data/avg_aqi", "w") as avg_aqi:
                avg_aqi.write(str(data))
        elif value == "PM10":
            with open("data/avg_pm10", "w") as avg_pm10:
                avg_pm10.write(str(data))
        elif value == "PM2.5":
            with open("data/avg_pm25", "w") as avg_pm25:
                avg_pm25.write(str(data))
        elif value == "No2":
            with open("data/avg_no2", "w") as avg_no2:
                avg_no2.write(str(data))
        return data
    except:
        return None


def scale_germany(data):
    with open("data/avg_aqi", "r") as avg_aqi_r:
        aqi_avg = float(avg_aqi_r.read())

    with open("data/avg_no2", "r") as avg_no2_r:
        no2_avg = float(avg_no2_r.read())

    with open("data/avg_pm25", "r") as avg_pm25_r:
        pm25_avg = float(avg_pm25_r.read())

    with open("data/avg_pm10", "r") as avg_pm10_r:
        pm10_avg = float(avg_pm10_r.read())
    points = 0
    underno2 = 0
    underpm10 = 0
    underpm25 = 0
    dif_no2 = 0
    dif_pm10 = 0
    dif_pm25 = 0
    no2_plus = ""
    pm10_plus = ""
    pm25_plus = ""
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
            dif_no2 = round(no2_avg - city_no2, 2)
            print(dif_no2)
            no2_plus = "-"
            points += 2
            underno2 += 1
        else:
            no2_plus = "+"
            dif_no2 = round(city_no2 - no2_avg, 2)
            print(dif_no2)
    else:
        max_points -= 2
    print(underpm25)
    print(underno2)
    print(underpm10)

    if not city_pm10 == None:
        if city_pm10 < pm10_avg:
            dif_pm10 = round(pm10_avg - city_pm10, 2)
            print(dif_pm10)
            pm10_plus = "-"
            points += 2
            underpm10 += 1
        else:
            pm10_plus = "+"
            dif_pm10 = round(city_pm10 - pm10_avg, 2)
            print(dif_pm10)
    else:
        max_points -= 2
    print(underpm25)
    print(underno2)
    print(underpm10)

    if not city_pm25 == None:
        if city_pm25 < pm25_avg:
            points += 2
            pm25_plus = "-"
            dif_pm25 = round(pm25_avg - city_pm25, 2)
            print(dif_pm25)
            underpm25 += 1
        else:
            pm25_plus = "+"
            dif_pm25 = round(city_pm25 - pm25_avg, 2)
            print(dif_pm25)
    else:
        max_points -= 2
    print(underpm25)
    print(underno2)
    print(underpm10)

    if not city_aqi == None:
        if city_aqi < aqi_avg:
            points += 4

    if forecast_day1_pm10 < pm10_avg:
        points_forecast += 2
    if forecast_day1_pm25 < pm25_avg:
        points_forecast += 2

    if points_forecast == 0:
        forecast_day1_index = "Kein Guter Tag"
    elif points_forecast == 2:
        forecast_day1_index = "Guter Tag"
    elif points_forecast == 4:
        forecast_day1_index = "Perfekter Tag"

    if max_points == 10:
        if points <= 2:
            index = "Auf keinen Fall!"
        if points == 4:
            index = "Demnächst!"
        if points == 6:
            index = "Wenn du es eilig hast"
        if points == 8:
            index = "Jetzt"
        if points == 10:
            index = "Sofort"
    elif max_points == 8:
        if points == 0:
            index = "Auf keinen Fall!"
        if points == 2:
            index = "Demnächst!"
        if points == 4:
            index = "Wenn du es eilig hast"
        if points == 6:
            index = "Jetzt"
        if points == 8:
            index = "Sofort"
    elif max_points == 6:
        if points == 0:
            index = "Auf keinen Fall!"
        if points == 2:
            index = "Wenn du es eilig hast"
        if points == 4:
            index = "Jetzt"
        if points == 6:
            index = "Sofort"

    if underpm10 == 1:
        underpm10 = "↓"
    else:
        underpm10 = "↑"
    if underpm25 == 1:
        underpm25 = "↓"
    else:
        underpm25 = "↑"
    if underno2 == 1:
        underno2 = "↓"
    else:
        underno2 = "↑"

    print(underpm25)
    print(underno2)
    print(underpm10)

    return max_points, points, index, forecast_day1_index, aqi_avg, pm25_avg, no2_avg, pm10_avg, underpm10, underpm25, underno2, \
           dif_pm10, dif_no2, dif_pm25, \
           no2_plus, pm25_plus, pm10_plus


if __name__ == '__main__':
    make_diagram("Berlin", PM10_avg=10, PM2_5_avg=273, NO2_avg=21, PM10=19, PM2_5=60, NO2=70)
