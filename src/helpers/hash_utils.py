import hashlib
import secrets

def generate_salt():
    return secrets.token_hex(8)

def hash(password:str, salt:str):
    """takes unhashed password and salt
    Args:
        password (str): _description_
        salt (str): _description_
    Returns:
        string: hashed password in hexadecimal digit
    """
    salted_password = password + salt
    hashed = hashlib.sha256(salted_password.encode())
    return hashed.hexdigest()  