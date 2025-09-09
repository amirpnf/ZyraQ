from flask import Blueprint, jsonify

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/users")
def get_users():
    return jsonify([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
