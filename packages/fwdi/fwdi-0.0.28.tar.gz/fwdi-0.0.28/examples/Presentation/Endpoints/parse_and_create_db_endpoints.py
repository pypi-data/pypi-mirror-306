from fastapi import Depends, Security
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from Application.Abstractions.base_usecase_context_data_base import BaseUsecaseContextDataBase
from Application.Usecases.usecase_context_database import UsecaseContextDataBase



class ParseEndpoint():
    def parse(usecase_create_db: UsecaseContextDataBase=Depends(), 
              current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
                    
        usecase_create_db.create_vectore_database()




        
