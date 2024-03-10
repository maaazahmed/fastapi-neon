from sqlmodel import create_engine,select, Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi_neon.model.user_model import UserResponse, UserCreate,User, UserLogin, Token, TokenData
from typing import Annotated
from fastapi_neon.service import get_hashed_pass, verify_password,create_access_token, verify_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
# from  dotenv import dotenv_values

app:FastAPI =  FastAPI()

db_url = "postgresql://maaazahmed:ySmszr3GV7jp@ep-late-scene-a1ra8ckq.ap-southeast-1.aws.neon.tech/sql-model?sslmode=require"
# db_url = dotenv_values(".env").get(dotenv_values("DATABASE_URL"))
engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_deb():
    with Session(engine) as session:
        return session




@app.post("/signup", response_model=Token)
async def create_user(user:UserCreate, db:Annotated[Session, Depends(get_deb)]):
    statement = select(User).where(User.email == user.email)
    is_user = db.exec(statement).first()
    if is_user is not None :
        raise HTTPException(status_code=404, detail="Email already in use!")
    else:    
        user.password = get_hashed_pass(user.password)
        validate_user = User.model_validate(user)
        db.add(validate_user)
        db.commit()
        db.refresh(validate_user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"email":validate_user.email}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type="bearer")
    




@app.post("/login", response_model=Token)
async def login_user(login_data:UserLogin, db:Annotated[Session,Depends(get_deb)]):
    statement = select(User).where(User.email == login_data.email)
    user = db.exec(statement).first()
    if user is not None:
        if not verify_password(login_data.password,user.password):
            raise HTTPException(status_code=404, detail="Invalid email or password!") 
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"email":user.email}, expires_delta=access_token_expires)
            return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=404, detail="User not found") 




@app.get("/user", response_model=UserResponse)
async def get_user(db:Annotated[Session, Depends(get_deb)],token_data:Annotated[TokenData, Depends(verify_token)]):
    print("token: ", token_data)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticat":"Bearer"}
    )
    if token_data.email is None:
        raise credentials_exception
    statement = select(User).where(User.email == token_data.email)
    response = db.exec(statement).one()
    if not response:
        raise credentials_exception
    return response

