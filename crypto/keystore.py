import win32crypt

from db.access_database import get_database, insert_new_key, read_key_by_alias


def _store_key_to_key_store(key_alias, key_data):
    if isinstance(key_alias, bytes):
        key_alias = key_alias.decode('utf-8')
    print(type(key_alias))
    print(type(key_data))
    protected_key = win32crypt.CryptProtectData(key_data, key_alias, None, None, None, 0)
    print(f"Key {key_alias} has been stored in Key Store.")
    return protected_key

def _read_key_from_keystore(encrypt_key):
    decrypted_data =  win32crypt.CryptUnprotectData(encrypt_key, None, None, None, 0)
    return decrypted_data

def store_key(key_alias, key_data, description:str=None):
    db = get_database("sqlite", db_file="keystore")
    encrypt_data = _store_key_to_key_store(key_alias, key_data)
    insert_new_key(db, key_alias, encrypt_data, description)

def read_key(key_alias):
    db = get_database("sqlite", db_file="keystore")
    encrypt_data = read_key_by_alias(db, key_alias)
    (alias, key) = _read_key_from_keystore(encrypt_data)
    if alias != key_alias:
        print("illegal key alias return")
        return None

    return key
