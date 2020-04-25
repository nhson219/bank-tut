from flask import request, send_from_directory
from flask_restplus import Resource

from ..util.dto import BankDto
from ..service.bank_service import save_new_bank, create_new_rsa
from constants import ROOT_PATH

api = BankDto.api


@api.route('/bank')
class Bank(Resource):

    @api.response(201, 'Bank successfully created.')
    @api.doc('create a new bankk')
    def post(self):
        """Creates a new Bank """
        data = request.json
        return save_new_bank(data=data)

@api.route('/bank/generate')
class BankGenerateRSA(Resource):
    @api.response(201, 'Bank rsa successfully created.')
    @api.doc('Generate a new rsa key')
    def get(self):
        """Creates a new Bank rsa """
        return create_new_rsa()


@api.route('/download')
class BankDownloadRSA(Resource):
    @api.response(201, 'Bank rsa download successfully created.')
    @api.doc('Bank rsa download')
    def get(self):
        """Download bank rsa """

        return send_from_directory(ROOT_PATH + '/key',
                               'public_key.pem', as_attachment=True)        