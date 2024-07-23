from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from .config import settings

# Membuat konteks enkripsi dengan menggunakan bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Fungsi untuk memverifikasi password yang diinputkan dengan password yang sudah di-hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Fungsi untuk meng-hash password yang diinputkan
def get_password_hash(password):
    return pwd_context.hash(password)


# Fungsi untuk membuat access token dengan data dan waktu kadaluarsa yang opsional
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()  # Menyalin data yang akan dienkode
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Menentukan waktu kadaluarsa jika disediakan
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default waktu kadaluarsa adalah 15 menit
    to_encode.update({"exp": expire})  # Menambahkan waktu kadaluarsa ke data yang akan dienkode
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)  # Meng-encode data menjadi JWT
    return encoded_jwt


# Fungsi untuk mendekode access token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # Mendekode token
        return payload.get("sub")  # Mengambil nilai "sub" dari payload
    except JWTError:
        return None  # Mengembalikan None jika terjadi kesalahan JWT
