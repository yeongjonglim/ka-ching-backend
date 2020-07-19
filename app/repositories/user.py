""" Defines the User repository """
import logging
import bcrypt
from models import User, BlacklistToken

from errors import AuthError


class UserRepository:
    """ The repository for the user model """

    @staticmethod
    def get(id):
        """ Query a user by last and first name """
        return User.query.filter_by(id=id).first()

    def reset_password(self, id, new_password):
        """ Reset a user password """
        user = self.get(id)
        salt = bcrypt.gensalt(rounds=4)
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        user.password_hash = password_hash

        return user.save()

    @staticmethod
    def create(email, password, first_name, last_name):
        """ Create a new user """
        salt = bcrypt.gensalt(rounds=4)
        encoded_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        decoded_hash = encoded_hash.decode('utf-8')
        user = User(
            email=email,
            password_hash=decoded_hash,
            last_name=last_name,
            first_name=first_name
        )

        user = user.save()
        auth_token = user.encode_auth_token()

        return auth_token

    @staticmethod
    def login(email, password):
        """ Login a user by email and password validation, return token on success """
        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user.encode_auth_token()
        raise AuthError({"code": "invalid_credentials",
                         "message": "invalid credentials"}, 401)

    @staticmethod
    def logout(auth_token):
        """ Blacklist auth_token and return None on success """
        user = User.decode_auth_token(auth_token)
        if user:
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                blacklist_token.save()
                return None
            except Exception as e:
                logging.error(e)
                raise
        else:
            raise AuthError({"code": "invalid_user",
                             "message": "unable to find user"}, 401)
