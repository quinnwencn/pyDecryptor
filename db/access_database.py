import pathlib
import uuid

from db.database import Database
from db.sqlitedatabase import Sqlite3Database


def _get_home_path():
    return pathlib.Path.home()

def get_database(db_type: str, **kwargs):
    db = None
    if db_type == "sqlite":
        db_dir = _get_home_path() / pathlib.Path(".decryptor")
        db_dir.mkdir(exist_ok=True)
        db_path = db_dir / kwargs.get("db_file")
        db = Sqlite3Database(db_path)


    create_table_sql = """
    CREATE TABLE IF NOT EXISTS keys (
        keyId VARCHAR(255) PRIMARY KEY,
        keyAlias VARCHAR(255) NOT NULL,
        key BLOB NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(keyAlias)
    );"""
    db.create_table(create_table_sql)

    return db

def insert_new_key(db: Database, key_alias, key, description: str=None):
    key_id = uuid.uuid4()
    id = str(key_id).replace('-', '')
    insert_sql = """
    INSERT INTO keys (keyId, keyAlias, key, description) VALUES(?, ?, ?, ?);
    """

    db.insert_data(insert_sql, (id, key_alias, key, description))

def read_key_by_alias(db : Database, key_alias):
    query_sql = """
    SELECT key FROM keys WHERE keyAlias = ?;
    """
    result = db.query_data(query_sql, (key_alias,))
    key = None
    if result:
        key = result[0][0]

    db.close()
    return key




