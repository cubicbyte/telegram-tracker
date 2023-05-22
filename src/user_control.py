from .database import Database
from datetime import datetime

class UserControl:
    def __init__(self, db: Database) -> None:
        self.db = db

    def set_status(self, user_id: int, status: bool, expires: datetime | None = None) -> None:
        expires = expires if expires != None else datetime.now()
        query = 'CALL setUserStatus(%s, %s, "%s");' % (user_id, status, expires.strftime('%Y-%m-%d %H:%M:%S'))

        self.db.execute_query(query)

    def make_online(self, user_id: int, expires: datetime) -> None:
        self.set_status(user_id, True, expires)

    def make_offline(self, user_id: int) -> None:
        self.set_status(user_id, False)

