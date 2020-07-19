"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api

from resources import CashTransactionResource

CASHTRANSACTION_BLUEPRINT = Blueprint("transactions", __name__)
Api(CASHTRANSACTION_BLUEPRINT).add_resource(
    CashTransactionResource, "/transactions"
)
