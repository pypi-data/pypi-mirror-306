import os
from fastapi import Depends, Security
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
#from fwdi.Infrastructure.LoggingService.logging_service import LoggingServiceFWDI

from Application.Config.service_congif import ServiceConfig
from Application.DTO.Request.request_detail_dump import RequestDetailDump
from Application.DTO.Request.request_upload_dump import RequestUploadDump
from Utilites.ext_rest import RestResponse


class DumpEndpoint():
    def dumps_list(request_pack:RequestUploadDump,
                  config: ServiceConfig=Depends(),
                  current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
            if not config.service_avaible:
                print('Сервис не доступен.')
                return RestResponse.response_200("Сервис временно недоступен.")
            # logger.info(f'Request dumps list: {quantity}')
            dumps = os.listdir("Dumps")[-int(request_pack.quantity)::1]
            # logger.info(f'Response dumps list: {len(dumps)}')
            return dumps

        
    def dump(request_pack: RequestDetailDump,
            config: ServiceConfig=Depends(),
            current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
            if not config.service_avaible:
                print('Сервис не доступен.')
                return RestResponse.response_200("Сервис временно недоступен.")
            
            dump_name = request_pack.name
            #logger.info(f'Request dump: {dump_name}')
            if os.path.exists(f"Dumps/{dump_name}"):
                with open(f"Dumps/{dump_name}", 'r', encoding="UTF-8") as fl:
                    text_dump = fl.read()
                    #logger.info(f'Returning dump with name: {dump_name}')
                    return RestResponse.response_200(str(text_dump))
            #logger.info(f'Is no dump named: {dump_name}')

            return RestResponse.response_200("Текстовый файл с таким именем не найден.")
    
    


