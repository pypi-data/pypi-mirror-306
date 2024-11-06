from ...Application.Abstractions.base_user_repository import BaseUserRepositoryFWDI
from ..Abstractions.base_manager_context import BaseManagerContextFWDI

class UserRepositoryFWDI(BaseUserRepositoryFWDI):
    def get_all(self, manager_db_context: BaseManagerContextFWDI) -> list[dict]:
        users = manager_db_context.get_metadata_user()
        user_list = []
        for user in users:
            dct_user = {
                        'username': user.username,
                        'hashed_password': user.hashed_password,
                        'email': user.email
                        }
            user_list.append(dct_user)

        return user_list

    def get_user_scopes(self, email:str, manager_db_context: BaseManagerContextFWDI) -> list[str]:
        user = manager_db_context.get_metadata_user().get(manager_db_context.get_metadata_user().email == email)
        scopes_user = user.scopes.scopes_detail
        scopes = []
        for scope in scopes_user:
            scopes.append(scope.name)

        return scopes