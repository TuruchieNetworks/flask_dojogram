from flask import Flask

app = Flask(__name__)

DATABASE = 'dojogram_db'
app.secret_key = 'act1onD0jOgrAM'

# flash needs the session secret secret_key