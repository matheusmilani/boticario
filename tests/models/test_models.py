import pytest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import create_test_app
from . import db

from models.user import UserModel
from models.purchase import PurchaseModel

@pytest.fixture(scope="session", autouse=True)
def before_all():
    create_test_app()


class TestUser:
    def test_get_user(self):
        admin = UserModel.get_by_cpf("23666513840")
        assert admin.email == 'matheus.milani21@gmail.com'
        assert admin.cpf == '23666513840'

        admin = UserModel.get_by_email("matheus.milani21@gmail.com")
        assert admin.email == 'matheus.milani21@gmail.com'
        assert admin.cpf == '23666513840'

        reseller = UserModel.get_by_cpf("74936635057")
        assert reseller.email == 'reseller@gmail.com'
        assert reseller.cpf == '74936635057'

        reseller = UserModel.get_by_email("reseller@gmail.com")
        assert reseller.email == 'reseller@gmail.com'
        assert reseller.cpf == '74936635057'

        wrong_user = UserModel.get_by_cpf("11111111")
        assert wrong_user == None

    def test_authenticate_correct_user(self):
        authenticate = UserModel.authenticate('matheus.milani21@gmail.com', 'teste@1234')
        assert authenticate == UserModel.query.filter_by(email='matheus.milani21@gmail.com').first()

        authenticate = UserModel.authenticate('reseller@gmail.com', 'teste@1234')
        assert authenticate == UserModel.query.filter_by(email='reseller@gmail.com').first()

    def test_no_authenticate_wrong_user(self):
        authenticate = UserModel.authenticate('wrong_user@wrong_user.com', '1234')
        assert authenticate is None

    def test_no_authenticate_wrong_password(self):
        authenticate = UserModel.authenticate('matheus.milani21@gmail.com', 'wrong-pass')
        assert authenticate is None

    def test_save_user(self):
        users = len(UserModel.list())
        new_user = UserModel()
        new_user.name = "Teste"
        new_user.cpf = "1234567890"
        new_user.email = "teste@gmail.com"
        new_user.password = "teste@1234"
        new_user.role = 2
        new_user.save()

        assert users + 1 == len(UserModel.list())

    def test_delete_user(self):
        users = len(UserModel.list())

        user = UserModel.delete(3)

        assert users - 1 == len(UserModel.list())

class TestPurchaseModel:
    def test_new_purchase(self):
        assert len(PurchaseModel.list()) == 0

        purchase = PurchaseModel()
        purchase.code = 1
        purchase.value = 1000
        purchase.id_reseller = 2
        purchase.status = "Em validação"
        purchase.save()

        assert len(PurchaseModel.list()) != 0

    def test_get_by_reseller(self):
        purchase = PurchaseModel.get(1)
        assert purchase != None

        purchase = PurchaseModel.get_by_reseller('74936635057')

        assert purchase != None

    def test_delete_purchase(self):
        purchase = PurchaseModel()
        purchase.code = 2
        purchase.value = 1000
        purchase.id_reseller = 2
        purchase.status = "Em validação"
        purchase.save()

        purchases = len(PurchaseModel.list())

        PurchaseModel.delete(2)

        assert purchases - 1 == len(PurchaseModel.list())
