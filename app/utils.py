from passlib.context import CryptContext


pw_hash = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

def hash(password:str):
    return pw_hash.hash(password)


def verifyHash(password:str,hpassword:str):
    return pw_hash.verify(password,hpassword)

