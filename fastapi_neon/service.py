from jose import  jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from fastapi import Header, HTTPException, status
from  typing import Annotated
from fastapi_neon.model.user_model import TokenData

SECRET_KEY = "090e3ba2a1d93d843715cb8cec50e1730e20991c62b04e7e249ef9b378d1490c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pass, hashed_pass):
   return pwd_context.verify(plain_pass, hashed_pass)





def get_hashed_pass(password):
  return pwd_context.hash(password)




def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)    
    return encode_jwt
       



def verify_token(token:Annotated[str, Header()]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="< Could not validate credentials >",
            headers={"WWW-Authenticat":"Bearer"}
        )
        try:
            payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM)
            email:str | None = payload.get("email") 
            if email is None:
                raise credentials_exception
            else:
                yield TokenData(email=email)
        except JWTError:
            raise credentials_exception
    
