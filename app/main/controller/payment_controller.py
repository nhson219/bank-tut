from flask import request
from flask_restplus import Resource, fields

from ..util.dto import PaymentDto
from ..service.payment_service import add_payment, create_transaction

api = PaymentDto.api
payment_add = PaymentDto.payment_add
@api.route('/')
class Payment(Resource):

    @api.response(201, 'add payment success')
    @api.doc('add payment')
    @api.expect(payment_add, validate=True)
    def post(self):
        data = request.json
        return add_payment(data=data)               
  

    @api.response(201, 'create transaction')
    @api.doc('create customer')
    @api.expect(_customer_add, validate=True)
    def post(self):
        data = request.json
        return create_transaction(data=data)