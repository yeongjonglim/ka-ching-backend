"""
Define the REST verbs relative to the users
"""

from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import UserRepository
from utils import parse_params


class UserResource(Resource):
    """ Verbs relative to the users """

    @staticmethod
    def get(id):
        """ Return an user key information based on his name """
        user = UserRepository.get(id=id)
        if user:
            return jsonify({"user": user.json})
        return {}, 404

    @staticmethod
    @parse_params(
        Argument("starting_asset", location="json"),
        Argument("starting_liability", location="json")
    )
    def put(id, starting_asset=None, starting_liability=None):
        """ Update an user based on the sent information """
        repository = UserRepository()
        user = repository.update(id, starting_asset, starting_liability)
        return jsonify({"user": user.json})
