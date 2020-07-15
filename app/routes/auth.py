"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api

from resources import LoginResource, LogoutResource, RegisterUserResource

AUTH_BLUEPRINT = Blueprint("auth", __name__)
Api(AUTH_BLUEPRINT).add_resource(
    LoginResource, "/auth/login"
)
Api(AUTH_BLUEPRINT).add_resource(
    LogoutResource, "/auth/logout"
)
Api(AUTH_BLUEPRINT).add_resource(
    RegisterUserResource, "/auth/register"
)
