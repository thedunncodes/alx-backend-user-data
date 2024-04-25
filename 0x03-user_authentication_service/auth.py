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
            hashed_pwd = _hash_password(password)
            user = User(email=email, hashed_password=hashed_pwd)
            self._db._session.add(user)
            self._db._session.commit()
            return user
        if user:
            raise ValueError("User {} already exists.".format(user.email))
