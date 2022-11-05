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
    luft = backend.get_data(stadt)
    return jsonify({'stadt': stadt,
                    'luftqualitaet': luft})

@app.route('/luft')
def luft():
    country = request.args.get('country')
    try: 
        luft = backend.get_data(country)
        aqi = luft['AQI']
        max_scale, scale, index = backend.scale_germany(avg_aqi, avg_no2, avg_pm25, avg_pm10, luft)

        Stationsname = luft['Station Name']
        Updatestatus = luft['Last Update']
        quality = luft['Air Quality']


        return render_template('daten.html',Stationsname = Stationsname,Updatestatus = Updatestatus,quality = quality,lueften = lueften,max_scale = max_scale, scale = scale, index= index)
    except:
        return render_template('main.html',Error=True)

if __name__ == '__main__':
    avg_aqi = backend.average_germany("AQI")
    avg_pm10 = backend.average_germany("PM10")
    avg_pm25 = backend.average_germany("PM2.5")
    avg_no2 = backend.average_germany("No2")

    app.run(debug=True)
