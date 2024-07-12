# middleware.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import decode_access_token
from ..services.user_service import get_user_by_username
from ..schemas.user_schema import User


# Mendefinisikan skema OAuth2 untuk mendapatkan token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mendefinisikan fungsi untuk mendapatkan pengguna saat ini berdasarkan token JWT
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:

    # Dekode token untuk mendapatkan username pengguna
    username = decode_access_token(token)

    # Jika tidak bisa memvalidasi token, lempar HTTPException
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ambil data pengguna dari database berdasarkan username
    user = get_user_by_username(db, username=username)

    # Jika pengguna tidak ditemukan, lempar HTTPException
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Kembalikan objek pengguna
    return user
