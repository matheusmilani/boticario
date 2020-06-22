from datetime import datetime, timedelta
from flask import jsonify, current_app, request
from flask_jwt_simple import JWTManager, get_jwt
from flask_restful import Api
from flask_cors import CORS
from functools import wraps
from werkzeug.exceptions import HTTPException
from os import environ
from dotenv import load_dotenv
from helpers.enum import Roles
import json
import jwt


def initialize_resources(application):
    api = Api(application)
    jwt = JWTManager(application)
    CORS(application, supports_credentials=True, origins="*")

    from resources.user import UserResource
    from resources.authentication import AuthenticationResource
    from resources.user_recovery_password import UserRecoveryPasswordResource
    from resources.purchase import PurchaseResource
    from resources.cashback import CashbackResource

    api.add_resource(AuthenticationResource, '/api/authentication')
    api.add_resource(UserRecoveryPasswordResource, '/api/recover_password')
    api.add_resource(UserResource, '/api/user')
    api.add_resource(PurchaseResource, '/api/purchase')
    api.add_resource(CashbackResource, '/api/cashback')

    @application.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        if environ.get('EBS_ENVIRONMENT') in ['local', None]:
            return jsonify(message=str(e)), code
        return jsonify(message='error'), code

    @application.after_request
    def nocache_control(response):
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

    @jwt.jwt_data_loader
    def add_claims_to_access_token(identity):
        now = datetime.utcnow()

        return {
            'exp': now + timedelta(hours=7),
            'iat': now,
            'nbf': now,
            'sub': {
                'id': identity['id'],
                'name': identity['name'],
                'email': identity['email'],
                'role': identity['role'],
                'cpf': identity['cpf'],
            }
        }


def require_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return {'message':'Missing authorization header'}, 403

            jwt_decoded = jwt.decode(request.headers['Authorization'], environ.get('JWT_SECRET_KEY'), options={'verify_exp': False})

            if datetime.utcnow() > datetime.fromtimestamp(jwt_decoded['exp']):
                return {'message':'Session expired'}, 403

            if any(str(role) in str(Roles().enum_to_name(jwt_decoded['sub']['role'])) for role in roles):
                return f(*args, **kwargs)

            return {'message':'Unauthorized'}, 403
        return wrapped
    return wrapper
