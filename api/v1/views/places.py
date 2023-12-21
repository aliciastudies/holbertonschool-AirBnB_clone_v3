#!/usr/bin/python3
""" Restful Api for places objects """

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_states_place(city_id):
    """ Retrieves list of all Places objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = city.places
    place_dict_list = []
    for obj in place_list:
        place_dict_list.append(obj.to_dict())
    return jsonify(place_dict_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a place object by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a city object by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)
    # 200 status code for success
    # added make_responses


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a place obj """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    # return jsonify({"Not a JSON"}), 400
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")

    if 'name' not in request.json:
        abort(400, description="Missing name")
    # return jsonify({"Missing name"}), 400
    data = request.get_json()
    user_id = data.get('user_id')
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/place/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates city object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
