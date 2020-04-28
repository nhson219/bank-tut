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
import base64


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



def create_transaction(data):
    # try: 
        read_private_key = open(ROOT_PATH + "/key/private_key.pem", "rb")
        private_key = RSA.importKey(read_private_key.read())

        data_b64decode = base64.b64decode(b'vpOHy9a3Cw9cufiw8wyMGbgXgyeJJ2u5p4VlspjEXQvamPIkq2qLqA+/zsJYeavVR/q+203KyRZCyGeJUEoQYq8/ZbD35D2pyqkUYn3uxT7tq0aZSe50J9GysvJIdOzdesmL3awjcblYLWca3hYaLBM6mCS7QXA/UJsxcJHWHddNwqmt4e1c8SmBgcke8Wa4mOS690YM/Ny/eYUBSq+6ckJm1/E2fmRV3095ixhq2+bqdemcCNRlvrc5Se9wyV6yzWc2i5UhbPFA1eseY4xBBssNiAAe05Dr7hcOuRpYLmoEskXWcbFWetMS8BnDJIKiz4n+ffTgbzguaTipsY0locsaLksNFt+B4bPJimQp146fC3hRNxvPy25716cGxwW93NO2/1HpONUfF6z331uLBW0KRiYhJiAUQuJaxva0/p2vj3yf1hYjLkjWwAF6B2O7eFb7LOIbU6L09eDHm4cDsR4Mak3FgL1zlmFsD24XDsGLccAcMA4cGNpJ3K4SJeLboCP9VhJPEzMtR863qiKEDF07c7206bWPOfd9mVmadRyBJk6mEVgZA1PM/+XHLZFOyH5tJBXWO2bXvA44KR7Pm31mcdSdsTyphDtw7FKHaCYc1Qs6pWXQLiI/TZ64UxoYYUJyEhbT6I98toTJ08ueItUDBUWTKtPNS2aXaQ950+k=')

        # print(b64decode)
        tmp = private_key.decrypt(data_b64decode)

        print(tmp)

        # customer = Customer.query.filter_by(CustomerId=data['number_account']).options(joinedload('payment_account')).first()
        # if customer:
        #     customer.payment_account.Amount = data['amount']
        #     db.session.commit()

        #     # add log history payment    
        #     add_payment_history(type=PaymentHistory.SEND_AMOUNT, customer_id=customer.CustomerId)

        #     response_object = {
        #                     'status' : 'success',
        #                     'message': 'Success confirm transaction'
        #                 }
        #     return ResponseService().response('success', 200, data), 201

        # else:
        #     response_object = {
        #         'status' : 'fail',
        #         'message': 'Customer does not exist. Please try again'
        #     }
        #     return response_object, 409    

    # except Exception as e:
    #     raise
    #     db.session.rollback()
    # finally:
    #     db.session.close()

def convert_uuid(data):
    try:
        # read public key
        read_public_key = open(ROOT_PATH + "/key/public_key.pem", "rb")  

        # import public key
        public_key = RSA.importKey(read_public_key.read())

        # encrypt
        uuid_encrypt = public_key.encrypt(str(data['uuid'], 'utf-8'))

        # base64 encode
        base64_uuid = base64.b64encode(uuid_encrypt)

        response_object = {
                        'status' : 'success',
                        'message': 'Success convert uuid base64',
                        'base64_uuid': base64_uuid
                    }

        return ResponseService().response('success', 200, response_object), 201


    except Exception as e:
        raise        




