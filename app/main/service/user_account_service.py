import uuid
import datetime

from app.main import db
from app.main.model.user_account import UserAccount

class UserAccountService:
    def save_user_account(data):
        try: 
            db.session.add(data)
            db.session.flush()
            db.session.commit()
            return data.AccountId
        except:
            db.session.rollback()
        finally:
            db.session.close()

# def get_all_customer():
#     return Customer.query.all()

    def get_customer(id):
        return UserAccount.query.filter_by(id=id).first()

    def save_changes(data):
        db.session.add(data)
        db.session.commit()
