from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(PWD_CONTEXT.hash("526c36c5-5177-494f-9388-d1f76a968572"))