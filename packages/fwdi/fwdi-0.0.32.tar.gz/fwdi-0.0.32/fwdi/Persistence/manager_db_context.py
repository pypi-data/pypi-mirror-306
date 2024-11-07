from ..Application.DTO.Repository.model_user import *
from ..Application.Abstractions.base_manager_context import BaseManagerContextFWDI


class ManagerDbContextFWDI(BaseManagerContextFWDI):

    def get_metadata_user(self) -> User:
        return User

    def get_metadata_permission(self) -> Permissions:
        return Permissions

    def get_metadata_scopes(self) -> Scope:
        return Scope