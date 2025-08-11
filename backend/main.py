from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI(
    title="Your Application Name API",
    description="API for user authentication and other features."
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is crucial for allowing your frontend (running on a different port/origin) to communicate with your backend.
origins = [
    "http://localhost:3000", # Your React app's default development port
    "http://127.0.0.1:3000",
    # Add your production frontend URL here when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security: Password Hashing --- 
# Configure password hashing context using bcrypt for strong, one-way hashing.
# This ensures passwords are never stored in plain text.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Mock Database for Demonstration --- 
# In a real application, this would be a database (e.g., PostgreSQL, MongoDB).
# For demonstration, we'll use a dictionary to simulate user storage.
# Passwords are pre-hashed.

# Hash a sample password for the mock user
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Simulate user data with a pre-hashed password
# The plain text password for 'testuser' is 'ValidPassword123'
MOCK_USERS_DB = {
    "testuser": UserInDB(
        username="testuser", 
        hashed_password=get_password_hash("ValidPassword123")
    )
}

# --- Authentication Utility Function --- 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    """Retrieves a user from the mock database."""
    return MOCK_USERS_DB.get(username)

# --- API Endpoints --- 

@app.post("/api/login", summary="Authenticate user credentials")
async def login(request: LoginRequest):
    """
    Handles user login attempts.
    
    - Verifies username and password.
    - Implements server-side validation for missing fields.
    - Returns success or a generic error message for security (prevents enumeration).
    """
    # Server-side validation for missing fields (though frontend also validates)
    if not request.username or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required."
        )

    user = get_user(request.username)
    
    # Check if user exists and password is correct
    if not user or not verify_password(request.password, user.hashed_password):
        # Use a generic error message to prevent username enumeration attacks
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password. Please try again."
        )
    
    # In a real application, you would generate and return an access token (e.g., JWT) here.
    # For this exercise, we just return a success message.
    return {"message": "Login successful!", "redirect_to": "/dashboard"}

# --- Root Endpoint (Optional) --- 
@app.get("/", summary="Root endpoint for API health check")
async def read_root():
    return {"message": "Your Application API is running"}

# To run this backend:
# 1. Save as `main.py` in a `backend` folder.
# 2. Install dependencies: `pip install "fastapi[all]" uvicorn passlib[bcrypt]`
# 3. Run: `uvicorn main:app --reload --port 8000`
#    The API will be available at http://localhost:8000
