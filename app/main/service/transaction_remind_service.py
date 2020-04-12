import uuid
import datetime

from app.main import db
from app.main.model.customer import Customer
from app.main.model.user_account import UserAccount
from app.main.model.payment_account import PaymentAccount
from app.main.service.user_account_service import UserAccountService
from app.main.service.payment_account_service import PaymentAccountService
from app.main.model.customer_store import CustomerStore
from app.main.service.response_service import ResponseService
from app.main.service.payment_transaction_service import PaymentTransactionService
from app.main.model.payment_transaction import PaymentTransaction
from app.main.model.payment_history import PaymentHistory
from sqlalchemy.orm import joinedload, aliased
from datetime import datetime
from flask import jsonify
from sqlalchemy import case, literal_column, func, or_, text
from app.main.service.payment_history_service import add_payment_history
from app.main.model.transaction_remind import TransactionRemind

def create_transaction_remind(data):
    customer = Customer.query.join("payment_account").filter(PaymentAccount.NumberPaymentAccount==data['number_payment']).first()
    customer_receive = Customer.query.join("payment_account").filter(PaymentAccount.NumberPaymentAccount==data['number_payment_remind']).first()                                         

    if customer and customer_receive:
        # if data['amount'] < customer.payment_account.Amount and data['amount'] > 0:

            # print(customer.PaymentAccount)
            # print(customer_receive.PaymentAccount)
            # create payment transaction here
            # otpCode = PaymentTransactionService.generate_otp_code()
        try:
            tmp = TransactionRemind(
                PaymentAccountId = data['number_payment'],
                PaymentAccountRemindId = data['number_payment_remind'],
                Amount = data['amount'],
                Content = data['content'],
                Status = TransactionRemind.STATUS_CREATED
            )
            
            db.session.add(tmp)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  

        response_object = {
                        'status' : 'success',
                        'message': 'Success create transaction'
                    }
        return ResponseService().response('success', 200, data), 201   
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Number payment not exist. Please try again'
        }
        return response_object, 409

def update_transaction_remind(data):
    transaction_remind = TransactionRemind.query.filter_by(TransactionRemindId=data['transaction_remind_id']).first()

    if transaction_remind:

        try:
            transaction_remind.Status = TransactionRemind.STATUS_DELETED
            transaction_remind.Content = "content" in data and data['content'] or transaction_remind.Content

            db.session.commit()
            response_object = {
                'status' : 'success',
                'message': 'Success update customer'
            }
            return ResponseService().response('success', 200, data), 201
        except Exception as e:
            #raise
            db.session.rollback()
        finally:
            db.session.close()
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Transaction remind not exist. Please try again'
        }
        return response_object, 409              

def get_transaction_remind(request):
    args = request.args

    if ("number_payment" in args or "number_payment_receive" in args) and "status" in args:
        arg_number_payment = "number_payment" in args and args['number_payment'] or ''
        arg_number_payment_receive = "number_payment_receive" in args and args['number_payment_receive'] or ''
        list_transaction_remind = TransactionRemind.query\
            .filter(or_(\
                TransactionRemind.PaymentAccountId== arg_number_payment,\
                TransactionRemind.PaymentAccountRemindId== arg_number_payment_receive\
            ))\
            .filter(TransactionRemind.Status==args['status'])\
            .all()
        return jsonify(data=[i.serialize for i in list_transaction_remind])  
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Transaction remind not exist. Please try again'
        }
        return response_object, 409    