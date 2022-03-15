

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.state import State

@app_views.route('/states', strict_slashes=False)
def all_states():
    """view to return all states"""
    obj_dict = storage.all(State)
    states = []
    for value in obj_dict.values():
        states.append(value.to_dict())
    return (jsonify(states)), 200

@app_views.route('/states/<state_id>', strict_slashes=False)
def states_by_id(state_id):
    """view to return state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404) 
    return (jsonify(state.to_dict())), 200

@app_views.route(
                '/states/<state_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def delete_state_by_id(state_id):
    """view to delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                '/states',
                strict_slashes=False,
                methods=['POST']
                )
def create_state():
    """view to create a state"""
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_state = State()
        for key, value in data.items():
            setattr(new_state, key, value)
        new_state.save()
        return (jsonify(State.to_dict(new_state)), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                '/states/<state_id>',
                strict_slashes=False,
                methods=['PUT']
                )
def update_state(state_id):
    """view to update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(state, key, value)
            state.save()
            return (jsonify(state.to_dict()), 200)
