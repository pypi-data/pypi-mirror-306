import functools
from typing import Any, Callable, TypeVar

from ..Domain.Enums.type_methods import TypeMethod

from ..Application.Abstractions.base_service import BaseServiceFWDI
from ..Application.DependencyInjection.resolve_provider import ResolveProviderFWDI

from ..Utilites.ext_reflection import ExtReflection
from ..Utilites.utilities import Utilities

_C = TypeVar("_C", bound=Callable[..., Any])

class my_wrapper(object):
    def __init__(self, func: _C):
        self.__func = func
        self.__doc__ = func.__doc__
        
        if hasattr(func, '__name__'):
            self.__name__ = func.__name__
            print(f"{func.__module__}::{self.__func}")
            
        functools.update_wrapper(self, func)           

    def __call__(self, *args, **kwargs):
        return self.__wrap_run(args, kwargs)
    
    def __wrap_run(self, *args, **kwargs):
        print(f"{__name__}::{self.__func} !!!!!!!!!!!!SYNC INJECT!!!!!!!!!!!!!!")            
        if 'is_inject' not in kwargs:
            method_info = ExtReflection.get_function_info_v2(self.__func, args, kwargs)
            new_args:dict = {}

            if len(kwargs) > 0 and len(kwargs) == len(method_info['method_params']):
                result = self.__func(*args, **kwargs)
                return result
            
            match method_info['method_type']:
                case TypeMethod.Instance:
                    new_args = ExtReflection.__instance_gen_new_args(method_info)
                case TypeMethod.Static:
                    if not method_info['has_self']:
                        new_args = my_wrapper.__static_gen_new_args(method_info)
                    else:
                        new_args = ExtReflection.__instance_gen_new_args(method_info)
                case TypeMethod.Classmethod:
                    new_args = ExtReflection.__classmethod_gen_new_args(method_info)

            result = self.__func(**new_args)
            return result
        else:
            new_args = [item for item in kwargs if item != 'is_inject']
            result = self.__func(*args, **new_args)

        return result
    
    @staticmethod
    def __static_gen_new_args(info:dict)->dict:
        args:tuple = info['origin_args'] if info['has_self'] else info['clear_args'] if 'clear_args' in info else {}
        kwargs:dict = info['origin_kwargs']

        method_params:dict = [item for item in info['method_params'] if item['name'] != 'self']

        new_kwargs_params:dict[str, any] = {}
        if Utilities.search_key(info['method_params'], 'self'):
            new_kwargs_params['self'] = args[0]
        else:
            if len(args) > 1:
                if type(args[0]) is info['method_class']:
                    new_kwargs_params['self'] = args[0]
                    method_params = method_params[1:]

                if len(args) == len(method_params):
                    for i, arg1 in enumerate(args):
                        if type(arg1) is method_params[i]['type']:
                            method_name = method_params[i]['name']
                            new_kwargs_params[method_name] = args[i]

                    method_params = method_params[i + 1:]

        count_args = len(args)
        for item in method_params:
            arg_pos, arg_name, arg_type = item['arg_pos'], item['name'], item['type']
            if count_args >= 1:
                if arg_pos < count_args:
                    arg_item = args[arg_pos]

                    if type(arg_item) == arg_type:
                        new_kwargs_params[arg_name] = args[arg_pos]
                    elif type(arg_item) is list:
                        new_kwargs_params[arg_name] = args[arg_pos]
                    else:
                        if len(kwargs) > 0:
                            try_get_value = kwargs.get(arg_name)
                            if try_get_value != None:
                                new_kwargs_params[arg_name] = try_get_value
                        else:
                            if issubclass(arg_type, BaseServiceFWDI):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                else:

                    if issubclass(arg_type, BaseServiceFWDI):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                    else:
                        if len(kwargs) > 0:
                            try_get_value = kwargs.get(arg_name)
                            new_kwargs_params[arg_name] = try_get_value if try_get_value != None else ResolveProviderFWDI.get_service(arg_type)
                        else:
                            if issubclass(arg_type, BaseServiceFWDI):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                            elif ResolveProviderFWDI.contains(arg_type):
                                new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                            elif 'default' in item:
                                new_kwargs_params[arg_name] = item['default']

            else:
                if len(kwargs) > 0:
                    try_get_value = kwargs.get(arg_name)
                    if try_get_value != None:
                        new_kwargs_params[arg_name] = try_get_value
                    else:
                        if issubclass(arg_type, BaseServiceFWDI):
                            new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)
                else:
                    if issubclass(arg_type, BaseServiceFWDI):
                        new_kwargs_params[arg_name] = ResolveProviderFWDI.get_service(arg_type)


        return new_kwargs_params