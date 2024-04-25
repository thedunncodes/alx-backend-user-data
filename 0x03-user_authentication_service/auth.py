#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hashes A password
    with Bcrypt
    """
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed_pw


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        if user:
            raise ValueError("User {} already exists.".format(user.email))
