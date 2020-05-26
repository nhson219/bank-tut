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
    Role = db.Column(db.JSON)

    user_account = db.relationship('UserAccount',
        backref=db.backref('customer', lazy=True))

    payment_account = db.relationship('PaymentAccount',
        backref=db.backref('customer', lazy=True))     

    payment_history = db.relationship("PaymentHistory")        

    #customer_store = db.relationship("CustomerStore", backref="customer")           

    # @property
    # def __repr__(self):
    #     return "<Customer '{}'>".format(self.CustomerName)


    

    @property
    def serialize(self):
        return {
            "id" : self.CustomerId,
            "name" : self.CustomerName,
            "nickname" : self.Nickname,
            "phone" : self.Phone,
            "email" : self.Email,
            "address" : self.Address,
            "gender" : self.Gender,
            'amount' : self.payment_account.Amount,
            'number_payment' : self.payment_account.NumberPaymentAccount,
            'user_name': self.user_account.UserName,
            'role': self.Role,
        }