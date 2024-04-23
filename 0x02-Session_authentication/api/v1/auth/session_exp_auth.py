#!/usr/bin/env python3
""" SessionExpAuth module """
from .session_auth import SessionAuth
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ A SessionExpAuth class that inherits same
    functionalities from a class SessionAuth and
    also provides session expiration functions
    """

    def __init__(self):
        """ SessionExpAuth init method"""

        duration = getenv("SESSION_DURATION")
        if duration:
            try:
                self.session_duration = int(duration)
            except TypeError:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates A session dict for a
        'user_id' (overload of baseclass)
        using session id from baseclass
        Return:
          - Session id
        """

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] =\
            {'user_id': user_id, 'created_at': datetime.now()}

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
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if not session_dictionary.get('created_at'):
            return None
        session_time = session_dictionary.get('created_at') +\
            timedelta(seconds=self.session_duration)

        if session_time < datetime.now():
            return None
        return session_dictionary.get('user_id')
