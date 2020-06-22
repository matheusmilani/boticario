from flask import request
from flask_jwt_simple import create_jwt
from flask_restful import Resource
from models.user import UserModel


class AuthenticationResource(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        if email == '':
            return {'message': 'Email não informado'}, 401

        if password == '':
            return {'message': 'Senha não informada'}, 401

        user = UserModel.authenticate(email, password)

        if user is not None:
            token = create_jwt({
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'id': user.id,
                'cpf': user.cpf,
            })

            return {
                'name': user.name,
                'token': token
            }
        else:
            return {'message': 'Invalid credentials'}, 401
