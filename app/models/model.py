from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(256))
    recipes = relationship("Recipe", back_populates="owner")

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    image = Column(Text)  # Increase the length to accommodate long URLs
    preparation_time = Column(Float)
    calories = Column(Float)
    ingredients = Column(JSON)  # Use JSON type for MySQL
    url = Column(String(1024))  # Increase the length to accommodate long URLs
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="recipes")