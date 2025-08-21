from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import User, UserInDB, TokenData
from services import get_user_by_username

# --- Security Configuration ---

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Secret Key (!!! In a real app, use environment variable and a strong, unique key !!!)
SECRET_KEY = "your-super-secret-key-replace-me-in-production"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Password Hashing Functions ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.
    Protects against timing attacks by bcrypt.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password.
    """
    return pwd_context.hash(password)

# --- JWT Functions ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decodes a JWT access token and returns its payload.
    Handles expired tokens and invalid signatures.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        scope: str = payload.get("scope")
        if username is None or scope is None:
            return None
        return TokenData(username=username, scope=scope)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current user from the provided JWT token.
    """
    token_data = decode_access_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_in_db = get_user_by_username(token_data.username)
    if user_in_db is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    # Check if account is locked
    if user_in_db.is_locked and user_in_db.locked_until and user_in_db.locked_until > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account locked until {user_in_db.locked_until.strftime('%Y-%m-%d %H:%M:%S')}.",
        )
    
    return User(**user_in_db.dict())

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """
    Authenticates a user by username and password.
    Handles initial lookup and password verification.
    """
    user = get_user_by_username(username)
    if not user: # For security, avoid revealing user existence
        return None
    if not verify_password(password, user.password_hash): 
        return None
    return user
