import uuid
import hashlib


def hash_password(text):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ":" + salt


def check_password(hashedText, providedText):
    _hashedText, salt = hashedText.split(":")
    return (
        _hashedText == hashlib.sha256(salt.encode() + providedText.encode()).hexdigest()
    )
