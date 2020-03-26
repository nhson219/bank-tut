import uuid
import datetime

from app.main import db
from app.main.model.customer import Customer
from app.main.model.user_account import UserAccount
from app.main.model.payment_account import PaymentAccount
from app.main.service.user_account_service import UserAccountService
from app.main.service.payment_account_service import PaymentAccountService
from app.main.model.customer_store import CustomerStore
from app.main.service.response_service import ResponseService
from app.main.service.payment_transaction_service import PaymentTransactionService
from app.main.model.payment_transaction import PaymentTransaction
from app.main.model.payment_history import PaymentHistory
from sqlalchemy.orm import joinedload
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from flask import jsonify


SENDER = "nhson219@gmail.com"
CONFIGURATION_SET = "nhson219"
AWS_REGION = "us-east-1"
SUBJECT = "Internet Banking project"
CHARSET = "UTF-8"

def add_payment(data):
    #PaymentAccount.update().values(Amount=5).where(PaymentAccount.PaymentAccountId == Customer.PaymentAccount)
    # number_payment = data['number_payment_or_user_name']
    # username = data['number_payment_or_user_name']
    payment_account = PaymentAccount.query.filter_by(NumberPaymentAccount=data['number_payment_or_user_name']).first()
    user_account = UserAccount.query.filter_by(UserName=data['number_payment_or_user_name']).first()
    if payment_account:
        try:
            payment_account.Amount = payment_account.Amount + data['amount']
            db.session.commit()
            response_object = {
                'status' : 'success',
                'message': 'Success update amount'
            }
            return ResponseService().response('success', 200, data), 201
        except:
            db.session.rollback()
        finally:
            db.session.close()  
    elif user_account:
        
        customer = Customer.query.filter_by(UserAccountId=user_account.AccountId).first()
        if customer:
                payment_account = PaymentAccount.query.filter_by(PaymentAccountId=customer.PaymentAccount).first()
                
                if payment_account:
                    try:
                        payment_account.Amount = payment_account.Amount + data['amount']
                        db.session.commit()
                        response_object = {
                            'status' : 'success',
                            'message': 'Success update amount'
                        }
                        return ResponseService().response('success', 200, data), 201
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close()    
                else:
                    response_object = {
                    'status' : 'fail',
                    'message': 'Update amount fail. Please try again'
                    }
                    return response_object, 409              
        else:
           response_object = {
            'status' : 'fail',
            'message': 'Update amount fail. Please try again'
        }
        return response_object, 409                               
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Update amount fail. Please try again'
        }
        return response_object, 409    
def create_transaction(data):
    customer = Customer.query.filter_by(CustomerId=data['customer_id']).options(joinedload('payment_account')).first()
    customer_receive = Customer.query.filter_by(CustomerId=data['customer_receive_id']).options(joinedload('payment_account')).first()                                         

    if customer and customer_receive:
        if data['amount'] < customer.payment_account.Amount and data['amount'] > 0:

            
            # create payment transaction here
            otpCode = PaymentTransactionService.generate_otp_code()

            tmp = PaymentTransactionService.save_payment_transaction(PaymentTransaction(
                PaymentAccountId = data['customer_id'],
                PaymentAccountReceiveId = data['customer_receive_id'],
                Amount = data['amount'],
                Content = data['content'],
                OtpCode = otpCode,
                SendOtpTime = datetime.utcnow().timestamp(),
                Status = PaymentTransaction.STATUS_INACTIVE
            ))
            data_sendmail = {
                'customer_email': customer.Email,
                'otp_code': otpCode
            }
            send_mail(data_sendmail)
            
            try:
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()  

            response_object = {
                            'status' : 'success',
                            'message': 'Success create transaction'
                        }
            return ResponseService().response('success', 200, data), 201   
        else:
            response_object = {
                'status' : 'fail',
                'message': 'Create transaction fail. Please try again'
            }
            return response_object, 409
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Create transaction fail. Please try again'
        }
        return response_object, 409

def send_mail(data):
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',
        aws_access_key_id='AKIA2IPQCAGZEJ7VDYUH',
        aws_secret_access_key="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",
        region_name=AWS_REGION
    )
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    data['customer_email'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': "OTP code : " + str(data['otp_code']),
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': "OTP code : " + str(data['otp_code']),
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def confirm_transaction(data):
    customer = Customer.query.filter_by(CustomerId=data['customer_id']).options(joinedload('payment_account')).first()
    otp_code = data['otp_code']
    if customer and otp_code:
        payment_transaction = PaymentTransaction.query.\
                        filter_by(PaymentAccountId=data['customer_id'], OtpCode=otp_code).\
                        first()

        current_time = datetime.utcnow().timestamp()

        if payment_transaction and payment_transaction.SendOtpTime <= current_time + PaymentTransaction.TIME_EXPIRE_OTP:

            customer_receive = Customer.query.filter_by(CustomerId=payment_transaction.PaymentAccountReceiveId).options(joinedload('payment_account')).first()   

            customer_amount = customer.payment_account.Amount # set amount of customer send
            customer_receive_amount = customer_receive.payment_account.Amount # set amount of customer will receive
            customer.payment_account.Amount = customer_amount - payment_transaction.Amount
            customer_receive.payment_account.Amount = customer_receive_amount + payment_transaction.Amount

            payment_transaction.Status = PaymentTransaction.STATUS_ACTIVE # set active

            try:
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                db.session.close()  

            response_object = {
                            'status' : 'success',
                            'message': 'Success confirm transaction'
                        }
            return ResponseService().response('success', 200, data), 201
        else:
            response_object = {
                'status' : 'fail',
                'message': 'Confirm transaction fail or otp expire. Please try again'
            }
            return response_object, 409
    else:
        response_object = {
            'status' : 'fail',
            'message': 'Confirm transaction fail. Please try again'
        }
        return response_object, 409    

def get_payment_history_customer(data):
    customer = Customer.query.filter_by(CustomerId=data).options(joinedload('payment_history')).first()
    return jsonify(data=[i.serialize for i in customer.payment_history])

#def transfer_money(data):

