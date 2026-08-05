from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    role: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class NoteCreate(BaseModel):
    title: str
    body: str
    category_id: int | None = None


class NoteUpdate(BaseModel):
    title: str
    body: str
    category_id: int | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    owner: UserResponse
    category: CategoryResponse | None = None

    model_config = ConfigDict(from_attributes=True)
    
class CategoryUpdate(BaseModel):
    name: str