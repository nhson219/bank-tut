import uuid
import datetime
import uuid
import os

from app.main import db
from app.main.model.bank import Bank
from Crypto.PublicKey import RSA
from constants import ROOT_PATH


def save_new_bank(data):
    RSAkey = RSA.generate(1024)
    getattr(RSAkey.key, 'n')


    bank = Bank.query.filter_by(Name=data['name']).first()
    if not bank:
        print(uuid.uuid1())
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

    # else:
    #     response_object = {
    #         'status': 'fail',
    #         'message': 'User already exists. Please Log in.',
    #     }
    #     return response_object, 409


