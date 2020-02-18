from flask import request
from flask_restplus import Resource

from ..util.dto import CustomerDto
from ..service.customer_service import save_new_customer, get_all_customer, get_customer

api = CustomerDto.api
_customer = CustomerDto.customer

@api.route('/')
class CustomerList(Resource):
    @api.doc('list_of_register_customer')
    @api.marshal_list_with(_customer, envelope='data')
    def get(self):
        return get_all_customer()

    @api.response(201, 'customer successfully created')    
    @api.doc('create customer')
    @api.expect(_customer, validate=True)
    def post(self):
        data = request.json
        return save_new_customer(data=data)
