from flask import request
from flask_restplus import Resource, fields

from ..util.dto import CustomerDto
from ..service.customer_service import save_new_customer, get_all_customer, get_customer, update_customer, get_customer_by_number_payment
from ..service.customer_store_service import get_customer_store_by_customer_id, save_new_customer_store

api = CustomerDto.api
_customer_get = CustomerDto.customer_get
_customer_add = CustomerAddDto.customer_add
_customer_update = CustomerDto.customer_update

@api.route('/')
class CustomerList(Resource):
    @api.doc('list_of_register_customer')
    # @api.marshal_list_with(_customer_get, envelope='data')
    def get(self):
        return get_all_customer()

    

    @api.response(201, 'customer successfully created')
    @api.doc('create customer')
    @api.expect(_customer_add, validate=True)
    def post(self):
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
class CustomerInfo(Resource):
    @api.response(404, 'Customer not found.')
    @api.doc('get a Customer')
    # @api.marshal_with(_customer_get)
    def get(self, customer_id):
        return get_customer(customer_id)        

@api.route('/number_payment/<int:number_payment>')
@api.param('number_payment', 'number_payment')
class CustomerPayment(Resource):
    @api.response(404, 'Customer not found.')
    @api.doc('get a Customer payment')
    # @api.marshal_with(_customer_get)
    def get(self, number_payment):
        return get_customer_by_number_payment(number_payment)   

@api.route('/customer_store/<int:customer_id>')
@api.param('customer_id', 'customer_id')
class CustomerStoreInfo(Resource):        
    @api.response(404, 'Customer not found.')
    @api.doc('get a Customer store')
    # @api.marshal_with(_customer_get)
    def get(self, customer_id):
        return get_customer_store_by_customer_id(customer_id)  

@api.route('/customer_store/')
class CustomerStore(Resource):        
    @api.response(404, 'Customer not found.')
    @api.doc('save a Customer store')
    #@api.marshal_with(_customer_store_add)
    @api.response(201, 'customer store successfully created')    
    @api.doc('create customer store')
    @api.expect(_customer_add)
    def post(self):
        data = request.json
        return save_new_customer_store(data=data)                    
  

  