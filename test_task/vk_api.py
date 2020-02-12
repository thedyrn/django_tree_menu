import requests
import os

AUTH_URL = 'https://oauth.vk.com/authorize'
ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
METHOD_URL = 'https://api.vk.com/method/'
CLIENT_ID = '7315979'
CLIENT_SECRET = '8VpJSKl7SmV7eQTunnIG'
RESPONSE_TYPE = 'code'
API_VERSION = '5.103'


class VkAPI:
    def __init__(self, redirect_uri: str):
        self.redirect_uri = redirect_uri
        self.client_id = CLIENT_ID

    def get_auth_url(self, scope: str, state: str = None, display: str = 'page') -> str:
        """Возращает сгегерированную сслыку для авторизации."""
        state_or_empty = f"&state={state}" if state is not None else ""

        return f'{AUTH_URL}?client_id={self.client_id}&redirect_uri={self.redirect_uri}' \
               f'&display={display}&scope={scope}&response_type={RESPONSE_TYPE}' \
               f'&v={API_VERSION}{state_or_empty}'

    # TODO обработка ошибок
    def get_access_token(self, code: str) -> dict:
        """Получение токена после переадрисации от ВК."""
        params = {'client_id': self.client_id, 'client_secret': CLIENT_SECRET,
                  'redirect_uri': self.redirect_uri, 'code': code}
        response = requests.get(ACCESS_TOKEN_URL, params)
        return response.json()

    @staticmethod
    def get_friends(user_id: int, access_token: str, count: int = 5) -> list:
        """Возращает список друзей."""
        url = METHOD_URL + 'friends.get'
        params = {'user_id': user_id, 'count': count, 'fields': 'photo_50',
                  'access_token': access_token, 'v': API_VERSION}
        response = requests.get(url, params)
        return response.json()['response']['items']

    @staticmethod
    def get_me(access_token: str) -> dict:
        """Возращает представление текущего пользователя в виде словаря."""
        url = METHOD_URL + 'users.get'
        params = {'fields': 'photo_100', 'access_token': access_token, 'v': API_VERSION}
        response = requests.get(url, params)
        return response.json()['response'][0]
