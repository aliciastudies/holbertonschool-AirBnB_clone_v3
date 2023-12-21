#!/usr/bin/python3
""" Restful Api for state objects """

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves list of all state objects """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a state object by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state object by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200 
    # 200 status code for success


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates new state object"""
    if not request.json:
        return jsonify({"Not a JSON"}), 400

    if 'name' not in request.json:
        return jsonify({"Missing name"}), 400

    new_state = State(**request.getjson())
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.json:
        return jsonify({"Not a JSON"}), 400

    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
