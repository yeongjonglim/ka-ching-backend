"""
Define the REST verbs relative to the users
"""

from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import UserRepository
from utils import parse_params, get_token_auth_header


class LoginResource(Resource):
    """ To login a user with email and password """

    @staticmethod
    @parse_params(
        Argument("email", location="json", required=True),
        Argument("password", location="json", required=True)
    )
    def post(email, password):
        """ Update an user based on the sent information """
        repository = UserRepository()
        token = repository.login(email, password)
        if token:
            return jsonify(token=token.decode("utf-8"))


class LogoutResource(Resource):
    """ To logout a user with token """

    @staticmethod
    def post():
        """ Blacklist user's token without any parameters """
        token = get_token_auth_header()
        repository = UserRepository()
        repository.logout(token)
        return {}, 204


class RegisterUserResource(Resource):
    """ To register a user and return a token upon success """

    @staticmethod
    @parse_params(
        Argument("email", location="json", required=True),
        Argument("password", location="json", required=True),
        Argument("first_name", location="json", required=True),
        Argument("last_name", location="json", required=True)
    )
    def post(email, password, first_name, last_name):
        repository = UserRepository()
        token = repository.create(email, password, first_name, last_name)
        return jsonify(token=token.decode("utf-8")), 201
