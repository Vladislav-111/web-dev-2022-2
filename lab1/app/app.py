from flask import Flask

app = Flask(__name__)
application = app

@app.route('/')
def index():
    1/0
    return 'qq'