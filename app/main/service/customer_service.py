import uuid
import datetime

from app.main import db
from app.main.model.customer import Customer
from app.main.model.user_account import UserAccount
from app.main.model.payment_account import PaymentAccount
from app.main.service.user_account_service import UserAccountService
from app.main.service.payment_account_service import PaymentAccountService
from app.main.service.response_service import ResponseService
import json

def save_new_customer(data):
    user_account = UserAccount.query.filter_by(UserName=data['username']).first()
    if not user_account:
        try: 
            password = '123456'
            user_account_id = UserAccountService.save_user_account(UserAccount(
                UserName = data['username'],
                password = password
            ))

            payment_account_id = PaymentAccountService.save_payment_account(PaymentAccount(
                Amount = 0 # init amount = 0
            ))
            
            if user_account_id and payment_account_id:
                new_customer = Customer(
                    CustomerName = data['customername'],
                    UserAccountId = user_account_id,
                    PaymentAccount = payment_account_id,
                    Nickname = data['nickname'],
                    Phone = data['phone'],
                    Email = data['email'],
                )
                save_changes(new_customer)
                # response_object = {
                #     'status' : 'success',
                #     'message': 'Success create customer'
                # }
                return ResponseService().response('success', 200, data), 201
        except:
            db.session.rollback()

        finally:
            db.session.close()  
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Customer already exists. Please login'
        }
        return response_object, 409

def update_customer(data):
    customer = Customer.query.filter_by(CustomerId=data['id']).first()
    if customer:
        try: 
            customer.CustomerName = data['customername']
            customer.Nickname = data['nickname']
            customer.Phone = data['phone']

            db.session.commit()
            response_object = {
                'status' : 'success',
                'message': 'Success update customer'
            }
            return ResponseService().response('success', 200, data), 201
            # return response_object, 201
        except:
            db.session.rollback()

        finally:
            db.session.close()  
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409        
        
   

def get_all_customer():
    list_customer = Customer.query.all()
    return ResponseService().response('success', 200, list_customer), 201
    # return Customer.query.all()

def get_customer(id):
    customer = Customer.query.filter_by(CustomerId=id).first()
    data = {
        'name' : customer.CustomerName,
        'phone': customer.Phone,
        'email': customer.Email
    }
    return ResponseService().response('success', 200, data), 201
    # return Customer.query.filter_by(CustomerId=id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()    

