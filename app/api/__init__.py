from flask import Blueprint



api = Blueprint('api', __name__)
# import shopping_list
# import user
# from . import shopping_list
# from . import user

from app.api import shopping_list
from app.api import user
from app.api import category


