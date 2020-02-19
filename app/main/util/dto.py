from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class CustomerDto:
    api = Namespace('customer', description='customer related operations')
    customer = api.model('customer', {
        'CustomerName': fields.String(required=True, description='Customer name'),
        'UserName': fields.String(required=True, description='Customer UserName'),
        'Password': fields.String(required=True, description='Customer Password'),
    })    