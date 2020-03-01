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
        'Nickname': fields.String(required=True, description='Customer nickname'),
        'Email': fields.String(required=True, description='Customer email'),
        'Phone': fields.String(required=True, description='Customer phone'),
        'CreatedDate': fields.DateTime(required=True, description='Customer created at'),
    })
    customer_add = api.model('customer', {
        'customername': fields.String(required=True, description='Customer name'),
        'username': fields.String(required=True, description='Customer UserName'),
        'nickname': fields.String(required=True, description='Customer nickname'),
        'phone': fields.String(required=True, description='Customer phone'),
        'email': fields.String(required=True, description='Customer email'),
    })
    customer_update = api.model('customer', {
        'id': fields.Integer(required=True, description='customer id'),
        'customername': fields.String(required=True, description='Customer name'),
        'nickname': fields.String(required=True, description='Customer nickname'),
        'phone': fields.String(required=True, description='Customer phone'),
    })     
