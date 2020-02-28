from .. import db, flask_bcrypt

class Customer(db.Model):
    __tablename__ = "customer"

    CustomerId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(255))
    CreatedDate = db.Column(db.DateTime)
    CreatedBy = db.Column(db.Integer)
    UserAccountId = db.Column(db.Integer)
    PaymentAccount = db.Column(db.Integer)
    Nickname = db.Column(db.String(255))
    Phone = db.Column(db.String(255))
    Email = db.Column(db.String(255))

    @property
    def __repr__(self):
        return "<Customer '{}'>".format(self.CustomerName)