

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask import abort
from flask import request

from models import storage
from models.review import Review
from models.place import Place

@app_views.route(
                'places/<place_id>/reviews',
                strict_slashes=False
                )
def all_reviews(place_id):
    """view to return all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    obj_dict = []
    for value in reviews:
        obj_dict.append(value.to_dict())
    return (jsonify(obj_dict)), 200

@app_views.route(
                '/reviews/<review_id>,
                strict_slashes=False
                )
def review_by_id(review_id):
    """view to return review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404) 
    return (jsonify(review.to_dict())), 200

@app_views.route(
                '/reviews/<review_id>',
                strict_slashes=False,
                methods=['DELETE']
                )
def delete_review_by_id(review_id):
    """view to delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({})), 200

@app_views.route(
                'places/<place_id>/reviews',
                strict_slashes=False,
                methods=['POST']
                )
def create_review(place_id):
    """view to create a review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data:
        if 'name' not in data:
            abort(400, description="Missing name")
        new_review = Review()
        for key, value in data.items():
            setattr(new_review, key, value)
        setattr(new_review, 'place_id', place_id)
        new_review.save()
        return (jsonify(new_review.to_dict()), 201)
    abort(400, description="Not a JSON")

@app_views.route(
                'reviews/<review_id>,
                strict_slashes=False,
                methods=['PUT']
                )
def update_review(review_id):
    """view to update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key in ['update_at', 'create_at', 'id']:
            continue
        else:
            setattr(review, key, value)
            review.save()
            return (jsonify(review.to_dict()), 200)
