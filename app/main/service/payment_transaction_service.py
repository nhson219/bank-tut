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
from random import randint

class PaymentTransactionService:
    def save_payment_transaction(data):
        try: 
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return data.PaymentTransactionID
        except:
            db.session.rollback()
        # finally:
            #db.session.close()

    def generate_otp_code():
        return randint(1000, 9999)