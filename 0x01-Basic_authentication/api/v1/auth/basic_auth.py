#!/usr/bin/env python3
""" BasicAuth module """
from .auth import Auth
from typing import TypeVar
from api.v1.views import User
import base64


class BasicAuth(Auth):
    """ A BasicAuth class that inherits same
    functionalities from a class Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ This returns Base64 part of
        the Authorization header for a Basic Authentication
        which starts with 'Basic ' space included
        """

        if isinstance(authorization_header, str):
            if authorization_header[:6] == 'Basic ':
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """ decodes the value of a Base64 string
        'base64_authorization_header'
        """

        if base64_authorization_header is None:
            return None

        if isinstance(base64_authorization_header, str):
            try:
                data = base64.b64decode(base64_authorization_header,
                                        validate=True)
                return data.decode("utf-8")
            except Exception:
                return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """ Returns user credentials:
        Username and email
        """

        if decoded_base64_authorization_header is None:
            return (None, None)

        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                split_data = decoded_base64_authorization_header.split(":")
                return (split_data[0], split_data[1])

        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """ Verifies and returns a
        Credible user present in database
        """
        if user_email is None or user_pwd is None:
            return None

        if isinstance(user_email, str) and isinstance(user_pwd, str):
            user = User.search({"email": user_email})
            if not user:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ User authentication Gateway"""

        if request is None:
            return None
        auth_data = self.authorization_header(request)

        if auth_data:
            user_raw_credentials = self.extract_base64_authorization_header(
                auth_data)

            if user_raw_credentials:
                user_credentials = self.decode_base64_authorization_header(
                    user_raw_credentials)

                if user_credentials:
                    user_info = self.extract_user_credentials(user_credentials)
                    user_email, user_password = user_info[0], user_info[1]
                    required_user = self.user_object_from_credentials(
                        user_email, user_password)
                    return required_user

        return None
