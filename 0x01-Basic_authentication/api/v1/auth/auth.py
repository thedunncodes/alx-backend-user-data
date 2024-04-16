#!/usr/bin/env python3
""" Auth module """
from typing import List, TypeVar
from flask import Flask, request


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

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """

        return None
