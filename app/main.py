from fastapi import FastAPI

from .controllers import user_controller
from .controllers import recipe_controller
from .controllers import prediction_controller
from .core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Test Command
@app.get("/")
def hello():
    return {"message": "Hello! We are Rechef team!"}


app.include_router(user_controller.router, prefix="/api")
app.include_router(recipe_controller.router, prefix="/api")
app.include_router(prediction_controller.router, prefix="/api")
