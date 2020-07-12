"""
Defines the blueprint for the users
"""
from flask import Blueprint

HELLO_BLUEPRINT = Blueprint("hello", __name__)


@HELLO_BLUEPRINT.route('/', methods=['GET'])
def home():
    return '''<h1>Hello World!</h1>'''
