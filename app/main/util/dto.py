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
    customer_add = api.model('customer', {
        'customername': fields.String(required=True, description='Customer name'),
        'username': fields.String(required=True, description='Customer UserName'),
        'nickname': fields.String(required=True, description='Customer nickname'),
        'phone': fields.String(required=True, description='Customer nickname'),
        'email': fields.String(required=True, description='Customer nickname'),
    })
    customer_update = api.model('customer', {
        'customerid': fields.Integer(required=True, description='customer id'),
        'customername': fields.String(required=True, description='Customer name'),
    })     
