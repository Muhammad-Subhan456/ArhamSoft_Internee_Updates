from pydantic import BaseModel, ConfigDict




class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)




class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    category_id: int | None = None


class TaskUpdate(BaseModel):
    title: str
    completed: bool
    category_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    
    category: CategoryResponse | None = None

    model_config = ConfigDict(from_attributes=True)