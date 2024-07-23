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

# Endpoint untuk mengambil resep dari Edamam berdasarkan query yang diberikan
@router.get("/edamam-recipes", response_model=List[Recipe])
def fetch_recipes_endpoint(
    q: str,
    _cont: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),  # Memastikan hanya pengguna yang terautentikasi yang dapat mengakses
    db: Session = Depends(get_db)
):
    try:
        page, recipes, continuation_token = fetch_recipes(q, _cont)  # Memanggil fungsi untuk mengambil resep dari Edamam
        return JSONResponse(
            content={
                "page": page,
                "recipes": recipes,
                "continuation_token": continuation_token,
            }
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)  # Mengembalikan respon error jika terjadi kesalahan


# Endpoint untuk menyimpan resep yang diinginkan
@router.post("/recipes", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Memastikan hanya pengguna yang terautentikasi yang dapat mengakses
):
    try:
        db_recipe = RecipeModel(**recipe.dict(), owner_id=current_user.id)  # Membuat objek resep baru dengan data dari pengguna
        db.add(db_recipe)  # Menambahkan resep ke database
        db.commit()  # Menyimpan perubahan ke database
        db.refresh(db_recipe)  # Memperbarui objek resep dengan data dari database
        return {"message": "Recipe created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # Mengembalikan respon error jika terjadi kesalahan


# Endpoint untuk mengambil semua resep milik pengguna saat ini
@router.get("/recipes", response_model=List[Recipe])
def get_all_recipes(
        current_user: User = Depends(get_current_user),  # Memastikan hanya pengguna yang terautentikasi yang dapat mengakses
        db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).filter(RecipeModel.owner_id == current_user.id).all()  # Mengambil semua resep milik pengguna dari database
    return [recipe.to_dict() for recipe in recipes]  # Mengembalikan daftar resep dalam bentuk dictionary


# Endpoint untuk mengambil resep berdasarkan ID
@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe_by_id(
        recipe_id: int,
        current_user: User = Depends(get_current_user),  # Memastikan hanya pengguna yang terautentikasi yang dapat mengakses
        db: Session = Depends(get_db)
        ):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()  # Mengambil resep dari database berdasarkan ID
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")  # Mengembalikan error jika resep tidak ditemukan
    return recipe.to_dict()  # Mengembalikan resep dalam bentuk dictionary


# Endpoint untuk menghapus resep berdasarkan ID
@router.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe_endpoint(
        recipe_id: int,
        current_user: User = Depends(get_current_user),  # Memastikan hanya pengguna yang terautentikasi yang dapat mengakses
        db: Session = Depends(get_db)
):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id,
                                             RecipeModel.owner_id == current_user.id).first()  # Mengambil resep dari database berdasarkan ID dan pemiliknya
    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")  # Mengembalikan error jika resep tidak ditemukan

    db.delete(db_recipe)  # Menghapus resep dari database
    db.commit()  # Menyimpan perubahan ke database

    return {"message": "Recipe deleted successfully"}  # Mengembalikan pesan sukses
