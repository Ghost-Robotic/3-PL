import hashlib
import secrets

def generate_salt():
    return secrets.token_hex(8)

def hash(password:str, salt:str):
    salted_password = password + salt
    hashed = hashlib.sha256(salted_password.encode())
    return hashed.hexdigest()    