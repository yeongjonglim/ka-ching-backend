"""
Define the User model
"""
import datetime
import jwt
import logging
from flask import current_app

from . import db
from . import BlacklistToken
from .abc import BaseModel, MetaBaseModel
from utils.errors import AuthError


class User(db.Model, BaseModel, metaclass=MetaBaseModel):
    """ The User model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    joined_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    first_name = db.Column(db.String(300))
    last_name = db.Column(db.String(300))

    def __init__(self,
                 email,
                 password_hash,
                 first_name,
                 last_name):
        """ Create a new User """
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.joined_datetime = datetime.datetime.utcnow()

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=5),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            logging.error(e)
            raise

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                raise AuthError({"code": "blacklisted_token",
                                 "description":
                                 "blacklisted token,"
                                 "please sign in again"}, 401)
            else:
                return User.query.filter_by(id=payload['sub']).first()
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token has expired"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_token",
                             "description":
                             "Unable to parse authentication token."}, 401)
