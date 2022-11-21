import time
import backend

hour1 = int(time.strftime("%H"))

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
            city_data = backend.get_data(city_to_get_data_of, "ScaleUpdater")[value]
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
    except Exception as error:
        print("Error in ScaleUpdater: ", error)

while True:
    hour = int(time.strftime("%H"))
    if hour == hour1:
        average_germany("AQI")
        average_germany("PM10")
        average_germany("PM2.5")
        average_germany("No2")
        print("Waiting...")
        if hour1 == "23":
            hour1 = 0
        else:
            hour1 += 1

