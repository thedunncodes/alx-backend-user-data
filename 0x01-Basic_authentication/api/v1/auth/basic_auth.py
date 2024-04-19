#!/usr/bin/env python3
""" BasicAuth module """
from .auth import Auth
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
