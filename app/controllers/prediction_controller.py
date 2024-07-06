from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil
from ..services.prediction_service import predict_image
from ..services.recipe_service import fetch_recipes
from ..middleware.auth import get_current_user  # Import from middleware module
from ..schemas.user_schema import User

router = APIRouter()

@router.post("/prediction")
async def predict_image_endpoint(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user)  # Adding the dependency for token validation
):
    try:
        with NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        class_name, confidence = predict_image(temp_file_path)
        
        # Fetch recipes based on the predicted class_name
        page, recipes, continuation_token = fetch_recipes(class_name)
        
        return JSONResponse(
            content={
                "class_name": class_name,
                "confidence": confidence,
                "recipes": recipes,
                "continuation_token": continuation_token,
            }
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        file.file.close()
