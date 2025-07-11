from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Del(BaseModel):
    id: int
    username: str