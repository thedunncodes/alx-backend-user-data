#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds a new user instance through
        User db schema
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """ Find user by ID
        """

        user_attr_dict = {}
        for k, v in kwargs.items():
            if hasattr(User, k):
                user_attr_dict[k] = v
            else:
                raise InvalidRequestError()
        session = self._session
        for key, value in user_attr_dict.items():
            query = session.query(User).filter(getattr(User, key) == value)
            user = query.one()
        if not user:
            raise NoResultFound()
        return user
