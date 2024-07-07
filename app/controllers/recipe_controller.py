from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..schemas.recipe_schema import RecipeCreate, Recipe
from ..services.recipe_service import fetch_recipes, save_recipe, delete_recipe
from ..middleware.auth import get_current_user
from ..core.database import get_db
from ..schemas.user_schema import User
from fastapi.responses import JSONResponse
from ..models.model import Recipe as RecipeModel

router = APIRouter()

@router.get("/edamam-recipes", response_model=List[Recipe])
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



@router.post("/recipes", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        db_recipe = RecipeModel(**recipe.dict(), owner_id=current_user.id)
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return {"message": "Recipe created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get all recipes
@router.get("/recipes", response_model=List[Recipe])
def get_all_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).all()
    return recipes

# Get recipe by id
@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe_endpoint(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id, RecipeModel.owner_id == current_user.id).first()
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    
    return {"message": "Recipe deleted successfully"}
