from flask import Blueprint

api = Blueprint('api', __name__)

from . import test
from . import user_auth