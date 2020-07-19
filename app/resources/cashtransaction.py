"""
Define the REST verbs relative to the cash transactions
"""
import datetime
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import CashTransactionRepository
from utils import parse_params, auth_required
from errors import FormatError


class CashTransactionResource(Resource):
    """ To login a user with email and password """

    @staticmethod
    @auth_required
    def get(user):
        """ Update an user based on the sent information """
        repository = CashTransactionRepository()
        transactions = repository.get(user.id)
        return jsonify({"transactions": [transaction.json for transaction in transactions]})

    @staticmethod
    @parse_params(
        Argument("transaction_date", location="json", required=True),
        Argument("category", location="json", required=True),
        Argument("tag", location="json", required=True),
        Argument("description", location="json", required=True),
        Argument("amount", location="json", required=True),
        Argument("currency", location="json", required=True)
    )
    @auth_required
    def post(user, transaction_date, category, tag, description, currency, amount):
        """ Update an user based on the sent information """
        repository = CashTransactionRepository()
        try:
            formatted_trans_date = datetime.datetime.strptime(transaction_date, '%Y%m%d')
        except ValueError:
            raise FormatError({"code": "malformatted_date", "message": "invalid form of date"}, 400)
        new_tx = repository.create(
            user,
            transaction_date=formatted_trans_date,
            category=category,
            tag=tag,
            description=description,
            currency=currency,
            amount=amount
        )
        return jsonify({"transaction": new_tx.json})

    @staticmethod
    @parse_params(
        Argument("transaction_date", location="json"),
        Argument("category", location="json"),
        Argument("tag", location="json"),
        Argument("description", location="json"),
        Argument("amount", location="json")
    )
    @auth_required
    def put(user, transaction_id, **kwargs):
        """ Update transaction with user auth check """
        repository = CashTransactionRepository()
        updated_tx = repository.update(transaction_id, kwargs)
        return jsonify({"cash_transaction": updated_tx.json})
