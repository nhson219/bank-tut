from .. import db, flask_bcrypt

class PaymentAccount(db.Model):
    __tablename__ = "payment_account"

    PaymentAccountId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NumberPaymentAccount = db.Column(db.String(255), index=True)
    Amount = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)

    db.Index('col_number_payment_account', 'payment_account.NumberPaymentAccount')
    #customer = db.relationship("Customer", back_populates="customer" );

    # @property
    # def __repr__(self):
    #     return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)