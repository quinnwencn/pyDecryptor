import pathlib

from crypto.decryptor import aes_decrypt
from crypto.keystore import read_key, store_key


def import_key(key_alias:str, key_file: str, password: str=None):
    if not pathlib.Path(key_file).exists():
        raise Exception("Key file not exists.")
    key = None
    if password is None:
        with open(key_file, 'rb') as fd:
            key = fd.read()
    else:
        if len(password) != 32:
            raise Exception(f"password length not valid")

        with open(key_file, 'rb') as fd:
            iv = fd.read(16)
            ciphertext = fd.read()

        key = aes_decrypt(bytes.fromhex(password), ciphertext, iv)

    pathlib.Path(key_file).unlink() # delete key file
    store_key(key_alias, key)

def decrypt(black_box: str, alias: str):
    if not pathlib.Path(black_box).exists():
        raise Exception("blackbox not exists.")

    key = read_key(alias)
    if key is None:
        raise Exception(f"No key alias named {alias}")

    with open(black_box, "rb") as fd:
        iv = fd.read(16)
        ciphertext = fd.read()

    plaintext = aes_decrypt(key, ciphertext, iv)
    decrypt_file = black_box + ".decrypt"
    with open(decrypt_file, "wb") as fd:
        fd.write(plaintext)