from datetime import datetime, timedelta
from dateutil.parser import parse
from flask import request
from flask_restful import Resource
from models.user import UserModel
from os import environ
from re import match
from service.email import EmailService
from uuid import uuid4

MESSAGE_TEMPLATE = """
O seu token de recuperação de senha é: {0}
"""

class UserRecoveryPasswordResource(Resource):
    def get(self):
        email = request.args['email']
        user = UserModel.get_by_email(email)

        if user:
            user.recover_token = str(uuid4())
            user.save()

            message = MESSAGE_TEMPLATE.format(user.recover_token)

            email_service = EmailService()
            email_service.send(to_address=user.email, message_content=message, subject='Boticário - Recuperação de senha')

            return 'Mensagem de recuperação de senha enviada para o email solicitado.', 200

        else:
            return 'Usuário não encontrado', 404

    def post(self):
        data = request.get_json()

        email = data['email']
        token = data['token']
        new_password = data['password']
        error = None

        user = UserModel.get_by_email(email)

        if not user or not user.recover_token:
            error = 'Usuário inválido'

        elif user.recover_token != token:
            error = 'Token inválido'

        if error:
            return error, 401

        user.recover_token = None
        user.password = new_password
        user.save()

        return "success", 204
