from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_rsa(private_key, encrypted_data, padding=padding.PKCS1v15()):
    plaintext = private_key.decrypt(
        encrypted_data,
        padding
    )
    return plaintext