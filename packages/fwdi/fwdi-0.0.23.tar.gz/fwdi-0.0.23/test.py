from enum import Enum
from functools import wraps
import inspect
from typing import Any, Callable, TypeVar

from fwdi.Application.Usecase.user_repository import UserRepositoryFWDI

_C = TypeVar("_C", bound=Callable[..., Any])

def wrapper_inject(func:_C):
    @wraps(func)
    def inject(*args, **kwargs):
        print(f"Info:{type(func)}")
        if hasattr(func,"__annotations__"):
            print(f"    __annotations__:{func.__annotations__}")
    
        if hasattr(func, "__class__"):
            print(f"    __class__:{func.__class__}")

        return func(*args, **kwargs)
    
    return inject

class TestFunc():
    @wrapper_inject
    def print_self(self):
        print(f"Self class method")

    @classmethod
    def print_class_method(cls):
        print(f"Class method")
    
    @staticmethod
    def print_static():
        print(f"Static method")


def get_type(func:_C)->str:
    func_class = inspect._findclass(func)
    method_name = func.__name__
    if method_name in func_class.__dict__:
        _annotations = func_class.__dict__[method_name].__annotations__
    else:
        _annotations = func.__annotations__

    print(f"Info func by point call :{func}")

def sample1():
    test_class_func = TestFunc()
    print(f"#0: {type(test_class_func.print_self())}")
    print(f"#1: {get_type(test_class_func.print_self)}")
    print(f"#1: {get_type(TestFunc.print_self)}")
    
if __name__ == "__main__":
    sample1()