#!/usr/bin/python3
""" Database Engine for AirBNB_v2 clone """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


class DBStorage:
    """ Class manages storage to database """
    __engine = None
    __session = None

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if env == 'test':
            """Drop all db"""
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the database session, depending on the class name """

        if cls:
            return self.__session.query(cls.__name__).all()
        else:
            objects = [User, Place, State, City, Amenity, Review]
            """Query all types of object"""

            for obj in objects:
                self.__session.query(obj).all()
            q_res = {f'<class-name>.<object-id>'}

            return q_res

    def new(self, obj):
        """add new session
        """
        with self.__session() as session:
            session.add(obj)
            session.commit()

    def save(self):
        pass

    def delete(self, obj=None):

        pass

    def reload(self):
        """reloads from data storage engine
        """
        # from models import User, Place, State, City, Amenity, Review
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                self.__engine,
                expire_on_commit=False
            )
        )


    def close(self):
        """closes a session
        """
        self.__session.remove()
