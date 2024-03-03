#!/usr/bin/env python3

import os
import emoji
import telethon
from time import sleep
from datetime import datetime
from telethon import events
from telethon import types
from dotenv import load_dotenv
from database import MySQLDatabase, SQLiteDatabase, User

load_dotenv()

os.environ.setdefault('DB_TYPE', 'sqlite')
os.environ.setdefault('DB_PATH', 'database.sqlite')
os.environ.setdefault('ESCAPE_EMOJIS', 'false')
os.environ.setdefault('LOG_USER_UPDATES', 'false')

assert os.getenv('API_ID') is not None, 'API_ID is not set in .env file'
assert os.getenv('API_HASH') is not None, 'API_HASH is not set in .env file'
assert os.getenv('API_ID').isdigit(), 'API_ID is not a number'

_db_type = os.getenv('DB_TYPE').lower()
if _db_type == 'mysql':
    db = MySQLDatabase(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'),
    )
elif _db_type == 'sqlite':
    db = SQLiteDatabase(
        path=os.getenv('DB_PATH'),
    )
else:
    raise NotImplementedError(f'Unknown database type: {_db_type}')

client = telethon.TelegramClient('status-collector', int(os.getenv('API_ID')), os.getenv('API_HASH'))
update_event = events.UserUpdate()
_log_user_updates = os.getenv('LOG_USER_UPDATES').lower() == 'true'
_escape_emojis = os.getenv('ESCAPE_EMOJIS').lower() == 'true'


@client.on(update_event)
async def handle_user_update(event: events.userupdate.UserUpdate.Event):
    if not isinstance(event.original_update, types.UpdateUserStatus):
        return

    _user = await client.get_entity(event.original_update.user_id)
    is_online = isinstance(event.original_update.status, types.UserStatusOnline)
    is_known = is_online or isinstance(event.original_update.status, types.UserStatusOffline)
    time = datetime.now().astimezone(tz=None) if is_online or not is_known else \
           event.original_update.status.was_online.astimezone(tz=None)
    expires = event.original_update.status.expires.astimezone(tz=None) if is_online else None

    if _escape_emojis:
        first_name = emoji.demojize(_user.first_name)
        last_name = emoji.demojize(_user.last_name) if _user.last_name else None
    else:
        first_name = _user.first_name
        last_name = _user.last_name

    user = User(
        id=_user.id,
        status_online=is_online,
        status_time=time,
        status_expires=expires,
        username=_user.username,
        first_name=first_name,
        last_name=last_name,
        phone=_user.phone,
    )

    if _log_user_updates:
        log_user_update(user)
    db.handle_user_update(user)


def log_user_update(user: User):
    status = '✅' if user.status_online else '❌'
    name = f'{user.first_name} {user.last_name}' if user.last_name else user.first_name

    # ✅ John Doe
    print('%s %s' % (status, name))


if __name__ == '__main__':
    while True:
        try:
            with client:
                client.run_until_disconnected()
        except (KeyboardInterrupt, SystemExit):
            print('Exiting...')
            break
        except Exception as e:
            print(e)
            sleep(30)
