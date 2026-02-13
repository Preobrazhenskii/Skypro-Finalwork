import requests 

class Api:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def auth(self):
        return self.headers

    def search(self, phrase):
        params = {"phrase": phrase}
        return requests.get(self.url+'search/facet-search', params=params, headers=self.auth())
    
    def no_auth_search(self, phrase):
        params = {"phrase": phrase}
        return requests.get(self.url+'search/facet-search', params=params)

    def wrong_method_search(self, phrase):
        params = {"phrase": phrase}
        return requests.delete(self.url+'search/facet-search', params=params, headers=self.auth())
    
    def delete_product(self, id):
        id = id
        return requests.delete(self.url+'cart/product/'+id, headers=self.auth())
    
    def get_cart(self):
        resp = requests.get(self.url+'cart', headers=self.auth())
        return resp.json()
    