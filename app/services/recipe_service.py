from ..module.recipes import fetch_recipes as fetch_recipes_func
from typing import Optional

def fetch_recipes(query: str, continuation: Optional[str] = None):
    return fetch_recipes_func(query, continuation)
