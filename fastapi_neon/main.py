from typing import  Optional, Annotated
from  sqlmodel import SQLModel, create_engine, Session ,Field, select
from fastapi import FastAPI, Depends
from fastapi_neon import settings

app: FastAPI = FastAPI()

class Todo(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    content:str = Field(index=True)

db_url = str(settings.DATABASE_URL)


engine = create_engine(db_url, echo=True)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



@app.on_event("startup")
def on_startup():
    create_db_and_tables()



def get_deb():
    with Session(engine) as session:
        return session



@app.get("/")
def read_root():
    return {"Hello":"Hello"}



@app.post("/todos/")
def create_todo(todo:Todo, db:Annotated[Session, Depends(get_deb)]):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


# test-key
@app.get("/todod/")
def read_todos(db:Annotated[Session, Depends(get_deb)]):
    todos = db.exec(select(Todo)).all()
    return todos
    
