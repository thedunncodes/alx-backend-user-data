from flask import request
from typing import List, TypeVar


class Auth:
    """ Authorization Class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """

        return False

    def authorization_header(self, request=None) -> str:
        """ Authorizatio header
        """

        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """

        return request
