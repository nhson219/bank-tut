from .. import db, flask_bcrypt

class PaymentHistory(db.Model):
    __tablename__ = "payment_history"

    PaymentHistoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    Type = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)

    # @property
    # def __repr__(self):
    #     return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)