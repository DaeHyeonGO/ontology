import pymysql
from pymysql.cursors import DictCursor

class BaseDAO:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def get_connection(self):
        if self.connection is None or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=DictCursor,
                charset='utf8mb4'
            )
        return self.connection
    
    def close_connection(self):
        if self.connection and self.connection.open:
            self.connection.close()