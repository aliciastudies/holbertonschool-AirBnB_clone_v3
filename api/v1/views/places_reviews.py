#!/usr/bin/python3
""" Restful API for reviews objects """
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves list of all review objects """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = places.reviews
    review_dict = []
    for review in reviews_list:
        review_dict.append(review.to_dict())
    return jsonify(review_dict)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a review object by ID """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review obj by ID """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a review obj """
    place = storage.get(Place, place_id)
    data = request.get_json()
    if place is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user_id = data.get('user_id')
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    if 'text' not in data:
        abort(400, description="Missing text")
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict(), 201))


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a review obj """
    review = storage.get(Review, review_id)
    data = request.get_json()
    if review is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_id', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
