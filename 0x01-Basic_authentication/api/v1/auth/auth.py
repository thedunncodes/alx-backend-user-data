#!/usr/bin/env python3
""" Auth module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authorization Class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """

        if path is None or excluded_paths is None or not excluded_paths:
            return True

        for paths in excluded_paths:
            if paths[-1] == '/':
                if path == paths[:-1]:
                    return False
            if paths == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """

        return None
