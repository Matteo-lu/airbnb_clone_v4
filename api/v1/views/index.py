

from api.v1.views import app_views
from flask import Flask
from flask import jsonify

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

@app_views.route('/status', strict_slashes=False)
def index():
    """method to return status ok"""
    return (jsonify(status="OK")), 200

@app_views.route('/stats', strict_slashes=False)
def count():
    """etrieves the number of each objects by type"""
    objs_count = {}
    for key, value in classes.items():
        objs_count[key] = storage.count(value)
    return (jsonify(objs_count)), 200
