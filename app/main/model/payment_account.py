from .. import db, flask_bcrypt

class PaymentAccount(db.Model):
    __tablename__ = "payment_account"

    PaymentAccountId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NumberPaymentAccount = db.Column(db.Integer)
    Amount = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)

    @property
    def __repr__(self):
        return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)