from ..module.recipes import fetch_recipes as fetch_recipes_func
from typing import Optional

from sqlalchemy.orm import Session
from ..models.model import Recipe
from ..schemas.recepie_schema import RecipeCreate
import json

def fetch_recipes(query: str, continuation: Optional[str] = None):
    return fetch_recipes_func(query, continuation)


def save_recipe(db: Session, recipe: RecipeCreate, user_id: int):
    db_recipe = Recipe(
        name=recipe.name,
        image=recipe.image,
        preparation_time=recipe.preparation_time,
        calories=recipe.calories,
        ingredients=json.dumps(recipe.ingredients),  # Convert list to JSON string
        url=recipe.url,
        owner_id=user_id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int, user_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id, Recipe.owner_id == user_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
        return db_recipe
    return None