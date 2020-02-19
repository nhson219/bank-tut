# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.customer_controller import api as customer_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Internet banking project',
          version='1.0',
          description='internet banking project'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(customer_ns, path='/customer')