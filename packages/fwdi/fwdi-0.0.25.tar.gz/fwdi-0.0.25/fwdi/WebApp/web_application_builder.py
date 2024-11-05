#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import TypeVar, Type
from fastapi.security import OAuth2PasswordBearer

from ..Utilites.ext_dict import ExtDict
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ..Application.DependencyInjection.resolve_provider import ResolveProviderFWDI
from ..Application.DependencyInjection.service_collection import ServiceCollectionFWDI
from ..Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from ..Persistence.default_init_db import DefaultInitializeDB

T = TypeVar('T')

class WebApplicationBuilder():
    def __init__(self, obj:T) -> None:
        self.__instance_app:Type[T] = obj
        self.services:BaseServiceCollectionFWDI = ServiceCollectionFWDI()
        self.__scopes:dict[str, str] = {}

    def build(self)-> Type[T]:
        from ..Presentation.dependency_injection import DependencyInjection
        
        self.__instance_app.instance = self
        self.__instance_app.resolver = ResolveProviderFWDI(self.services.GenerateContainer(), self.__instance_app.Debug)
        
        #---------------------- DEFAULT WEB CONTROLLER SERVICES ------------------------------------
        
        DependencyInjection.AddPresentation(self.__instance_app)

        #---------------------- /DEFAULT WEB CONTROLLER SERVICES -----------------------------------

        JwtServiceFWDI.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=self.__scopes,) if len(self.__scopes) > 0 else OAuth2PasswordBearer(tokenUrl="token")
        DefaultInitializeDB.init_db(self.__scopes)
        return self.__instance_app
    
    def add_scope(self, scopes:dict[str,str]):
        for item in scopes.items():
            if not item in self.__scopes:
                self.__scopes[item[0]] = item[1]
    
    def add_authentification(self):
        ...
        
    def add_health_checks(self):
        ...
    
    def add_httpclient(self):
        ...

    def add_logging(self):
        ...