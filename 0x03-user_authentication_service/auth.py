#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hashes A password
    with Bcrypt
    """
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed_pw
