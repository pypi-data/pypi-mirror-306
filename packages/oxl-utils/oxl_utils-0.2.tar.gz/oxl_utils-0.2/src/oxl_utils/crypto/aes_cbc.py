#!/usr/bin/env python3

from base64 import b64encode, b64decode
from hashlib import sha256
from os import environ
from sys import argv as sys_argv

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from ..state import is_null


def __key(secret: str = None) -> bytes:
    if is_null(secret):
        secret = environ['CRYPTO_SECRET']

    return sha256(secret.encode('utf-8')).digest()


def encrypt(plaintext: str, secret: str = None) -> str:
    if is_null(plaintext):
        return ''

    try:
        return encrypt_bytes(
            plaintext=plaintext.encode('utf-8'),
            secret=secret,
        ).decode('utf-8')

    except ValueError as err:
        print(f"Got error encrypting plaintext: '{err}'")
        return ''


def encrypt_bytes(plaintext: bytes, secret: str = None) -> bytes:
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(__key(secret), AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(
        plaintext=pad(
            data_to_pad=plaintext,
            block_size=AES.block_size,
            style='pkcs7',
        ),
    )
    return b64encode(ciphertext)


def decrypt(ciphertext: str, secret: str = None) -> str:
    if is_null(ciphertext):
        return ''

    try:
        return decrypt_bytes(
            ciphertext=ciphertext.encode('utf-8'),
            secret=secret,
        ).decode('utf-8')

    except ValueError as err:
        print(f"Got error decrypting ciphertext: '{err}'")
        return ''


def decrypt_bytes(ciphertext: bytes, secret: str = None) -> bytes:
    ciphertext = b64decode(ciphertext)
    cipher = AES.new(__key(secret), AES.MODE_CBC, ciphertext[:AES.block_size])
    return unpad(
        padded_data=cipher.decrypt(ciphertext[AES.block_size:]),
        block_size=AES.block_size,
        style='pkcs7',
    )


if __name__ == '__main__':
    print('Encrypted:', encrypt(sys_argv[1]))
