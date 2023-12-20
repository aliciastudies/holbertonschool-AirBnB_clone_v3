#!/usr/bin/python3
""" Index """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns a JSON status ok """
    return jsonify({"status": "OK"})
