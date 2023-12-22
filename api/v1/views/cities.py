#!/usr/bin/python3
""" Restful Api for city objects """

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_states_cities(state_id):
    """ Retrieves list of all city objects """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = state.cities
    cities_dict_list = []
    for city in cities_list:
        cities_dict_list.append(city.to_dict())
    return jsonify(cities_dict_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a city object by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city object by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)
    # 200 status code for success
    # added make_response


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a city obj """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    # return jsonify({"Not a JSON"}), 400
    if 'name' not in request.json:
        abort(400, description="Missing name")
    # return jsonify({"Missing name"}), 400

    city_data = request.get_json()
    new_city = City(name=city_data['name'], state_id=state_id)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
