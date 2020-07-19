from flask import Blueprint
from flask.json import jsonify
from .auth_error import AuthError
from .format_error import FormatError


ERROR_BLUEPRINT = Blueprint('errors', __name__)


@ERROR_BLUEPRINT.app_errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@ERROR_BLUEPRINT.app_errorhandler(FormatError)
def handle_format_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
