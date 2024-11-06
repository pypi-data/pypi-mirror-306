import requests
from pydantic import BaseModel

from ...Application.Abstractions.base_rest_client import BaseRestClientFWDI
from ...Application.DTO.Auth.login_response import LoginResponse
from ...Infrastructure.Configs.rest_client_config import RestClientConfig

class RestClientFWDI(BaseRestClientFWDI):
    def __init__(self, config:RestClientConfig) -> None:
        self.__config:RestClientConfig = config
        self.__schem:str = 'http' if not config.security_layer else 'https'
        self.__base_url = f'{self.__schem}://{self.__config.server}:{self.__config.port}'
        self.__is_auth: bool = False
        self.__token:str = ''
        self.__headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization':''
        }
    
    @property
    def IsAuth(self):
        return self.__is_auth

    def login(self, url:str='/token')->bool:
        response = requests.post(f'{self.__base_url}{url}', 
                                 data = {'username': self.__config.username,'password': self.__config.password}) 
        if response.status_code == 200:
            response_json = response.json()
            if 'access_token' in response_json:
                response_toke = LoginResponse(**response.json())
                self.__token = response_toke.access_token
                self.__headers["Authorization"] = f"Bearer {self.__token}"
                self.__is_auth = True
                
                return True
            else:
                print(f'Error auth:{response}')
                unknow_error = response.json()
                print(unknow_error)

                return False
        elif response.status_code == 401:
            error_auth = response.json()
            print(f"Error:{error_auth}, code: {response.status_code}")

            return False
    
    def get(self, path:str, _data:BaseModel)->any:
        if len(self.__token) > 0:
            response_get = requests.get(f"{self.__base_url}{path}", data=_data.model_dump_json(), headers=self.__headers)
            
            if response_get.status_code == 200:
                return response_get.json(), response_get.status_code
            else:
                error_json = response_get.json()
                if 'detail' in error_json:
                    if error_json['detail'] == 'Could not validate credentials':
                        if self.login():
                            return self.get(path, _data)

                return response_get, response_get.status_code

    def post(self, path:str, _data:BaseModel)->any:
        if len(self.__token) > 0:
            response_post = requests.post(f"{self.__base_url}{path}", data=_data.model_dump_json(), headers=self.__headers)
            
            if response_post.status_code == 200:
                return response_post.json(), response_post.status_code
            else:
                error_json = response_post.json()
                if 'detail' in error_json:
                    if error_json['detail'] == 'Could not validate credentials':
                        if self.login():
                            return self.get(path, _data)

                return response_post, response_post.status_code