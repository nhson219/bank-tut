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
import json
from flask import jsonify
from sqlalchemy.orm import joinedload
from random import randint

def save_new_customer_store(data):
    if data['customer_id'] != data['customer_store_id']:
        customer = Customer.query.filter_by(CustomerId=data['customer_id']).first()
        customer_store = Customer.query.filter_by(CustomerId=data['customer_store_id']).first()
        customer_store_current = CustomerStore.query.filter_by(CustomerId=data['customer_id'], CustomerStoreId=data['customer_store_id']).first()
        if (customer and customer_store):
            if not customer_store_current:
                try: 
                    new_customer_store = CustomerStore(
                        CustomerId= data['customer_id'],
                        CustomerStoreId= data['customer_store_id'],
                        NameStore=data['name_store']
                    )
                    save_changes(new_customer_store)
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
                customer_store_current.NameStore = data['name_store']
                try:
                    db.session.commit()
                    response_object = {
                        'status' : 'success',
                        'message': 'Success update customer store'
                    }
                    return ResponseService().response('success', 200, data), 201
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
    else:
        response_object = {
                'status' : 'fail',
                'message': 'Fail, please try again'
        }
        return response_object, 409                      

def save_changes(data):
    db.session.add(data)
    db.session.commit()    


def get_customer_store_by_customer_id(customer_id):
    customer_store = CustomerStore.query.filter_by(CustomerId=customer_id).all()
    #customer = Customer.query.filter_by(CustomerId=customer_id).first()
    #print(customer_store[1].customer_store.CustomerName)
    if customer_store:
        return jsonify(data=[i.serialize for i in customer_store])   
    else:
        response_object = {
                'status' : 'success',
                'message': 'No data'
        }
        return response_object, 404         

