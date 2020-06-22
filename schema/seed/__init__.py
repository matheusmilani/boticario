from models.user import UserModel
from models.purchase import PurchaseModel

def first_user():
    if UserModel.get_by_cpf("23666513840") != None:
        return
    new_user = UserModel()
    new_user.name = "Matheus D'Adamo Milani"
    new_user.cpf = "23666513840"
    new_user.email = "matheus.milani21@gmail.com"
    new_user.password = "teste@1234"
    new_user.role = 1
    new_user.save()
    return

def first_purchase():
    return
