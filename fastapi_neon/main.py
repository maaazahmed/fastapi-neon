from sqlmodel import create_engine,select, Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException, status,Response
from fastapi_neon.model.model import UserResponse, UserCreate,User,TodoUpdate, UserLogin, Token, TokenData, TodoCreate, TodoResponse,Todos,  TodoBase
from typing import Annotated, List
from fastapi_neon.service import get_hashed_pass, verify_password,create_access_token, verify_token,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from  fastapi_neon  import settings
from  contextlib import asynccontextmanager



connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"""
    --------------------------------------------
    ======== | Welcome to FastAPI | ========  
        
                PORT    :        8000
                ---------------------
                HOST    :   localhost
                ---------------------
                ENV     :         DEV
                ---------------------
                STATUS  :     WORKING
        
            URL => http://localhost:8000 
    --------------------------------------------
    """)
    yield



app:FastAPI =  FastAPI(lifespan=lifespan, title="FastAPI Neon Todo API", version="2.0.0", servers=[
     {
        "url": "http://localhost:8000",
        "description": "Local server"
    }
])






def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "World", "message":"Welcome to FastAPI", }


@app.post("/signup", response_model=Token)
async def create_user(user:UserCreate, db:Annotated[Session, Depends(get_session)]):
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
async def login_user(login_data:UserLogin, db:Annotated[Session,Depends(get_session)],response: Response):
    statement = select(User).where(User.email == login_data.email)
    user = db.exec(statement).first()
    if user is not None:
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=404, detail="Invalid email or password!") 
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"email":user.email, "id":user.id}, expires_delta=access_token_expires)
            token_type="bearer"
            response.headers["authorization"] = access_token
            response.headers["type"] = token_type
            return Token(access_token=access_token, token_type=token_type)
    else:
        raise HTTPException(status_code=404, detail="User not found") 







@app.get("/user", response_model=UserResponse)
async def get_user(db:Annotated[Session, Depends(get_session)],token_data:Annotated[TokenData, Depends(verify_token)]):
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




@app.post("/todo", response_model=TodoResponse)
async def create_todo(todo:TodoCreate, db:Annotated[Session, Depends(get_session)],token_data:Annotated[TokenData, Depends(verify_token)]):
        db_user = db.get(User ,token_data.id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_todo = Todos.model_validate(todo)
        db_todo.user = db_user
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo






@app.patch("/todo{id}", response_model=TodoResponse, dependencies=[Depends(verify_token)])
async def update_todo(todo:TodoUpdate,id:int,  db:Annotated[Session, Depends(get_session)]):
        db_todo = db.get(Todos ,id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="User not found")
        todo_data = todo.model_dump(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo





@app.get("/todos", response_model=List[TodoResponse])
async def read_todos(db:Annotated[Session, Depends(get_session)],token_data:Annotated[TokenData, Depends(verify_token)]):
        statement = select(Todos).where(Todos.user_id == token_data.id)
        result = db.exec(statement).all()
        return result





@app.get("/todo/{id}", response_model=TodoResponse, dependencies=[Depends(verify_token)])
async def read_todo(id:int, db:Annotated[Session, Depends(get_session)]):
        try:
           item = db.get(Todos, id)  
           return item
        except:
            raise HTTPException(status_code=404, detail="Item Not found")





@app.delete("/todo/{id}",dependencies=[Depends(verify_token)])
async def delete_todo(id:int, db:Annotated[Session, Depends(get_session)]):
        item = db.get(Todos, id)
        if not item:
            raise HTTPException(status_code=404, detail="item not found")
        db.delete(item)
        db.commit()
        return {"message":"Successfully removed"}
       












        

