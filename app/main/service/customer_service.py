import uuid
import datetime

from app.main import db
from app.main.model.customer import Customer
from app.main.model.user_account import UserAccount
from app.main.service.user_account_service import UserAccountService

def save_new_customer(data):
    user_account = UserAccount.query.filter_by(UserName=data['UserName']).first()
    if not user_account:
        new_customer = Customer(
            CustomerName = data['CustomerName'],
        )
        save_changes(new_customer)
        UserAccountService.save_changes(UserAccount(
            UserName = data['UserName'],
            Password = data['Password']
        ))
        response_object = {
            'status' : 'success',
            'message': 'Success create customer'
        }
        return response_object, 201
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Customer already exists. Please login'
        }
        return response_object, 409

def get_all_customer():
    return Customer.query.all()

def get_customer(id):
    return Customer.query.filter_by(id=id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()    
    
