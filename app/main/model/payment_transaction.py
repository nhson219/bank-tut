from .. import db, flask_bcrypt

class PaymentTransaction(db.Model):
    __tablename__ = "payment_transaction"

    PaymentTransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PaymentAccountId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    PaymentAccountReceiveId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    OtpCode = db.Column(db.Integer) 
    Amount = db.Column(db.Integer)
    Content = db.Column(db.Text)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    Status = db.Column(db.Integer)
    SendOtpTime = db.Column(db.Integer)

    TIME_EXPIRE_OTP = 120
    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1

    # @property
    # def __repr__(self):
    #     return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)