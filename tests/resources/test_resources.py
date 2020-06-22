from urllib.request import urlopen
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import create_test_app, app, client
import pytest
import json


@pytest.fixture(scope="session", autouse=True)
def before_all():
    create_test_app()


class TestEndpoint:
    def test_non_exists_endpoint(self, client):
        res = client.get('/usernonblah')

        assert res.status_code == 404

    def test_endpoint_without_authorization(self, client):
        res = client.get('/api/user')

        assert res.status_code == 403

    def test_wrong_authentication_none_email(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': '',
                'password': '1234'})
        access_decode = json.loads(auth.data.decode())

        assert access_decode['message'] == 'Email não informado'
        assert auth.status_code == 401

    def test_wrong_authentication_none_password(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'asd',
                'password': ''})
        access_decode = json.loads(auth.data.decode())

        assert access_decode['message'] == 'Senha não informada'
        assert auth.status_code == 401

    def test_wrong_authentication(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'asd',
                'password': 'asd'})
        access_decode = json.loads(auth.data.decode())

        assert access_decode['message'] == 'Invalid credentials'
        assert auth.status_code == 401


class TestAdminActionEndpoint:
    def test_authentication(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})

        access_decode = json.loads(auth.data.decode())

        assert access_decode['name'] == "Matheus D'Adamo Milani"

    def test_get_user_endpoint(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/user',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200

    def test_get_user_by_id(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/user?id=1',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200
        assert res.data != None

    def test_get_user_by_cpf(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/user?cpf=23666513840',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200
        assert res.data != None

    def test_get_user_by_email(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/user?email=matheus.milani21@gmail.com',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200
        assert res.data != None

    def test_post_user_with_wrong_params(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.post(
            '/api/user',
            json={
                'email': 'matheus.milani21+teste@gmail.com',
                'cpf': '23666513840'},
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 401
        assert res.data == b'"Par\\u00e2metros incorretos"\n'

    def test_post_user(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.post(
            '/api/user',
            json={
                'email': 'matheus.milani21+teste@gmail.com',
                'name': 'teste',
                'role': 'admin',
                'cpf': '01340534002'},
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 201

    def test_post_user_with_duplicate_cpf_or_email_params(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.post(
            '/api/user',
            json={
                'email': 'matheus.milani21@gmail.com',
                'name': 'teste',
                'role': 'admin',
                'cpf': '236.66513840'},
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 401
        assert res.data == b'"CPF incorreto"\n'

        res = client.post(
            '/api/user',
            json={
                'email': 'matheus.milani21@gmail.com',
                'name': 'teste',
                'role': 'admin',
                'cpf': '23666513849'},
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 401

    def test_get_cashback_endpoint(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/cashback?cpf=23666513840&month=06&year=2020',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200

    def test_get_purchase_endpoint(self, client):
        auth = client.post(
            '/api/authentication',
            json={
                'email': 'matheus.milani21@gmail.com',
                'password': 'teste@1234'})
        access_decode = json.loads(auth.data.decode())

        res = client.get(
            '/api/purchase',
            headers={
                'Authorization': access_decode['token']})

        assert res.status_code == 200
