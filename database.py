from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, fields
from mysql.connector import connect


def _iterable(cls):
    """Adds __iter__ method to dataclass"""
    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)

    cls.__iter__ = __iter__
    return cls


@_iterable
@dataclass
class UserStatus:
    id: int
    online: bool
    time: datetime


@_iterable
@dataclass
class User:
    id: int
    status_online: bool
    status_time: datetime
    status_expires: datetime | None
    username: str | None
    first_name: str
    last_name: str | None
    phone: str | None

    @property
    def status(self) -> UserStatus:
        return UserStatus(
            id=self.id,
            online=self.status_online,
            time=self.status_time,
        )


class BaseDatabase(ABC):

    @abstractmethod
    def handle_user_update(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User | None:
        pass


class MySQLDatabase(BaseDatabase):

    connection = None

    def __init__(self, *args, **kwargs):
        self.connection = connect(*args, **kwargs)

    def handle_user_update(self, user: User):
        with self.connection.cursor() as cur:
            cur.callproc('updateUser', (user.id,))
            cur.callproc('handleUserUpdate', [*user])
            cur.callproc('saveUserUpdate', (user.id,))
        self.connection.commit()

    def get_user(self, user_id: int) -> User | None:
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            res = cur.fetchone()

        if res is None:
            return None

        return User(*res)
