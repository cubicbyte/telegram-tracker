import os
import telethon
from datetime import datetime
from telethon import events
from telethon.types import UpdateUserStatus, UserStatusOnline
from dotenv import load_dotenv
from database import MySQLDatabase, User

load_dotenv()

_db_type = os.getenv('DB_TYPE')
if _db_type == 'mysql':
    db = MySQLDatabase(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'),
    )
else:
    raise NotImplementedError(f'Unknown database type: {_db_type}')

client = telethon.TelegramClient('status-collector', int(os.getenv('API_ID')), os.getenv('API_HASH'))
update_event = events.UserUpdate()
_log_user_updates = os.getenv('LOG_USER_UPDATES', 'false').lower() == 'true'


@client.on(update_event)
async def handle_user_update(event: events.userupdate.UserUpdate.Event):
    if not isinstance(event.original_update, UpdateUserStatus):
        return

    _user = await client.get_entity(event.original_update.user_id)
    is_online = isinstance(event.original_update.status, UserStatusOnline)
    time = datetime.now() if is_online else event.original_update.status.was_online
    expires = event.original_update.status.expires if is_online else None

    user = User(
        id=_user.id,
        status_online=is_online,
        status_time=time,
        status_expires=expires,
        username=_user.username,
        first_name=_user.first_name,
        last_name=_user.last_name,
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
    with client:
        try:
            client.run_until_disconnected()
        except (KeyboardInterrupt, SystemExit):
            pass
