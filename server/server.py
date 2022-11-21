from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

user = 'test'
rndmtxt = 'irgendwas halt'

import backend

avg_aqi = 0
avg_pm10 = 0
avg_pm25 = 0
avg_no2 = 0

app = Flask(__name__, template_folder="templates")


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/style.css')
def style():
    return render_template('style.css')


@app.route('/script.js')
def script():
    return render_template('script.js')


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
        country = request.args.get('country')
        luft = backend.get_data(country, "Server")
        print(luft)
        Stationsname = luft['Station Name']
        Updatestatus = luft['Last Update']
        quality = luft['Air Quality']
        forecast_1_avg_pm25 = luft['Forecast PM2.5 Avg']
        forecast_1_avg_pm10 = luft['Forecast PM10 Avg']

        with open("data/avg_aqi", "r")as avg_aqi_r:
            avg_aqi = float(avg_aqi_r.read())

        with open("data/avg_no2", "r")as avg_no2_r:
            avg_no2 = float(avg_no2_r.read())

        with open("data/avg_pm25", "r")as avg_pm25_r:
            avg_pm25 = float(avg_pm25_r.read())

        with open("data/avg_pm10", "r")as avg_pm10_r:
            avg_pm10 = float(avg_pm10_r.read())

        max_scale, scale, index, forecast_day1 = backend.scale_germany(avg_aqi, avg_no2, avg_pm25, avg_pm10, luft)

        return render_template('daten.html', Stationsname=Stationsname, Updatestatus=Updatestatus, quality=quality,
                               lueften=lueften, max_scale=max_scale, scale=scale, index=index,
                               forecast_day1_index=forecast_day1, forecast_1_avg_pm25=forecast_1_avg_pm25,
                               forecast_1_avg_pm10=forecast_1_avg_pm10)
    except Exception as error:
        print(error)
        return render_template('main.html', Error=True)


if __name__ == '__main__':
    backend.average_germany("AQI")
    backend.average_germany("PM10")
    backend.average_germany("PM2.5")
    backend.average_germany("No2")

    app.run(debug=True, host="0.0.0.0")
