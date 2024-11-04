# pylint: disable=C0415


def test_aes_encrypt():
    from .aes_cbc import encrypt, decrypt
    plaintext = 'test'
    secret = 'SECRET123'

    ciphertext = encrypt(plaintext, secret=secret)

    assert len(ciphertext) > 40
    assert plaintext == decrypt(ciphertext, secret=secret)


def test_aes_decrypt():
    from .aes_cbc import decrypt
    plaintext = 'test'
    secret = 'SECRET123'
    ciphertext = 'CnV+6XggsbfXJAhLsM1MnvX2fsPqK9We5hOeoQeCWW4='

    assert plaintext == decrypt(ciphertext, secret=secret)


def test_aes_encrypt_bytes():
    from .aes_cbc import encrypt_bytes, decrypt_bytes
    plaintext = b'test'
    secret = 'SECRET123'

    ciphertext = encrypt_bytes(plaintext, secret=secret)

    assert len(ciphertext) > 40
    assert plaintext == decrypt_bytes(ciphertext, secret=secret)


def test_aes_decrypt_bytes():
    from .aes_cbc import decrypt_bytes
    plaintext = b'test'
    secret = 'SECRET123'
    ciphertext = b'CnV+6XggsbfXJAhLsM1MnvX2fsPqK9We5hOeoQeCWW4='

    assert plaintext == decrypt_bytes(ciphertext, secret=secret)
