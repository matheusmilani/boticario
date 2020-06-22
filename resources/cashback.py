from flask import request
from flask_jwt_simple import create_jwt
from flask_restful import Resource
from helpers import *
from helpers.enum import Roles
from models.user import UserModel
from models.purchase import PurchaseModel
from resources import require_roles
from os import environ
import jwt
import re
from datetime import datetime

class CashbackResource(Resource):
    @require_roles('admin', 'reseller')
    def get(self):
        current_user = jwt.decode(request.headers['Authorization'], environ.get('JWT_SECRET_KEY'), options={'verify_exp': False})

        if Roles().enum_to_name(current_user['sub']['role']) == 'admin':
            if 'cpf' in request.args and 'month' in request.args and 'year' in request.args:
                user = UserModel.get_by_cpf(request.args['cpf'])
                if user == None:
                    return "Revendedor não encontrado"
                itens = PurchaseModel.get_by_reseller(user.id)
                itens = serialize_model_list(itens)
                itens = list(filter(lambda item: datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S.%f").month == int(request.args['month']) and datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S.%f").year == int(request.args['year']) and item['status'] == "Aprovado", itens))
                return {"purchases": itens, "cashback_by_month": calculate_multi_cashback(itens)}
        else:
            if 'month' in request.args and 'year' in request.args:
                itens = PurchaseModel.get_by_reseller(current_user['sub']['id'])
                itens = serialize_model(itens)
                itens = list(filter(lambda item: datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S.%f").month == int(request.args['month']) and datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S.%f").year == int(request.args['year']) and item['status'] == "Aprovado", itens))
                return {"purchases": itens, "cashback_by_month": calculate_multi_cashback(itens)}
