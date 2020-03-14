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

from sqlalchemy.orm import joinedload


     

def add_payment(data):
    #PaymentAccount.update().values(Amount=5).where(PaymentAccount.PaymentAccountId == Customer.PaymentAccount)
    # number_payment = data['number_payment_or_user_name']
    # username = data['number_payment_or_user_name']
    payment_account = PaymentAccount.query.filter_by(NumberPaymentAccount=data['number_payment_or_user_name']).first()
    user_account = UserAccount.query.filter_by(UserName=data['number_payment_or_user_name']).first()
    if payment_account:
        try:
            payment_account.Amount = payment_account.Amount + data['amount']
            db.session.commit()
            response_object = {
                'status' : 'success',
                'message': 'Success update amount'
            }
            return ResponseService().response('success', 200, data), 201
        except:
            db.session.rollback()
        finally:
            db.session.close()  
    elif user_account:
        
        customer = Customer.query.filter_by(UserAccountId=user_account.AccountId).first()
        if customer:
                payment_account = PaymentAccount.query.filter_by(PaymentAccountId=customer.PaymentAccount).first()
                
                if payment_account:
                    try:
                        payment_account.Amount = payment_account.Amount + data['amount']
                        db.session.commit()
                        response_object = {
                            'status' : 'success',
                            'message': 'Success update amount'
                        }
                        return ResponseService().response('success', 200, data), 201
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close()    
                else:
                    response_object = {
                    'status' : 'fail',
                    'message': 'Update amount fail. Please try again'
                    }
                    return response_object, 409              
        else:
           response_object = {
            'status' : 'fail',
            'message': 'Update amount fail. Please try again'
        }
        return response_object, 409                               
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Update amount fail. Please try again'
        }
        return response_object, 409                             
                
                