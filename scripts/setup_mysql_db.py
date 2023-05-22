
# Needed to import from parent directory
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))


from database import MySQLDatabase


def setup(db: MySQLDatabase):
    setup_file = os.path.join(os.path.dirname(__file__), '..', 'sql', 'setup.sql')
    with open(setup_file) as fp:
        setup_sql = fp.read()

    cur = db.connection.cursor()

    res = cur.execute(setup_sql, multi=True)
    if res is not None:
        for i in res:
            pass

    db.connection.commit()
    db.connection.close()


if __name__ == '__main__':
    import os

    setup(MySQLDatabase(
        host=os.getenv('DB_HOST') or input('DB_HOST: '),
        port=os.getenv('DB_PORT') or input('DB_PORT: '),
        user=os.getenv('DB_USER') or input('DB_USER: '),
        password=os.getenv('DB_PASSWORD') or input('DB_PASSWORD: '),
        database=os.getenv('DB_DATABASE') or input('DB_DATABASE: '),
    ))
