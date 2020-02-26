from flask import request
from flask_restplus import Resource

from ..util.dto import CustomerDto
from ..service.customer_service import save_new_customer, get_all_customer, get_customer, update_customer

api = CustomerDto.api
_customer_get = CustomerDto.customer_get
_customer_add = CustomerDto.customer_add
_customer_update = CustomerDto.customer_update

@api.route('/')
class CustomerList(Resource):
    @api.doc('list_of_register_customer')
    @api.marshal_list_with(_customer_get, envelope='data')
    def get(self):
        return get_all_customer()

    

    @api.response(201, 'customer successfully created')    
    @api.doc('create customer')
    @api.expect(_customer_add, validate=True)
    def post(self):
        print(_customer_add)
        data = request.json
        return save_new_customer(data=data)


    @api.response(201, 'customer successfully updated')    
    @api.doc('updated customer')
    @api.expect(_customer_update, validate=True)
    def patch(self):
        data = request.json
        return update_customer(data=data)


@api.route('/<int:customer_id>')
@api.param('customer_id', 'The Customer identifier')
@api.response(404, 'Customer not found.')
class User(Resource):
    @api.doc('get a Customer')
    @api.marshal_with(_customer_get)
    def get(self, customer_id):
        data = request.json
        return get_customer(customer_id)        
  