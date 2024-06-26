#!/usr/bin/env python3
""" SessionAuth module """
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ A SessionAuth class that inherits same
    functionalities from a class Auth and
    also provides session auth type functions
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates A session ID for a
        'user_id'
        Return:
          - Session id
        """

        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retreives a user through a session_id
        Returns:
          - User
        """

        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """ User authentication Gateway"""

        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        """

        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session_id)
        return True
