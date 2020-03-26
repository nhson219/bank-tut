from .. import db, flask_bcrypt

class PaymentHistory(db.Model):
    __tablename__ = "payment_history"

    ADD_AMOUNT = 1
    SEND_AMOUNT = 2

    PaymentHistoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    Type = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)


    customer = db.relationship("Customer")

    def convert_message(self, type):
        print(self.SEND_AMOUNT)
        msg = ""
        if (type == self.ADD_AMOUNT):
            msg = " has received amount"
        elif (type == self.SEND_AMOUNT):
            msg = " has send amount"   
        return msg   

    # @property
    # def __repr__(self):
    #     return "<PaymentAccount '{}'>".format(self.NumberPaymentAccount)

    @property
    def serialize(self):
        return {
            "customer_id" : self.CustomerId,
            "name": self.customer.CustomerName,
            "type" : PaymentHistory.convert_message(self, self.Type),
        }

          