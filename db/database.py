from abc import ABC, abstractmethod


class Database(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_table(self, create_table_sql):
        pass

    @abstractmethod
    def insert_data(self, insert_sql, data):
        pass

    @abstractmethod
    def query_data(self, query_sql, params=()):
        pass

    @abstractmethod
    def close(self):
        pass