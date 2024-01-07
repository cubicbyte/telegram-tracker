#!/usr/bin/env python3
# Needed to import from parent directory
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import os

from database import SQLiteDatabase


def setup(db: SQLiteDatabase):
    setup_file = os.path.join(os.path.dirname(__file__), '..', 'sql', 'setup-sqlite.sql')

    with open(setup_file) as fp:
        setup_sql = fp.read()

    cur = db.connection.cursor()

    res = cur.executescript(setup_sql)
    if res is not None:
        for i in res:
            pass

    db.connection.commit()
    db.connection.close()


if __name__ == '__main__':
    import dotenv
    dotenv.load_dotenv()

    setup(SQLiteDatabase(
        path=os.getenv('DB_PATH') or input('DB_PATH: '),
    ))
