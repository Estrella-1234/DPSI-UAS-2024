from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from ..services.recipe_service import fetch_recipes
from ..schemas.user_schema import User
from ..middleware.auth import get_current_user  # Import from middleware module

router = APIRouter()

@router.get("/recipes")
def fetch_recipes_endpoint(
    q: str, 
    _cont: Optional[str] = Query(None), 
    current_user: User = Depends(get_current_user)  # Adding the dependency for token validation
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
