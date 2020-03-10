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
    customer_get = api.model('customer', {
        'CustomerName': fields.String(required=True, description='Customer name'),
        'CreatedDate': fields.DateTime(required=True, description='Customer created at'),
    })
    
    customer_update = api.model('customer', {
        'CustomerId': fields.Integer(required=True, description='customer id'),
        'CustomerName': fields.String(required=True, description='Customer name'),
    })
class CustomerAddDto:
    api = Namespace('customer', description='customer related operations')
    customer_add = api.model('customer', {
        'CustomerName': fields.String(required=True, description='Customer name'),
        'UserName': fields.String(required=True, description='Customer UserName'),
        'Nickname': fields.String(required=True, description='Customer nickname'),
    })