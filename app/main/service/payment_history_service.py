import uuid
import datetime

from app.main import db
from app.main.model.payment_history import PaymentHistory
from sqlalchemy.orm import joinedload, aliased
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from flask import jsonify
from sqlalchemy import case, literal_column, func


def add_payment_history(**data):
    try:
        db.session.add(PaymentHistory(
                Type=data['type'],
                CustomerId=data['customer_id']
            )
        )
        db.session.commit()
    except:
        raise
        db.session.rollback()
    return True    
        

