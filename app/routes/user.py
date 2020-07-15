"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api

from resources import UserResource

USER_BLUEPRINT = Blueprint("users", __name__)
Api(USER_BLUEPRINT).add_resource(
    UserResource, "/users/<int:id>"
)
