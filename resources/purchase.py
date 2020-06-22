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

class PurchaseResource(Resource):
    @require_roles('admin', 'reseller')
    def get(self):
        current_user = jwt.decode(request.headers['Authorization'], environ.get('JWT_SECRET_KEY'), options={'verify_exp': False})

        if Roles().enum_to_name(current_user['sub']['role']) == 'admin':
            if 'id' in request.args:
                item = PurchaseModel.get(request.args['id'])
                item = serialize_model(item)
                item['cashback'] = calculate_unit_cashback(item['value'])
                return item
            elif 'cpf' in request.args:
                itens = PurchaseModel.get_by_reseller(request.args['cpf'])
                itens = serialize_model_list(itens)
                for item in itens:
                    item['cashback'] = calculate_unit_cashback(item['value'])
                return itens
            list = PurchaseModel.list()
            list = serialize_model_list(list)
            for item in list:
                item['cashback'] = calculate_unit_cashback(item['value'])
            return list
        else:
            if 'id' in request.args:
                item = PurchaseModel.get_by_reseller(current_user['sub']['id'])
                item = serialize_model(item)
                if item['id'] == request.args['id']:
                    return item
                else:
                    return
            list = PurchaseModel.get_by_reseller(current_user['sub']['id'])
            return list

    @require_roles('admin', 'reseller')
    def post(self):
        try:
            data = request.get_json()
            item = PurchaseModel()

            current_user = jwt.decode(request.headers['Authorization'], environ.get('JWT_SECRET_KEY'), options={'verify_exp': False})

            if Roles().enum_to_name(current_user['sub']['role']) == 'admin':
                if check_params(['code', 'value', 'cpf'], data.keys()) == False:
                    return "Parâmetros incorretos", 401

                if check_cpf(data['cpf']) is False:
                    return 'CPF incorreto', 401

                if UserModel.get_by_cpf(data['cpf']) == None:
                    return 'CPF não registrado', 401

                for parameter in data:
                    setattr(item, parameter, data[parameter])
                item.id_reseller = UserModel.get_by_cpf(data['cpf']).id
                item.status = "Em validação" if data['cpf'] not in ['153.509.460-56', '15350946056'] else "Aprovado"
                item.save()
                return "success", 201
            else:
                if check_params(['code', 'value'], data.keys()) == False:
                    return "Parâmetros incorretos", 401

                for parameter in data:
                    setattr(item, parameter, data[parameter])
                item.reseller = UserModel.get_by_cpf(current_user['sub']['cpf'])
                item.status = "Em validação" if current_user['sub']['cpf'] not in ['153.509.460-56', '15350946056'] else "Aprovado"
                item.save()
                return "success", 201
        except:
            return "error", 401

    @require_roles('admin')
    def put(self):
        try:
            data = request.get_json()
            item = PurchaseModel.get(data['id'])

            if item == None:
                return "ID incorreto"

            if data['status'] not in ['Aprovado', 'Reprovado', 'Em validação']:
                return "Status informado incorreto. Deve ser: Aprovado, Reprovado ou Em validação"

            item.status = data['status']
            item.save()
            return "success", 201
        except:
            return "error", 401

    @require_roles('admin')
    def delete(self):
        try:
            if 'id' in request.args:
                item = PurchaseModel.delete(request.args['id'])
                return "success", 201
            return "No ID", 401
        except:
            return "error", 401
