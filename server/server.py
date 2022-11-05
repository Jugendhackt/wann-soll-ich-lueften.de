from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

user = 'test'
rndmtxt = 'irgendwas halt'

import backend

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
    luft = backend.get_data(country)
    aqi = luft['AQI']
    averageaqi = backend.average_germany('aqi')
    lueften = 'Jetzt'
    #if aqi > averageaqi : 
    #    lueften = 'Nein'

    Stationsname = luft['Station Name']
    Updatestatus = luft['Last Update']
    quality = luft['Air Quality']


    return render_template('daten.html',Stationsname = Stationsname,Updatestatus = Updatestatus,quality = quality,lueften = lueften)

if __name__ == '__main__':
    app.run(debug=True)