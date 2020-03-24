import uuid
import datetime

from app.main import db
from app.main.model.payment_account import PaymentAccount

class PaymentAccountService:
    def save_payment_account(data):
        try: 
            db.session.add(data)
            print(db.session.all())
            #db.session.flush()
            db.session.commit()
            return data.PaymentAccountId
        except Exception as e:
            db.session.rollback()
        # finally:
        #     db.session.close()

# def get_all_customer():
#     return Customer.query.all()

    def get_customer(id):
        return PaymentAccount.query.filter_by(id=id).first()

    def save_changes(data):
        db.session.add(data)
        db.session.commit()
