from flask import Flask
from config import *


app = Flask(__name__)

app.config['TESTING'] = TESTING
app.config['DEBUG'] = DEBUG


@app.route("/")
def root():
    return f'Main page'


@app.route("/api/v1/hello-world-<int:variant>")
def hello_world(variant):
    return f'Hello World {variant}'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
