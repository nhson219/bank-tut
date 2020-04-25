from .. import db, flask_bcrypt
import json


class Bank(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "bank"

    BankId = db.Column(db.String(255), primary_key=True, autoincrement=False)
    Name = db.Column(db.String(255))
    CreatedDate = db.Column(db.DateTime)
    LastConnect = db.Column(db.DateTime)
    Status = db.Column(db.Integer)


