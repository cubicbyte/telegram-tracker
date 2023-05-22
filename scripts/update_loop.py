import time
import os
import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)
os.chdir(sys.path[0])

from src.utils.load_config import load_config
from src.database import Database

config = load_config('config.yml')
db = Database(**config['database'])

while True:

    db.execute_query('CALL updateUsers();')
    time.sleep(60)

