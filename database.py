import sqlite3
from typing import Optional
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
    status_expires: Optional[datetime]
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    phone: Optional[str]

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
    def get_user(self, user_id: int) -> Optional[User]:
        pass


class MySQLDatabase(BaseDatabase):

    connection = None

    def __init__(self, *args, **kwargs):
        self.connection = connect(*args, **kwargs)

    def handle_user_update(self, user: User):
        with self.connection.cursor() as cur:
            cur.callproc('updateUser', (user.id,))
            cur.callproc('handleUserUpdate', [*user])
            cur.callproc('saveUserUpdate', (user.id,))  # TODO: remove user update logging
        self.connection.commit()

    def get_user(self, user_id: int) -> Optional[User]:
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            res = cur.fetchone()

        if res is None:
            return None

        return User(*res)


class SQLiteDatabase(BaseDatabase):

    connection = None

    _GET_USER_SQL = 'SELECT * FROM users WHERE id = ?'
    _SET_OFFLINE_SQL = 'UPDATE users SET status_online = 0, status_time = ?, status_expires = NULL WHERE id = ?'
    _RENEW_EXPIRATION_SQL = 'UPDATE users SET status_expires = ? WHERE id = ?'
    _UPDATE_USER_SQL = """
        UPDATE users SET
            status_online = ?,
            status_time = ?,
            status_expires = ?,
            username = ?,
            first_name = ?,
            last_name = ?,
            phone_number = ?
        WHERE id = ?
    """
    _CREATE_USER_UPDATE_SQL = """
        INSERT INTO updates (
            id,
            state,
            time
        ) VALUES (?, ?, ?)
    """
    _CREATE_USER_SQL = """
        INSERT INTO users (
            id,
            status_online,
            status_time,
            status_expires,
            username,
            first_name,
            last_name,
            phone_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row

    def _result_to_user(self, res: sqlite3.Row) -> User:
        return User(
            id=res['id'],
            status_online=bool(res['status_online']),
            status_time=datetime.fromisoformat(res['status_time']),
            status_expires=datetime.fromisoformat(res['status_expires']) if res['status_expires'] else None,
            username=res['username'],
            first_name=res['first_name'],
            last_name=res['last_name'],
            phone=res['phone_number'],
        )

    def _update_user(self, user: User):
        cur = self.connection.execute(self._GET_USER_SQL, (user.id,))
        res = cur.fetchone()

        if res is None:
            self.connection.execute(self._CREATE_USER_SQL, [*user])
            self.connection.commit()
            return

        old_user = self._result_to_user(res)

        if old_user.status_online and old_user.status_expires < datetime.now().astimezone(tz=None):
            self.connection.execute(self._SET_OFFLINE_SQL, (res['status_expires'], user.id,))

        self.connection.commit()

    def _create_user_update(self, user: User):
        cur = self.connection.execute(self._GET_USER_SQL, (user.id,))
        res = cur.fetchone()

        if res is None:
            raise ValueError(f'User {user.id} does not exist')

        old_user = self._result_to_user(res)

        if old_user.status_online == user.status_online:
            if user.status_online:
                self.connection.execute(self._RENEW_EXPIRATION_SQL, (user.status_expires, user.id,))
        else:
            self.connection.execute(self._CREATE_USER_UPDATE_SQL, [*user.status])
            self.connection.execute(self._UPDATE_USER_SQL, [*user, user.id][1:])

        self.connection.commit()

    def handle_user_update(self, user: User):
        self._update_user(user)
        self._create_user_update(user)

    def get_user(self, user_id: int) -> Optional[User]:
        cur = self.connection.execute(self._GET_USER_SQL, (user_id,))
        res = cur.fetchone()

        if res is None:
            return None

        return self._result_to_user(res)
