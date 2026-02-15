import requests
import allure


class Api:
    def __init__(self, url, token):
        """
        Конструктор класса ApiClass
        
        
        :param url: URL страницы
        :param token: Bearer токен авторизации
        """
        self.url = url
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def auth(self) -> dict:
        """
        Добавление токена авторизации в headers
        """
        return self.headers

    def search(self, phrase): 
        """
        Поиск товара
        
        :param phrase: Слово/фраза для ввода в строку поиска
        :return: Respons object с результатами поиска
        """
        params = {"phrase": phrase}
        return requests.get(self.url+'search/facet-search', params=params, headers=self.auth())
    
    def no_auth_search(self, phrase):
        """
        Поиск товара без аутентификации
        
        :param phrase: Слово/фраза для ввода в строку поиска
        """
        params = {"phrase": phrase}
        return requests.get(self.url+'search/facet-search', params=params)

    def wrong_method_search(self, phrase):
        """
        Поиск на странице с некорректным методом (DELETE)
        
        :param phrase: Слово/фраза для ввода в строку поиска
        """
        params = {"phrase": phrase}
        return requests.delete(self.url+'search/facet-search', params=params, headers=self.auth())
    
    def delete_product(self, id):
        """
        Удаление товара из корзины
        
        :param id: ID товара в корзине 
        """
        return requests.delete(self.url+'cart/product/'+id, headers=self.auth())
    
    def get_cart(self) -> dict:
        """
        Получение списка товаров в корзине
        """
        resp = requests.get(self.url+'cart', headers=self.auth())
        return resp.json()