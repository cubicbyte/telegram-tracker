import logging
import mysql.connector
from datetime import datetime, timedelta

class Database:
    __reconnect_delay = timedelta(seconds=30)
    __last_connection_try = datetime.now()
    __connection_params = None

    connection = None

    def __init__(self, **kwargs) -> None:
        self.connect(**kwargs)

        self.execute_query = self.__handle_error('Query execution error: %s')(self.execute_query)
        self.execute_read_query = self.__handle_error('Query execution error: %s')(self.execute_read_query)
        self.execute_multi_query = self.__handle_error('Query execution error: %s')(self.execute_multi_query)

    def __handle_error(self, msg: str = 'Error: %s'):
        def decorator(func):
            def inner(*args, **kwargs):
                try:
                    if self.connection == None:
                        raise mysql.connector.Error('Connection not established')
                    result = func(*args, **kwargs)
                    return result
                
                except mysql.connector.Error as e:
                    logging.error(msg % e)
                    if self.connection == None or not self.connection.is_connected():
                        cur_time = datetime.now()

                        if self.__last_connection_try + self.__reconnect_delay < cur_time:
                            self.connect(**self.__connection_params)
                            self.__last_connection_try = cur_time

                    return False

            return inner

        return decorator
        


    def connect(self, **kwargs) -> bool:
        logging.info('Connecting to MySQL database...')

        try:
            if self.__connection_params == None:
                self.__connection_params = kwargs

            self.connection = mysql.connector.connect(**kwargs)

        except mysql.connector.Error as e:
            logging.critical(f'Can\'t connect to MySQL database: {e}')
            return False

        else:
            logging.info('Connected to MySQL database successfully')
            self.__connection_params = kwargs
            return True

    def execute_query(self, query: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
        return True

    def execute_multi_query(self, query: str) -> list:
        cursor = self.connection.cursor()
        result = cursor.execute(query, multi=True)

        fetch_result = []
        for cursor in result:
            if cursor.with_rows:
                fetch_result.append(cursor.fetchall())

        return fetch_result

    def execute_read_query(self, query: str) -> list | bool:
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result

