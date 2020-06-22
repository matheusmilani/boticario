from helpers import *


class TestHelpers:
    def test_remove_repeated(self):
        list_1 = [1,2,3,1]
        assert remove_repeated(list_1) == [1,2,3]

    def test_is_none_or_zero(self):
        assert isNoneOrZero(0) == True
        assert isNoneOrZero(None) == True
        assert isNoneOrZero('None') == False
        assert isNoneOrZero('aasdasd') == False

    def test_check_email(self):
        assert check_email('asd@asd.com') == True
        assert check_email('asd') == False

    def test_check_cpf(self):
        assert check_cpf('23666513840') == True
        assert check_cpf('236.665.138-40') == True
        assert check_cpf('111111') == False
        assert check_cpf('asdasd') == False

    def test_check_params(self):
        assert check_params(['teste', 'teste_1', 'teste_2'], ['teste', 'teste_1', 'teste_2']) == True
        assert check_params(['teste', 'teste_1', 'teste_2'], ['teste', 'teste_1']) == False
        assert check_params(['teste', 'teste_1'], ['teste', 'teste_1', 'teste_2']) == False

    def test_calculate_unit_cashback(self):
        assert calculate_unit_cashback(800) == 80
        assert calculate_unit_cashback(1000) == 10
        assert calculate_unit_cashback(1300) == 195
        assert calculate_unit_cashback(4000) == 800

    def test_calculate_unit_cashback(self):
        itens_1 = [{"value": 100},{"value": 500},{"value": 200},{"value": 200}]
        assert calculate_multi_cashback(itens_1) == 100

        itens_2 = [{"value": 100},{"value": 500},{"value": 200},{"value": 200},{"value": 100},{"value": 500},{"value": 200},{"value": 200}]
        assert calculate_multi_cashback(itens_1) == 100
