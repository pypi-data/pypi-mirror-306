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

from .base_service import BaseServiceFWDI

class BaseLoggingServiceFWDI(BaseServiceFWDI, metaclass=ABCMeta):
    
    @abstractmethod
    def info(self, msg:str)->None:
        ...
        
    @abstractmethod
    def alert(self, msg:str)->None:
        ...

    @abstractmethod
    def warning(self, msg:str)->None:
        ...

    @abstractmethod
    def error(self, msg:str)->None:
        ...
