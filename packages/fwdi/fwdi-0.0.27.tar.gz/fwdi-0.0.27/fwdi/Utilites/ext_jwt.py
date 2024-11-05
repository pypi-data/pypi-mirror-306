import jwt
import logging
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError

from ..Application.DTO.Auth.user_in_db import UserInDB
from ..Application.DTO.Auth.model_user import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

logging.getLogger('passlib').setLevel(logging.ERROR)

class JwtTools():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return JwtTools.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return JwtTools.pwd_context.hash(password)

    @staticmethod
    def get_user_by_username(db_context, username: str)-> UserInDB:
        user = [item for item in db_context if item['username'] == username]
        if len(user) > 0:
            user_dict = user[0]

            return UserInDB(**user_dict)

    @staticmethod
    def get_user_by_email(users_db:User, email: str)-> UserInDB:
        for user in users_db:
            if user.email == email:
                return UserInDB(**{
                        'username': user.username,
                        'hashed_password': user.hashed_password,
                        'email': user.email,
                        })

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt