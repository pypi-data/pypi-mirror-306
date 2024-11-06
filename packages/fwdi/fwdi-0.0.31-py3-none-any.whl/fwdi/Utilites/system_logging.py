from enum import Enum
import logging

class TypeLogging(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    NOTSET = 5

logging.basicConfig(filename='__system__.log', encoding='utf-8', level=logging.DEBUG)

class SysLogging():
    _instance = None
    def __init__(self):
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls, logging_level=TypeLogging, filename:str='__system__.log'):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            print(f'Creating new logger instance:{cls._instance}')
            match(logging_level):
                case TypeLogging.INFO:
                    level_log = logging.INFO
                case TypeLogging.DEBUG:
                    level_log = logging.DEBUG
                case TypeLogging.WARNING:
                    level_log = logging.WARNING
                case TypeLogging.ERROR:
                    level_log = logging.ERROR
                case TypeLogging.CRITICAL:
                    level_log = logging.CRITICAL
                case TypeLogging.NOTSET:
                    level_log = logging.NOTSET

            cls.logging = logging.getLogger(f'ITSHelper')
            cls.logging.setLevel(level_log)
            
            formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(message)s')
            file_handler = logging.FileHandler(f"log{filename}")
            file_handler.setLevel(level_log)
            file_handler.setFormatter(formatter
                                      )
            cls.logging.addHandler(file_handler)
            
        return cls._instance

    def __call__(self, message:str, type_log:str='INFO', args:any=None):
        match(type_log.upper()):
            case 'INFO':
                self.logging.info(message)
            case 'DEBUG':
                self.logging.debug(message)
            case 'WARNING':
                self.logging.warning(message)
            case 'ERROR':
                self.logging.error(message)
            case _:
                self.logging.info(message)