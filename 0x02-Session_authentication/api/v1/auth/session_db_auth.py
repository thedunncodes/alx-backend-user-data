#!/usr/bin/env python3
""" SessionDBAuth module """
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ A SessionDBAuth class that inherits same
    functionalities from a class SessionExpAuth and
    also provides database functions
    """

    def create_session(self, user_id=None):
        """ Creates A UserSession instance for a
        'user_id' (overload of baseclass)
        using session id from baseclass
        Return:
          - Session id
        """

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        if user_session is None:
            return None
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retreives a user through a session_id
        and also times the duration till expiration
        Returns:
          - User
          - None if timeout
        """

        if session_id is None:
            return None
        try:
            user = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not user:
            return None
        if self.session_duration <= 0:
            return user[0].user_id
        session_time = user[0].created_at +\
            timedelta(seconds=self.session_duration)

        if session_time < datetime.now():
            return None

        return user[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the user session / logout
        """

        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = UserSession.search({"session_id": session_id})
        if not user_id:
            return False
        user_id[0].remove()
        return True
