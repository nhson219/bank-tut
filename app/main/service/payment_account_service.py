import uuid
import datetime

from app.main import db
from app.main.model.user_account import UserAccount

class PaymentAccountService:
# def save_new_customer(data):
#     user_account = UserAccount.query.filter_by(UserName=data['UserName']).first()
#     if not user_account:
#         new_customer = Customer(
#             CustomerName = data['CustomerName'],
#         )
#         save_changes(new_customer)
#         response_object = {
#             'status' : 'success',
#             'message': 'Success create customer'
#         }
#         return response_object, 201
#     else:
#         response_object = {
#             'status' : 'fail',
#             'message': 'Customer already exists. Please login'
#         }
#         return response_object, 409

# def get_all_customer():
#     return Customer.query.all()

    def get_customer(id):
        return UserAccount.query.filter_by(id=id).first()

    def save_changes(data):
        db.session.add(data)
        db.session.commit()
