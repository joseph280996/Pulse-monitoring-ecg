from mysql import connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from operator import itemgetter
from os import environ

load_dotenv()


class DB():
    def __init__(self):
        try:
            host, database, user, password = itemgetter(
                'host', 'database', 'user', 'password')(environ)
            base_config = {
                'poolname': 'pulse-monitoring-app',
                'pool_size': 3
            }
            self.connection = connector.pooling.MySQLConnectionPool(
                host=host, database=database, user=user, password=password, **base_config)
            self.cursor = self.connection.cursor()

        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid username/password provided")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor.close()
            self.connection.close()

    def query(self, query: str, variables: dict):
        self.cursor.execute(query.format(**variables))
        return self.cursor

    def cleanup(self):
        if self.connection:
            self.connection.close()
