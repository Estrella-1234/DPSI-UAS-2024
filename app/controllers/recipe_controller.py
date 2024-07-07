from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..schemas.recipe_schema import RecipeCreate, Recipe
from ..services.recipe_service import fetch_recipes, save_recipe, delete_recipe
from ..middleware.auth import get_current_user
from ..core.database import get_db
from ..schemas.user_schema import User
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/recipes", response_model=List[Recipe])
def fetch_recipes_endpoint(
    q: str, 
    _cont: Optional[str] = Query(None), 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    try:
        page, recipes, continuation_token = fetch_recipes(q, _cont)
        return JSONResponse(
            content={
                "page": page,
                "recipes": recipes,
                "continuation_token": continuation_token,
            }
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/recipes", response_model=Recipe)
def save_recipe_endpoint(
    recipe: RecipeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return save_recipe(db, recipe, current_user.id)

@router.delete("/recipes/{recipe_id}", response_model=Recipe)
def delete_recipe_endpoint(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_recipe = delete_recipe(db, recipe_id, current_user.id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe
