import sqlite3
from abc import ABC
from sqlite3 import Error

from db.database import Database


class Sqlite3Database(Database, ABC):
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self, create_table_sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, insert_sql, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, data)
            self.connection.commit()
        except Error as e:
            print(f"Error inserting data: {e}")

    def query_data(self, query_sql, params=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query_sql, params)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error querying data: {e}")
            return []

    def close(self):
        if self.connection:
            self.connection.close()
