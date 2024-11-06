#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from datetime import datetime

from ...Application.Abstractions.base_logging_service import BaseLoggingServiceFWDI
from ...Application.Abstractions.base_storage_service import BaseStorageServiceFWDI

class LoggingServiceFWDI(BaseLoggingServiceFWDI):
    def __init__(self, storage:BaseStorageServiceFWDI) -> None:
        super().__init__()
        self._storage:BaseStorageServiceFWDI = storage
       
    def info(self, log:str)->None:
        self._storage.write(f"{datetime.now()}::INFO::{log}")

    def alert(self, log:str)->None:
        self._storage.write(f"{datetime.now()}::ALERT::{log}")
    
    def warning(self, log:str)->None:
        self._storage.write(f"{datetime.now()}::WARN::{log}")

    def error(self, log:str)->None:
        self._storage.write(f"{datetime.now()}::ERROR::{log}")