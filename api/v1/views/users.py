

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.user import User

@app_views.route('/users', strict_slashes=False)
def all_users():
    """view to return all places"""
    obj_dict = storage.all(User)
    users = []
    for value in obj_dict.values():
        users.append(value.to_dict())
    return (jsonify(users)), 200

@app_views.route('/users/<user_id>', strict_slashes=False)
def user_by_id(user_id):
    """view to return user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404) 
    return (jsonify(user.to_dict())), 200

@app_views.route(
                '/users/<user_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def user_place_by_id(user_id):
    """view to delete user by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                '/users',
                strict_slashes=False,
                methods=['POST']
                )
def create_user():
    """view to create a user"""
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_user = User()
        for key, value in data.items():
            setattr(new_user, key, value)
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                '/users/<user_id>',
                strict_slashes=False,
                methods=['PUT']
                )
def update_user(user_id):
    """view to user a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(user, key, value)
            user.save()
            return (jsonify(user.to_dict()), 200)
