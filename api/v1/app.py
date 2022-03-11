

from os import getenv
from flask import Flask, escape, request, Blueprint

from models import storage

from api.v1.views import app_views

if getenv("HBNB_API_HOST") is None:
    HBNB_API_HOST = '0.0.0.0'
else:
    HBNB_API_HOST = getenv("HBNB_API_HOST")
if getenv("HBNB_API_PORT") is None:
    HBNB_API_PORT = '5000'
else:
    HBNB_API_PORT = getenv("HBNB_API_PORT")

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """method to handle teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
