from .. import db, flask_bcrypt

class PaymentTransaction(db.Model):
    __tablename__ = "payment_transaction"

    PaymentTransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PaymentAccountId = db.Column(db.Integer, db.ForeignKey('payment_account.PaymentAccountId'))
    OtpCode = db.Column(db.Integer) 
    Amount = db.Column(db.Integer)
    Content = db.Column(db.Text)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)

    # @property
    # def __repr__(self):
    #     return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)