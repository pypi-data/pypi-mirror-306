from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError

from pydantic import ValidationError

from ...Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ...Application.Abstractions.base_service import BaseServiceFWDI
from ...Application.DTO.Auth.model_user import User
from ...Application.DTO.Auth.token_data import TokenData
from ...Persistence.manager_db_context import ManagerDbContextFWDI
from ...Utilites.ext_jwt import JwtTools, SECRET_KEY, ALGORITHM

class JwtServiceFWDI(BaseServiceFWDI):
    oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    #def authenticate_user(db_context:BaseUserRepositoryFWDI, username: str, password: str, test:str = "Hello World !"):
    def authenticate_user(db_context:BaseUserRepositoryFWDI, username: str, password: str):
        user = JwtTools.get_user_by_username(db_context, username)
        if not user:
            return False
        if not JwtTools.verify_password(password, user.hashed_password):
            return False
        
        return user
    
    @staticmethod
    async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            email: str = payload.get("email")
            if username is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username, email=email)

        except (InvalidTokenError, ValidationError):
            raise credentials_exception
        
        users_db = ManagerDbContextFWDI().get_metadata_user()
        user = JwtTools.get_user_by_email(users_db, email=token_data.email)
        if user is None:
            raise credentials_exception
        
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
            
        return user
    
    @staticmethod
    async def get_current_active_user(current_user:User = Security(get_current_user),):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return current_user