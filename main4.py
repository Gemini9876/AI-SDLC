```python
from datetime import datetime, timedelta
import secrets
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import pyotp

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./sql_app.db"

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    two_factor_secret = Column(String, nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    profile_picture_url = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    privacy_settings = Column(JSON, default={})

Base.metadata.create_all(bind=engine)

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password): return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password): return pwd_context.hash(password)

# JWT Utilities
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise HTTPException(status_code=401, detail="Could not validate credentials")
        return email
    except JWTError: raise HTTPException(status_code=401, detail="Could not validate credentials")

# Pydantic Schemas
class UserBase(BaseModel):
    email: EmailStr
    class Config: from_attributes = True

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    enable_2fa: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfile(UserBase):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    two_factor_enabled: bool
    privacy_settings: dict = {}

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None

class ProfilePictureUploadResponse(BaseModel):
    message: str
    profile_picture_url: str

class EmailUpdate(BaseModel):
    new_email: EmailStr
    password: str

class PrivacySettingsUpdate(BaseModel):
    privacy_settings: dict

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=8)

class TwoFactorAuthSetupResponse(BaseModel):
    secret: str
    qr_code_url: str

class TwoFactorAuthVerify(BaseModel):
    code: str

# FastAPI Application
app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# Current User Dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_access_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user is None: raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active: raise HTTPException(status_code=400, detail="Inactive user")
    return user

# --- Routes ---

@app.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    if user_in.enable_2fa: new_user.two_factor_secret = pyotp.random_base32()
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/password/forgot", status_code=status.HTTP_200_OK)
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_access_token(data={"sub": user.email, "type": "password_reset"}, expires_delta=timedelta(minutes=10))
    return {"message": "Password reset link sent to your email (simulated)."}

@app.post("/password/reset", status_code=status.HTTP_200_OK)
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email, token_type = payload.get("sub"), payload.get("type")
        if email is None or token_type != "password_reset": raise HTTPException(status_code=401, detail="Invalid or expired token")
    except JWTError: raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.email == email).first()
    if user is None: raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(request.new_password); db.commit()
    return {"message": "Password has been reset successfully."}

@app.post("/2fa/setup", response_model=TwoFactorAuthSetupResponse)
def setup_two_factor_auth(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.two_factor_enabled and current_user.two_factor_secret:
        raise HTTPException(status_code=400, detail="2FA already enabled.")
    secret = pyotp.random_base32()
    qr_code_url = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name="YourAppName")
    current_user.two_factor_secret = secret; db.commit(); db.refresh(current_user)
    return TwoFactorAuthSetupResponse(secret=secret, qr_code_url=qr_code_url)

@app.post("/2fa/verify", status_code=status.HTTP_200_OK)
def verify_two_factor_auth(verification: TwoFactorAuthVerify, current_user: User = Depends(get_current_user)):
    if not current_user.two_factor_secret: raise HTTPException(status_code=400, detail="2FA not set up.")
    if not pyotp.TOTP(current_user.two_factor_secret).verify(verification.code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code.")
    return {"message": "2FA code verified successfully."}

@app.post("/2fa/enable", status_code=status.HTTP_200_OK)
def enable_two_factor_auth(verification: TwoFactorAuthVerify, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.two_factor_enabled: raise HTTPException(status_code=400, detail="2FA already enabled.")
    if not current_user.two_factor_secret: raise HTTPException(status_code=400, detail="2FA secret not set. Run /2fa/setup.")
    if not pyotp.TOTP(current_user.two_factor_secret).verify(verification.code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code. Cannot enable.")
    current_user.two_factor_enabled = True; db.commit(); db.refresh(current_user)
    return {"message": "Two-factor authentication enabled successfully."}

@app.get("/profile", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/profile", response_model=UserProfile)
def update_user_profile(profile_update: UserProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in profile_update.dict(exclude_unset=True).items(): setattr(current_user, key, value)
    db.commit(); db.refresh(current_user)
    return current_user

@app.post("/profile/picture", response_model=ProfilePictureUploadResponse)
async def upload_profile_picture(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"): raise HTTPException(status_code=400, detail="Only image files are allowed.")
    dummy_url = f"https://example.com/profiles/{current_user.id}/{file.filename}"
    current_user.profile_picture_url = dummy_url; db.commit(); db.refresh(current_user)
    return ProfilePictureUploadResponse(message="Profile picture uploaded successfully.", profile_picture_url=dummy_url)

@app.patch("/profile/email", status_code=status.HTTP_200_OK)
def change_email(email_update: EmailUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(email_update.password, current_user.hashed_password): raise HTTPException(status_code=401, detail="Incorrect password.")
    if db.query(User).filter(User.email == email_update.new_email, User.id != current_user.id).first():
        raise HTTPException(status_code=400, detail="New email address is already taken.")
    current_user.email = email_update.new_email; db.commit(); db.refresh(current_user)
    return {"message": "Email address updated successfully."}

@app.patch("/profile/privacy", response_model=UserProfile)
def set_privacy_preferences(privacy_settings_update: PrivacySettingsUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.privacy_settings = privacy_settings_update.privacy_settings; db.commit(); db.refresh(current_user)
    return current_user
```