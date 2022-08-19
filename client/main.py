import os.path
import time
import logging

from telethon import types
from telethon.sync import TelegramClient, events
from src.utils.init_dirs import init_dirs
from src.utils.load_config import load_config
from src.database import Database
from src.user_control import UserControl



cwd = os.path.dirname(__file__)
config = load_config(os.path.join(cwd, 'config.yml'))

init_dirs(cwd)

logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(cwd, 'logs/debug.log'),
    filenode='a',
    format='%(asctime)s [%(levelname)s] - %(message)s'
)

logging.info('Starting application')

db = Database(**config['database'])
client = TelegramClient('sessions/Angron42', config['telegram']['api-id'], config['telegram']['api-hash'])
user_control = UserControl(db)

@client.on(events.UserUpdate)
async def user_update_handler(event):
    if not isinstance(event.original_update, types.UpdateUserStatus):
        return

    user_id = event.original_update.user_id
    is_online = isinstance(event.status, types.UserStatusOnline)

    user_control.set_status(
        user_id,
        is_online,
        event.status.expires.astimezone(tz=None) if is_online else None
    )

def telethon_loop():
    logging.info('Connecting to telegram...')

    try:
        client.start()
        logging.info('Connected to telegram succesfully')
        client.run_until_disconnected()

    except ConnectionError:
        logging.critical('Telethon connection error.')
        time.sleep(60)
        telethon_loop()

telethon_loop()
