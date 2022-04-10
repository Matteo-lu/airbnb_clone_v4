

from os import getenv
from flask import Flask
from flask import make_response
from flask import jsonify
from models import storage
from flask_cors import CORS

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
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_db(exception):
    """method to handle teardown"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """Error Handler"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
