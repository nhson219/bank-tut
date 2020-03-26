from flask import request
from flask_restplus import Resource, fields

from ..util.dto import PaymentDto
from ..service.payment_service import add_payment, create_transaction, confirm_transaction, get_payment_history_customer

api = PaymentDto.api
payment_add = PaymentDto.payment_add
@api.route('/<int:customer_id>')
class Payment(Resource):

    @api.response(201, 'add payment success')
    @api.doc('add payment')
    @api.expect(payment_add, validate=True)
    def post(self):
        data = request.json
        return add_payment(data=data)    

    @api.doc('list_of_register_customer')
    @api.param('customer_id', 'The Customer identifier')
    #@api.marshal_list_with(_customer_get, envelope='data')
    def get(self, customer_id):
        return get_payment_history_customer(customer_id)                  
  
@api.route('/transaction')
class PaymentTransaction(Resource):
    
    @api.doc('create customer')
    @api.expect(payment_add)
    def post(self):
        data = request.json
        return create_transaction(data=data)

@api.route('/transaction_confirm')
class PaymentTransactionConfirm(Resource):
    
    @api.doc('confirm transaction')
    @api.expect(payment_add)
    def post(self):
        data = request.json
        return confirm_transaction(data=data)        