

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.city import City
from models.state import State

@app_views.route('/cities', strict_slashes=False)
def all_cities():
    """view to return all states"""
    obj_dict = storage.all(State)
    cities = []
    for value in obj_dict.values():
        cities.append(value.to_dict())
    return (jsonify(cities)), 200

@app_views.route('/states/cities', strict_slashes=False)
def all_cities_by_states():
    """view to return all states"""
    state_dict = storage.all(State)
    city_dict = storage.all(City)
    obj_dict = {}
    for state in state_dict.values():
        cities = []
        for city in city_dict.values():
            if city.state_id == state.id:
                cities.append(city.to_dict())
        obj_dict[state.name] = cities
    return (jsonify(obj_dict)), 200

@app_views.route(
                '/states/<state_id>/cities',
                strict_slashes=False
                )
def all_cities_by_states_id(state_id):
    """view to return all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    obj_dict = []
    for value in cities:
        obj_dict.append(value.to_dict())
    return (jsonify(obj_dict)), 200

@app_views.route(
                '/cities/<city_id>',
                strict_slashes=False
                )
def city_by_id(city_id):
    """view to return city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404) 
    return (jsonify(city.to_dict())), 200

@app_views.route(
                '/cities/<city_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def delete_city_by_id(city_id):
    """view to delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                '/states/<state_id>/cities',
                strict_slashes=False,
                methods=['POST']
                )
def create_city(state_id):
    """view to create a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_city = City()
        for key, value in data.items():
            setattr(new_city, key, value)
        setattr(new_city, 'state_id', state_id)
        new_city.save()
        return (jsonify(new_city.to_dict()), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                'cities/<city_id>',
                strict_slashes=False,
                methods=['PUT']
                )
def update_city(city_id):
    """view to update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(city, key, value)
            city.save()
            return (jsonify(city.to_dict()), 200)
