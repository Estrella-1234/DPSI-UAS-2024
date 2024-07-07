from pydantic import BaseModel
from typing import List, Optional

class RecipeBase(BaseModel):
    name: str
    image: str
    preparation_time: float
    calories: float
    ingredients: List[str]
    url: str

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode: True
