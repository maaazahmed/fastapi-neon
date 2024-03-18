from sqlmodel import Field , SQLModel, Relationship
from typing import List, Optional, Union

class UserBase(SQLModel):
    first_name:str = Field(index=True)
    last_name:str = Field(index=True)


class User(UserBase, table=True):
    id:int = Field(default=None,primary_key=True)
    email:str = Field(index=True, unique=True,  )
    password:str
    todos: List["Todos"] = Relationship(back_populates="user")



class UserCreate(UserBase):
    email:str = Field(index=True, unique=True)
    password:str


class UserResponse(UserBase):
    id:int
    email:str


class UserLogin(SQLModel):
    email:str 
    password:str


class Token(SQLModel):
    access_token: str
    token_type: str



class TokenData(SQLModel):
    email:str
    id:Optional[int] = None





class TodoBase(SQLModel):
    title:str = Field(index=True)
    description:str
    



class Todos(TodoBase, table=True):
     id:int = Field(default=None, primary_key=True)
     status:str = Field(default="pending")
     user:Optional[User] = Relationship(back_populates="todos")
     user_id:Optional[int] = Field(default=None, foreign_key="user.id")




class TodoCreate(TodoBase):
    pass
    # user_id:Optional[int] = Field(default=None, foreign_key="user.id")


class TodoResponse(TodoBase):
     id:int = Field(default=None, primary_key=True)
     user_id:int
     status:Optional[str]
     
     


class TodoUpdate(SQLModel):
    status:Optional[str] = None
    title:Optional[str] = None
    description:Optional[str] = None



