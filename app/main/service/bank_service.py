import uuid
import datetime
import uuid
import os

from app.main import db
from app.main.model.bank import Bank
from Crypto.PublicKey import RSA
from constants import ROOT_PATH
from sqlalchemy.orm import joinedload, aliased
from app.main.service.payment_history_service import add_payment_history
from app.main.model.customer import Customer
from app.main.model.payment_history import PaymentHistory
from app.main.service.response_service import ResponseService
from app.main.service.payment_transaction_service import PaymentTransactionService
from app.main.model.payment_transaction import PaymentTransaction

import base64
from app.main.model.payment_account import PaymentAccount
from flask import jsonify

def save_new_bank(data):
    RSAkey = RSA.generate(1024)
    getattr(RSAkey.key, 'n')


    bank = Bank.query.filter_by(Name=data['name']).first()
    if not bank:
        try:
            new_bank = Bank(
                BankId = str(uuid.uuid1()),
                Name = data['name'],
            )
            db.session.add(new_bank)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'data': {
                    'uuid': str(uuid.uuid1())
                }
            }
            return response_object, 201
        except Exception as e:
                raise
                db.session.rollback()
        finally:
                db.session.close()

    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def create_new_rsa():
    
    try:
        # RSAkey = RSA.generate(1024)
        key = RSA.generate(4096)

        # if not bank:
        os.mkdir(ROOT_PATH + "/key", 0o755)
        f = open(ROOT_PATH + '/key/public_key.pem', 'wb')
        f.write(key.publickey().exportKey('PEM'))
        f.close()
        f = open(ROOT_PATH + '/key/private_key.pem', 'wb')
        f.write(key.exportKey('PEM'))
        f.close()

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    except Exception as e:
            raise
            db.session.rollback()
    finally:
            db.session.close()



def create_transaction(data):
    try: 
        read_private_key = open(ROOT_PATH + "/key/private_key.pem", "rb")
        private_key = RSA.importKey(read_private_key.read())

        data_b64decode = base64.b64decode(bytes(data['uuid'], 'utf-8'))
        
        uuid = private_key.decrypt(data_b64decode)

        bank = Bank.query.filter_by(BankId=uuid).first()

        if bank:
            customer = Customer.query.join('payment_account').filter(PaymentAccount.NumberPaymentAccount==data['number_account']).first()
            if customer:
                customer.payment_account.Amount = data['amount']
                db.session.commit()


                # add payment transaction 
                tmp = PaymentTransactionService.save_payment_transaction(PaymentTransaction(
                    PaymentAccountId = customer.CustomerId,
                    PaymentAccountReceiveId = customer.CustomerId,
                    Amount = data['amount'],
                    Content = 'nap tien',
                    OtpCode = None,
                    SendOtpTime = datetime.utcnow().timestamp(),
                    Status = PaymentTransaction.STATUS_ACTIVE
                ))

                # add log history payment    
                add_payment_history(type=PaymentHistory.SEND_AMOUNT, customer_id=customer.CustomerId)

                response_object = {
                                'status' : 'success',
                                'message': 'Success confirm transaction'
                            }
                return ResponseService().response('success', 200, data), 201

            else:
                response_object = {
                    'status' : 'fail',
                    'message': 'Customer does not exist. Please try again'
                }
                return response_object, 409    
        else:
            response_object = {
                    'status' : 'fail',
                    'message': 'Bank does not exist. Please try again'
                }
            return response_object, 409                                

    except Exception as e:
        raise
        db.session.rollback()
    finally:
        db.session.close()

def convert_uuid(data):
    try:
        # read public key
        read_public_key = open(ROOT_PATH + "/key/public_key.pem", "rb")  

        # import public key
        public_key = RSA.importKey(read_public_key.read())

        # encrypt
        uuid_encrypt = public_key.encrypt(bytes(data['uuid'], 'utf-8'), 32)
        
        # base64 encode
        base64_uuid = base64.b64encode(uuid_encrypt[0])
        response_object = {
                        'status' : 'success',
                        'message': 'Success convert uuid base64',
                        'base64_uuid': base64_uuid.decode('utf-8')
                    }

        return ResponseService().response('success', 200, response_object), 201


    except Exception as e:
        raise        


def get_all_customer():
    try: 
        list_customer = db.session.query(Customer, PaymentAccount, Customer.CustomerName, PaymentAccount.NumberPaymentAccount).select_from(Customer).join(PaymentAccount).all()
        data = []
        for i in list_customer:
            tmp = {
                'customer': i[2],
                'number_payment': i[3]
            }
            data.append(tmp)
        return ResponseService().response('success', 200, data), 201
    except:
        return jsonify(data=[])



