#!/usr/bin/python3
""" Build Flask """
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint
import os
import requests
import sys
from flask import jsonify
from models import storage


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current session."""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
