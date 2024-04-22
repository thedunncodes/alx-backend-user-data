#!/usr/bin/env python3
""" Auth module """
from flask import request
from typing import List, TypeVar
from os import getenv


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

            last_path_index = paths.rfind("/")
            delimitter_index = paths.find("*")

            if delimitter_index == -1:
                delimitter_index = False

            if delimitter_index:
                delimitter_string = paths[last_path_index:delimitter_index]
                if delimitter_string in path and delimitter_string in paths:
                    return False

            if paths == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """

        if request is None or not request.headers.get('Authorization'):
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """

        return None

    def session_cookie(self, request=None):
        """ Session cookie
        Return:
          - Cookie value
        """
        if request is None:
            return None

        session_name = getenv('SESSION_NAME')
        cookie_value = request.cookies.get(session_name)
        return cookie_value
