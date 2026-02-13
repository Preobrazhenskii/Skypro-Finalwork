import requests
from ApiClass import Api

base_url = "https://web-agr.chitai-gorod.ru/web/api/v2/"
cart_url = "https://web-agr.chitai-gorod.ru/web/api/v1/"
token = 
api = Api(base_url, token)
api_cart = Api(cart_url, token)


# Поиск по названию на кириллице
def test_search_by_cyrillic():
    resp = api.search('Титаник')
    print(resp.status_code)
    assert resp.status_code == 200

# Поиск c цифрами
def test_search_by_numbers():
    resp = api.search('365')
    #print(resp.status_code)
    assert resp.status_code == 200
# Поиск без токена
def test_search_with_no_auth():
    resp = api.no_auth_search('Да, я не авторизован')
    assert resp.status_code == 401 
# Поиск с неправильным методом

def test_search_with_wrong_method():
    resp = api.wrong_method_search('Ждем статус 405 в проверке')
    assert resp.status_code == 405

#Удаление товара из корзины

def test_delete_product():
    resp = api_cart.delete_product("247369297")

    assert resp.status_code == 204