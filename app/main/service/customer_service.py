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
from flask import jsonify
from sqlalchemy.orm import joinedload
from random import randint

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
                Amount = 0, # init amount = 0,
                NumberPaymentAccount = randint(1000000000, 9999999999)
            ))
            
            if user_account_id and payment_account_id:
                new_customer = Customer(
                    CustomerName = data['customername'],
                    UserAccountId = user_account_id,
                    PaymentAccount = payment_account_id,
                    Nickname = data['nickname'],
                    Phone = data['phone'],
                    Email = data['email'],
                    Address = data['address'],
                    Gender = data['gender']
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
            customer.Address = data['address']
            customer.Email = data['email']
            customer.Gender = data['gender']

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
    list_customer = Customer.query.options(joinedload('user_account'))
    return jsonify(data=[i.serialize for i in list_customer])
    #return ResponseService().response('success', 200, jsonify(json_list=[i.serialize for i in list_customer])), 201
    # return Customer.query.all()

def get_customer(id):
    customer = Customer.query.filter_by(CustomerId=id).options(joinedload('user_account')).first()
    data = {
        'name' : customer.CustomerName,
        'phone': customer.Phone,
        'email': customer.Email,
        'id' : customer.CustomerId,
        'address': customer.Address,
        'gender' : customer.Gender,
        'nickname' : customer.Nickname,
        'username' : customer.user_account.UserName,
        'amount' : customer.payment_account.Amount,
        'number_payment': customer.payment_account.NumberPaymentAccount,
    }
    return ResponseService().response('success', 200, data), 201
    # return Customer.query.filter_by(CustomerId=id).first()

def get_customer_by_number_payment(number_payment):
    payment_account = PaymentAccount.query.filter_by(NumberPaymentAccount=number_payment).first()
    if payment_account:
        customer = Customer.query.filter_by(PaymentAccount=payment_account.PaymentAccountId).options(joinedload('payment_account')).first()
        data = {
            'name' : customer.CustomerName,
            'number_payment': customer.payment_account.NumberPaymentAccount,
            'customer_id': customer.CustomerId,
            'amount': customer.payment_account.Amount,
            'nick_name': customer.Nickname
        }
        return ResponseService().response('success', 200, data), 201
    else: 
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409      

def save_changes(data):
    db.session.add(data)
    db.session.commit()    
    return data

