from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from crypto.aes_decryptor import aes_decrypt
from crypto.keystore import read_key, store_key
from cmd_parser.tlv_reader import TLVReader
from crypto.rsa_decryptor import decrypt_rsa


def import_key(key_alias:str, key_file: str, password: str=None):
    key_path = Path(key_file)
    if not key_path.exists():
        raise Exception("Key file not exists.")
    key = None
    if password is None:
        with open(key_file, 'rb') as fd:
            key = fd.read()
    else:
        encrypted_priv_key = key_path.read_bytes()
        key = load_pem_private_key(encrypted_priv_key, password.encode("utf-8"))

    key_path.unlink() # delete key file
    pem_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # 不加密
    )
    store_key(key_alias, pem_bytes)

def decrypt(black_box: str, alias: str):
    if not Path(black_box).exists():
        raise Exception("blackbox not exists.")

    rsa_key_bytes = read_key(alias)
    rsa_key = serialization.load_pem_private_key(
        rsa_key_bytes,
        password=None,  # 如果私钥是加密的，需要提供密码
        backend=default_backend()
    )
    if rsa_key is None:
        raise Exception(f"No key alias named {alias}")

    tlv = TLVReader(black_box)
    encrypted_key = tlv.get_value_by_type(0x5555)
    iv = tlv.get_value_by_type(0xaaaa)
    ciphertext = tlv.get_value_by_type(0x55aa)

    key = decrypt_rsa(rsa_key, encrypted_key)
    plaintext = aes_decrypt(key, ciphertext, iv)
    decrypt_file = black_box + ".decrypt"
    with open(decrypt_file, "wb") as fd:
        fd.write(plaintext)