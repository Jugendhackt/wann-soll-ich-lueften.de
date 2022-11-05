from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('home.html')

# http://localhost:5000/lueften.json?stadt=Berlin
@app.route('/lueften.json')
def lueften():
    stadt = request.args.get('stadt')
    return jsonify({'stadt': stadt,
                    'luftqualitaet': 'schlecht'})

if __name__ == '__main__':
    app.run(debug=True)
