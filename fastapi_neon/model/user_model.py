from sqlmodel import Field , SQLModel



class UserBase(SQLModel):
    first_name:str = Field(index=True)
    last_name:str = Field(index=True)


class User(UserBase, table=True):
    id:int = Field(default=None,primary_key=True)
    email:str = Field(index=True, unique=True)
    password:str


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



