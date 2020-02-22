from flask import request
from flask_restplus import Resource

from ..util.dto import CustomerDto
from ..service.customer_service import save_new_customer, get_all_customer, get_customer, update_customer

api = CustomerDto.api
_customer_get_info = CustomerDto.customer_get_info
_customer_get = CustomerDto.customer_get
_customer = CustomerDto.customer
_customer_update = CustomerDto.customer_update

@api.route('/')
class CustomerList(Resource):
    @api.doc('list_of_register_customer')
    @api.marshal_list_with(_customer_get, envelope='data')
    def get(self):
        return get_all_customer()

    @api.doc('get info customer')
    @api.expect(_customer_get_info, validate=True)
    # @api.marshal_list_with(_customer_get_info, envelope='data')
    def get_info(self):
        data = request.json
        return get_customer(data['CustomerId'])        

    @api.response(201, 'customer successfully created')    
    @api.doc('create customer')
    @api.expect(_customer, validate=True)
    def post(self):
        data = request.json
        return save_new_customer(data=data)


    @api.response(201, 'customer successfully updated')    
    @api.doc('updated customer')
    @api.expect(_customer_update, validate=True)
    def patch(self):
        data = request.json
        return update_customer(data=data)