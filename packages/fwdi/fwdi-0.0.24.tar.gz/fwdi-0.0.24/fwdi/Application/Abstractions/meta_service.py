#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

import inspect
from ...Utilites.ext_reflection import ExtReflection

class MetaServiceFWDI(type):
    def __init__(cls, name, bases, ns):
        for attr, value in cls.__dict__.items():
            if callable(value):
                if attr == '__call__':
                    setattr(cls, attr, ExtReflection.init_inject(value))
                    
                #if attr == '__init__':
                    #setattr(cls, attr, ExtReflection.init_inject(value))

                if not attr.startswith('__'):
                    if not inspect.isabstract(cls):
                        #setattr(cls, attr, ExtReflection.method_inject(value))
                        setattr(cls, attr, ExtReflection.method_inject_v2(value))
                        #setattr(cls, attr, my_wrapper(value))

        super().__init__(name, bases, ns)