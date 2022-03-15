

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """view to return all amenities"""
    obj_dict = storage.all(Amenity)
    amenities = []
    for value in obj_dict.values():
        amenities.append(value.to_dict())
    return (jsonify(amenities)), 200

@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_by_id(amenity_id):
    """view to return amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404) 
    return (jsonify(amenity.to_dict())), 200

@app_views.route(
                '/amenities/<amenity_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def delete_amenity_by_id(amenity_id):
    """view to delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                '/amenities',
                strict_slashes=False,
                methods=['POST']
                )
def create_amenity():
    """view to create a amenity"""
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_amenity = Amenity()
        for key, value in data.items():
            setattr(new_amenity, key, value)
        new_amenity.save()
        return (jsonify(new_amenity.to_dict()), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                '/amenities/<amenity_id>',
                strict_slashes=False,
                methods=['PUT']
                )
def update_amenity(amenity_id):
    """view to update a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(amenity, key, value)
            amenity.save()
            return (jsonify(amenity.to_dict()), 200)
