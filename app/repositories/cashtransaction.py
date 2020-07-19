""" Defines the Cash Transaction repository """
from models import db, CashTransaction

from errors import AuthError


class CashTransactionRepository:
    """ The repository for the user model """

    @staticmethod
    def get_transaction(id):
        """ Get specific transaction """
        return CashTransaction.query.filter_by(id=id).first()

    @staticmethod
    def get(user_id):
        """ Query all transactions for specific user id """
        return CashTransaction.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(user, **kwargs):
        """ Query all transactions for specific user id """
        cashtx = CashTransaction(user=user, **kwargs)
        return cashtx.save()

    def update(self, user, transaction_id, **kwargs):
        """ Update single transaction for all given keyword arguments """
        tx = self.get_transaction(transaction_id)
        if tx.user_id == user.id:
            CashTransaction.query.filter_by(id=transaction_id).update(kwargs)
            db.session.commit()
            return CashTransaction.query.filter_by(id=transaction_id).first()

        raise AuthError({"code": "unauthorised", "message": "unable to find transaction"}, 401)
