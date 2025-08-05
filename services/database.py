import mysql.connector
from mysql.connector import Error


class Database:
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = Database()
        return Database._instance

    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'abcd1234',
            'database': 'personal_budget_tracker'
        }

    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True, buffered=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = None
            if fetchone:
                result = cursor.fetchone()
            elif fetchall:
                result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid

            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()