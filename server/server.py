from flask import (
    Flask,
    render_template,
    jsonify,
    request
)


import backend

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    backend.get_list()
    return render_template('main.html')

@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/doc-api')
def doc_api():
    return render_template('doc-api.html')

@app.route('/api')
def api():
    try:
        city = request.args.get('city')
        normaldata = backend.get_data(city, "Server")
        data = backend.get_data(city, "API")
        max_points, points, index, forecast_day1_index, aqi_avg, pm25_avg, no2_avg, underpm10, underpm25, underno2, pm10_avg, dif_pm10, dif_no2, dif_pm25, no2_plus, pm25_plus, pm10_plus = backend.scale_germany(normaldata)
        if "ä" in index:
            index = index.replace("ä", "")
        f_data = {
            "Version": "0.3",
            "Copyright": "(C)2022-2023 Wann-soll-ich-lueften.de; api.waqi.info",
            "Data from": "api.waqi.info",
            "Station Name": data[1],
            "Station Id": data[0],
            "Last Update": data[2],
            "PM10": data[4],
            "PM2.5": data[5],
            "NO2": data[6],
            "Forecast Date": data[8],
            "Forecast PM10": data[10],
            "Forecast PM2.5": data[11],
            "Difference PM10": dif_pm10,
            "Difference PM2.5": dif_pm25,
            "Difference No2": dif_no2,
            "Average AQI Germany": aqi_avg,
            "Average PM25 Germany": pm25_avg,
            "Average Pm10 Germany": pm10_avg,
            "Average NO2 Germany": no2_avg,
            "Ventilate? Index": index,
            "Ventilate? Forecast Index": forecast_day1_index,
            "Max Scale Points": max_points,
            "Points reached": points

        }
        return jsonify(f_data)

    except:
        f_data = {
            "Error": f"City {city} couldn't be found",
            "Tipp": "Maybe look if the City is spelled correctly",
            "Server Response": "404-City not found"
        }
        return jsonify(f_data)


@app.route('/style.css')
def style():
    return render_template('style.css')


@app.route('/table.html')
def table():
    return render_template("table.html", encoding='unicode_escape')


# http://localhost:5000/lueften.json?stadt=Berlin
@app.route('/lueften.json')
def lueften():
    stadt = request.args.get('stadt')
    luft = backend.get_data(stadt, "Server")
    return jsonify({'stadt': stadt,
                    'luftqualitaet': luft})


@app.route('/luft')
def luft():
    try:
        country = request.args.get('city')
        luft = backend.get_data(country, "Server")
        print(luft)
        requests = luft["Requests"]
        Stationsname = luft['Station Name']
        Updatestatus = luft['Last Update']
        quality = luft['Air Quality']
        forecast_1_avg_pm25 = luft['Forecast PM2.5 Avg']
        forecast_1_avg_pm10 = luft['Forecast PM10 Avg']
        PM25 = luft['PM2.5']
        PM10 = luft['PM10']
        No2 = luft['No2']

        max_scale, scale, index, forecast_day1, aqi_avg, pm25_avg, no2_avg, pm10_avg, underpm10, underpm25, underno2, dif_pm10, dif_no2, dif_pm25, no2_plus, pm25_plus, pm10_plus = backend.scale_germany(
            luft)

        return render_template('daten.html', Stationsname=Stationsname, Updatestatus=Updatestatus, quality=quality,
                               lueften=lueften, max_scale=max_scale, scale=scale, index=index,
                               forecast_day1_index=forecast_day1, forecast_1_avg_pm25=forecast_1_avg_pm25,
                               forecast_1_avg_pm10=forecast_1_avg_pm10, requests=requests, country=country, Pm25=PM25,
                               PM10=PM10, No2=No2, pm10_avg=round(float(pm10_avg), 2), pm25_avg=round(float(pm25_avg), 2),
                               no2_avg=round(float(no2_avg), 2),
                               underpm25=underpm25, underno2=underno2, underpm10=underpm10, dif_pm25=dif_pm25, dif_no2=dif_no2, dif_pm10=dif_pm10, no2_plus=no2_plus,
                               pm25_plus=pm25_plus, pm10_plus=pm10_plus)
    except:
        return render_template("main.html", Error=True)
if __name__ == '__main__':
    backend.average_germany("AQI")
    backend.average_germany("PM10")
    backend.average_germany("PM2.5")
    backend.average_germany("No2")

    app.run(debug=True, host="0.0.0.0")
