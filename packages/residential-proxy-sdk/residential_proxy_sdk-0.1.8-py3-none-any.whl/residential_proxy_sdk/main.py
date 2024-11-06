import requests

class ProxySDK:
    def __init__(self, base_url: str, user_api_key: str):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'user-api-key': user_api_key,
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def login(self, username: str, password: str):
        data = {'username': username, 'password': password}
        response = self.session.post(f'{self.base_url}/api/client/login', json=data)
        response.raise_for_status()
        return response.json()
    
    def register(self, username: str, email: str, password: str):
        data = {'username': username, 'email': email, 'password': password}
        response = self.session.post(f'{self.base_url}/api/client/register', json=data)
        response.raise_for_status()
        return response.json()
    
    def forgot_password(self, email: str):
        data = {'email': email}
        response = self.session.post(f'{self.base_url}/api/client/forgot-password', json=data)
        response.raise_for_status()
        return response.json()
    
    def reset_password(self, token: str, new_password: str):
        data = {'token': token, 'new_password': new_password}
        response = self.session.post(f'{self.base_url}/api/client/reset-password', json=data)
        response.raise_for_status()
        return response.json()

    def get_provinces(self, search_text: str = None):
        params = {}
        if search_text:
            params['search_text'] = search_text
        response = self.session.get(f'{self.base_url}/api/client/provinces', params=params)
        response.raise_for_status()
        return response.json()

    def get_new_ip(self, proxy_key: str, province_id: int = None):
        params = {'proxy_key': proxy_key}
        if province_id is not None:
            params['province_id'] = province_id
        response = self.session.get(f'{self.base_url}/api/client/proxy/available', params=params)
        response.raise_for_status()
        return response.json()

    def get_current_ip(self, proxy_key: str):
        params = {'proxy_key': proxy_key}
        response = self.session.get(f'{self.base_url}/api/client/proxy/current', params=params)
        response.raise_for_status()
        return response.json()

    def remove_old_ip(self, proxy_key: str):
        data = {'proxy_key': proxy_key}
        response = self.session.post(f'{self.base_url}/api/client/proxy/remove', json=data)
        response.raise_for_status()
        return response.json()

    def get_key_list(self):
        response = self.session.get(f'{self.base_url}/api/client/key/list')
        response.raise_for_status()
        return response.json()

    def get_key_detail(self, proxy_key: str):
        params = {'proxy_key': proxy_key}
        response = self.session.get(f'{self.base_url}/api/client/key/detail', params=params)
        response.raise_for_status()
        return response.json()

    def buy_new_key(self, buy_key_dto: dict):
        response = self.session.post(f'{self.base_url}/api/client/key/buy', json=buy_key_dto)
        response.raise_for_status()
        return response.json()

    def renew_key(self, renew_key_dto: dict):
        response = self.session.post(f'{self.base_url}/api/client/key/renewal', json=renew_key_dto)
        response.raise_for_status()
        return response.json()

    def remove_key(self, proxy_key: str):
        data = {'proxy_key': proxy_key}
        response = self.session.post(f'{self.base_url}/api/client/key/remove', json=data)
        response.raise_for_status()
        return response.json()

    def get_user_info(self):
        response = self.session.get(f'{self.base_url}/api/client/user/current')
        response.raise_for_status()
        return response.json()
