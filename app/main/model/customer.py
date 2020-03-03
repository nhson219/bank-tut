from .. import db, flask_bcrypt
import json

class Customer(db.Model):
    __tablename__ = "customer"

    CustomerId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(255))
    CreatedDate = db.Column(db.DateTime)
    CreatedBy = db.Column(db.Integer)
    UserAccountId = db.Column(db.Integer, db.ForeignKey('user_accounts.AccountId'))
    PaymentAccount = db.Column(db.Integer, db.ForeignKey('payment_account.PaymentAccountId'))
    Nickname = db.Column(db.String(255))
    Phone = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    Gender = db.Column(db.Integer, default=0)

    user_account = db.relationship('UserAccount',
        backref=db.backref('customer', lazy=True))

    payment_account = db.relationship('PaymentAccount',
        backref=db.backref('customer', lazy=True))        

    # @property
    # def __repr__(self):
    #     return "<Customer '{}'>".format(self.CustomerName)