from .. import db, flask_bcrypt
import json


class Bank(db.Model):
    __tablename__ = "bank"

    BankId = db.Column(db.String(255), primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255))
    CreatedDate = db.Column(db.DateTime)
    LastConnect = db.Column(db.DateTime)


