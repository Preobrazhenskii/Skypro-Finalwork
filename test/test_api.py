import requests
from ApiClass import Api
import allure


base_url = "https://web-agr.chitai-gorod.ru/web/api/v2/"
cart_url = "https://web-agr.chitai-gorod.ru/web/api/v1/"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIzNDA3MjU1LCJpYXQiOjE3NzA5OTA0MzgsImV4cCI6MTc3MDk5NDAzOCwidHlwZSI6MjAsImp0aSI6IjAxOWM1NzQxLTg5ZWUtNzc5OC1hYjFkLWIwYTUwMTM5MmM3MiIsInJvbGVzIjoxMH0.xaM9ofrm6GkEfIsiuYxSEymfEmbIcDLoxl5ORa6hbhh30mL1zY_60LfqLsj5FCuYypEOw3LPMM8z7Ubdwmkf5jSTPYV0Ib4HmpXylk2CfWwLL3jMJZ8sTyVDJQL9iLJzpk30rQQqtBVGEiITdfFJCqPa6COLVRSWwVDTY-3eg15uepdBO0NZbWB-iTPS0Qb6NOnt1htJiIaVd4xau3s7JfBzymTWQ8SPEvT4nm4xkzDJARUPgOU67oSF7VD_3RlXVgqkJYXU3INTXhKNtzUWJ-JHy4krD6jHoRfDAp8agpQttuyOskY3uOxSr122OpNIPVWta0NrfCIGeSe--FG6JA"
api = Api(base_url, token)
api_cart = Api(cart_url, token)



@allure.title('Поиск по названию на кириллице')
@allure.description('Проверка корректной работы поиска при вводе запроса на русском языке')
@allure.feature('Поиск товаров')
@allure.severity(allure.severity_level.CRITICAL)
def test_search_by_cyrillic():
    resp = api.search('Титаник')
    print(resp.status_code)
    assert resp.status_code == 200

@allure.title("Поиск c цифрами")
@allure.description('Проверка, что поиск обрабатывает запросы, содержащие только цифры')
@allure.feature('Поиск товаров')
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_numbers():
    resp = api.search('365')
    #print(resp.status_code)
    assert resp.status_code == 200

@allure.title("Поиск без токена")
@allure.description('Проверка, что запрос без авторизации возвращает статус 401')
@allure.feature('Авторизация')
@allure.severity(allure.severity_level.CRITICAL)
def test_search_with_no_auth():
    resp = api.no_auth_search('Да, я не авторизован')
    assert resp.status_code == 401 


@allure.title("Поиск с неправильным методом")
@allure.description('Проверка, что DELETE-запрос к эндпоинту поиска возвращает статус 405')
@allure.feature('Поиск товаров')
@allure.severity(allure.severity_level.NORMAL)
def test_search_with_wrong_method():
    resp = api.wrong_method_search('Ждем статус 405 в проверке')
    assert resp.status_code == 405

@allure.title("Удаление товара из корзины")
@allure.description('Проверка успешного удаления товара из корзины (статус 204)')
@allure.feature('Корзина')
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_product():
    resp = api_cart.delete_product("247369297")

    assert resp.status_code == 204