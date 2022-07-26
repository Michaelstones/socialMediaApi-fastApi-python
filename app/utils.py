from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


def hashPW(password:str):
    return pwd_context.hash(password)

def verifyPWD(plain_pwd, password):
    return pwd_context.verify(plain_pwd, password)