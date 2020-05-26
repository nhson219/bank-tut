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
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, lazyload, subqueryload, raiseload
from random import randint
import jwt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


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
                role = {
                    "customer": 'customer' in data['role'] and data['role']['customer'] or False,
                    'employee': 'employee' in data['role'] and data['role']['employee'] or False,
                    'admin': 'admin' in data['role'] and data['role']['admin'] or False,
                    'any': True
                }
                new_customer = Customer(
                    CustomerName = data['customername'],
                    UserAccountId = user_account_id,
                    PaymentAccount = payment_account_id,
                    Nickname = data['nickname'],
                    Phone = data['phone'],
                    Email = data['email'],
                    Address = data['address'],
                    Gender = data["gender"],
                    Role = json.JSONEncoder().encode(role)
                )
                save_changes(new_customer)
                # response_object = {
                #     'status' : 'success',
                #     'message': 'Success create customer'
                # }
                return ResponseService().response('success', 200, data), 201
            else: 
                response_object = {
                    'status' : 'fail',
                    'message': 'Create payment_account and user_account fail. Please try again'
                }
                return response_object, 409    
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
            role = {
                "customer": 'customer' in data['role'] and data['role']['customer'] or False,
                'employee': 'employee' in data['role'] and data['role']['employee'] or False,
                'admin': 'admin' in data['role'] and data['role']['admin'] or False,
                'any': True
            }


            customer.CustomerName = "customername" in data and data["customername"] or customer.CustomerName
            customer.Nickname = "nickname" in data and data["nickname"] or customer.Nickname
            customer.Phone = "phone" in data and data['phone'] or customer.Phone
            customer.Address = "address" in data and data['address'] or customer.Address
            customer.Email = "email" in data and data['email'] or customer.Email
            customer.Gender = "gender" in data and data['gender'] or customer.Gender
            customer.Role = json.JSONEncoder().encode(role)

            db.session.commit()
            response_object = {
                'status' : 'success',
                'message': 'Success update customer'
            }
            return ResponseService().response('success', 200, data), 201
            # return response_object, 201
        except Exception as e:
            #raise
            db.session.rollback()
        finally:
            db.session.close()  
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409        
        
   

def get_all_customer(data):
    data = data.args

    try: 
        if data:
            if "phone" in data and "customer_name" in data:
                condition = or_("phone" in data and Customer.Phone==data['phone'], "customer_name" in data and Customer.CustomerName==data['customer_name'])
            elif "customer_name" in data:
                condition = Customer.CustomerName==data['customer_name']
            elif "phone" in data:            
                condition = Customer.Phone==data['phone']

            list_customer = Customer.query.options(joinedload('user_account')).filter(condition)
        else:
            list_customer = Customer.query.options(joinedload('user_account'))                        

        return jsonify(data=[i.serialize for i in list_customer])
    except:
        return jsonify(data=[])

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
        customer = Customer.query.filter_by(PaymentAccount=payment_account.PaymentAccountId).options(joinedload('payment_account')).options(joinedload('user_account')).first()
        data = {
            'name' : customer.CustomerName,
            'number_payment': customer.payment_account.NumberPaymentAccount,
            'customer_id': customer.CustomerId,
            'amount': customer.payment_account.Amount,
            'nick_name': customer.Nickname,
            'email': customer.Email,
            'phone': customer.Phone,
            'username': customer.user_account.UserName
        }
        return ResponseService().response('success', 200, data), 201
    else: 
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409      

def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()    
        return data
    except:
        db.session.rollback()
    finally:
        db.session.close()       

def change_password(data):
    customer = Customer.query.filter_by(CustomerId=data['customer_id']).first()


    if 'customer_id' not in data or 'password' not in data or 'new_password' not in data:
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409   

    if customer:
        if customer.user_account.check_password(data['password']):

            try: 
                customer.user_account.password = data['new_password']
                db.session.commit()    
                response_object = {
                    'status' : 'success',
                    'message': 'Success update customer'
                }
                del data['password']
                del data['new_password']
                return ResponseService().response('success', 200, data), 201
                # return response_object, 201
            except Exception as e:
                raise
                db.session.rollback()
            finally:
                db.session.close()
        else:
            response_object = {
                'status' : 'fail',
                'message': 'Old password does not match. Please try again'
            }
            return response_object, 409
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Customer not exists. Please try again'
        }
        return response_object, 409        

def login(data):             
    # customer = Customer.query.options(joinedload('user_account'))\
    #     .filter(or_(Customer.Email == data['email_or_username'], Customer.user_account==data['email_or_username'])).first()

    customer = Customer.query.join('user_account')\
                .filter(or_(Customer.Email == data['email_or_username'], UserAccount.UserName==data['email_or_username'])).first()

    # auth_token = encode_auth_token(customer.CustomerId)
    access_token = create_access_token(identity=data['email_or_username'])
    refresh_token = create_refresh_token(identity=data['email_or_username'])
    # current_user = get_jwt_identity()

    # print(current_user)

    if customer:
        if customer.user_account.check_password(data['password']):
            response_object = {
                'status' : 'success',
                'message': 'Success login customer',
                'email_or_username': data['email_or_username'],
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return ResponseService().response('success', 200, response_object), 201
        else:
            response_object = {
                'status' : 'fail',
                'message': 'Password does not match. Please try again'
            }
            return response_object, 409    
    else:
            response_object = {
                'status' : 'fail',
                'message': 'Customer does not exist. Please try again'
            }
            return response_object, 409            
    #


def encode_auth_token(customer_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': customer_id
            }
            return jwt.encode(
                payload,
                '123456@L', # key private
                algorithm='HS256'
            )
        except Exception as e:
            return e    
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, '123456@L')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'  

def get_profile_customer(customer_name):
    customer = Customer.query.filter(UserAccount.UserName==customer_name).join(Customer.user_account).options(subqueryload(Customer.user_account)).first()
    if customer:
        data = {
                'name' : customer.CustomerName,
                'number_payment': customer.payment_account.NumberPaymentAccount,
                'customer_id': customer.CustomerId,
                # 'amount': customer.payment_account.Amount,
                'nick_name': customer.Nickname,
                'email': customer.Email,
                'phone': customer.Phone,
                'username': customer.user_account.UserName,
                'role': customer.Role is not None and json.JSONDecoder().decode(customer.Role) or ''
            }     

        return ResponseService().response('success', 200, data), 200 
    else:
        response_object = {
                'status' : 'fail',
                'message': 'Customer does not exist. Please try again'
            }
        return response_object, 409        




