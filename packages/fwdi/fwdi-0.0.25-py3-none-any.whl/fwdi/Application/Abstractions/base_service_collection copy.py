#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from abc import ABCMeta, abstractmethod
from typing import Type, TypeVar, Protocol

from .base_di_container import BaseDIConteinerFWDI

TService = TypeVar('TService')

class BaseServiceCollectionFWDI(metaclass=ABCMeta):

    @abstractmethod
    def AddSingleton(self, type_service:Type[TService], implementation:Type[TService]):
        pass

    @abstractmethod
    def AddImplementSingleton(self, implementation:TService):
        pass

    @abstractmethod
    def AddTypeSingleton(self, implementation:Type[TService]):
        pass

    @abstractmethod
    def AddTransient(self, type_service:Type[TService], implementation:TService):
        pass

    @abstractmethod
    def AddImplementTransient(self, implementation:TService):
        pass

    @abstractmethod
    def AddTypeTransient(self, implementation:Type[TService]):
        pass

    @abstractmethod
    def GenerateContainer(self)->BaseDIConteinerFWDI:
        pass
