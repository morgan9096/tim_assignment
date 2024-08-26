from mysql.connector import connect, Error

from utils.logger import log


class DbAdapter:
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password

        self.connection = None

    @property
    def is_connected(self):
        return self.connection is not None

    def connect(self):
        log.info(f'Connecting to MySQL db. Host={self.host}')
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
            ) as connection:
                self.connection = connection
                log.info(f'Connected to Mysql db: {self.host}')
                return connection
        except Error as e:
            log.error(e)

    def disconnect(self):
        self.connection.close()
        self.connection = None

    def execute(self, queries: list[str]):
        with self.connection.cursor as cursor:
            for query in queries:
                cursor.execute(query)
            self.connection.commit()
            result = cursor.fetchall()
        return result

    def create_db(self, db_name: str):
        self.execute([f'CREATE DATABASE {db_name}'])

    def get_tables(self, db_name: str) -> list[str]:
        return self.execute([f'use {db_name}', 'show tables'])

    def create_table(self, db_name: str, table_name: str, table_data: str):
        return self.execute([f'use {db_name}', f'CREATE TABLE {table_name} {table_data}'])

    def drop_table(self, db_name: str, table_name: str):
        return self.execute([f'use {db_name}', f'DROP TABLE {table_name}'])

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
