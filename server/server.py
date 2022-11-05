#
# https://www.educba.com/python-rest-server/
#
from flask import (
    Flask,
    render_template
)

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


# https://pythonbasics.org/flask-rest-api/