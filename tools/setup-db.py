import os
import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)
os.chdir(sys.path[0])

from src.utils.load_config import load_config
from src.database import Database

config = load_config('config.yml')

db_name = config['database']['database']
del config['database']['database']

db = Database(**config['database'])

with open('sql/setup-db.sql', 'r') as file:
    print('Executing queries...')

    query = file.read().format(
        db_name=db_name,
        users_table_name='users',
        statuses_table_name='statuses'
    )
    
    result = db.execute_multi_query(query)

    if result != False:
        print('Queries executed')

    file.close()
