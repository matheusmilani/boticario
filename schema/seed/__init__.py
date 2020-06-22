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

def first_reseller_user():
    if UserModel.get_by_cpf("74936635057") != None:
        return
    new_user = UserModel()
    new_user.name = "Matheus D'Adamo Milani"
    new_user.cpf = "74936635057"
    new_user.email = "reseller@gmail.com"
    new_user.password = "teste@1234"
    new_user.role = 2
    new_user.save()
    return

def first_purchase():
    if UserModel.get_by_cpf("74936635057") == None:
        first_reseller_user()

    if PurchaseModel.get_by_reseller(2) != None:
        return

    new_purchase = PurchaseModel()
    new_purchase.code = 1
    new_purchase.value = 1000
    new_purchase.id_reseller = 1
    new_purchase.status = "Em validação"
    new_purchase.save()
    return
