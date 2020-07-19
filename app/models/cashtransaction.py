"""
Define the Cash Transaction model
"""
import datetime

from .abc import BaseModel, MetaBaseModel
from . import db
from errors import FormatError

CURRENCY = ['SGD', 'USD', 'MYR']


class CashTransaction(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The cash transaction model """

    __tablename__ = "cash_transaction"
    to_json_filter = ["user", "user_id"]

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    category = db.Column(db.String(120))
    tag = db.Column(db.String(120))
    description = db.Column(db.String(300))
    currency = db.Column(db.String(3))
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='transactions', lazy=True)

    def __init__(
            self,
            transaction_date=datetime.date.today,
            category=None,
            tag=None,
            description=None,
            currency=CURRENCY[0],
            amount=None,
            user=None):
        """ Create a new transaction """
        self.transaction_date = datetime.date.today() if transaction_date is None else transaction_date
        self.category = category
        self.tag = tag
        self.description = description
        if currency in CURRENCY:
            self.currency = currency
        else:
            raise FormatError({"code": "malformatted_currency", "message": "invalid form of currency"})
        self.amount = amount
        self.user_id = user.id
