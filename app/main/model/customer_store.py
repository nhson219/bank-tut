from .. import db, flask_bcrypt
import json

class CustomerStore(db.Model):
    __tablename__ = "customer_store"

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    CustomerStoreId = db.Column(db.Integer, db.ForeignKey('customer.CustomerId'))
    NameStore = db.Column(db.String(255))
    CreatedDate = db.Column(db.DateTime)
    

    customer = db.relationship("Customer", foreign_keys=[CustomerId]) 
    customer_store = db.relationship("Customer", foreign_keys=[CustomerStoreId]) 

    @property
    def serialize(self):
        return {
            "customer_id" : self.CustomerId,
            "customer_name": self.customer.CustomerName,
            "customer_store_id": self.customer_store.CustomerId,
            "customer_store_name": self.NameStore,
            "customer_store_number_payment": self.customer_store.payment_account.NumberPaymentAccount
        }