

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.city import City
from models.place import Place

@app_views.route(
                '/cities/<city_id>/places',
                strict_slashes=False
                )
def all_places(city_id):
    """view to return all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    obj_dict = []
    for value in places:
        obj_dict.append(value.to_dict())
    return (jsonify(obj_dict)), 200

@app_views.route(
                '/places/<place_id>,
                strict_slashes=False
                )
def place_by_id(place_id):
    """view to return place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404) 
    return (jsonify(place.to_dict())), 200

@app_views.route(
                'places/<place_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def delete_place_by_id(place_id):
    """view to delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                '/cities/<city_id>/places',
                strict_slashes=False,
                methods=['POST']
                )
def create_place(city_id):
    """view to create a place"""
    city = storage.get(City, city_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_place = Place()
        for key, value in data.items():
            setattr(new_place, key, value)
        setattr(new_place, 'city_id', city_id)
        new_place.save()
        return (jsonify(new_place.to_dict()), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                'places/<place_id>',
                strict_slashes=False,
                methods=['PUT']
                )
def update_place(place_id):
    """view to update a city"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(place, key, value)
            place.save()
            return (jsonify(place.to_dict()), 200)
