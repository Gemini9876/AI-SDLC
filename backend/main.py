from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import hashlib
import os

# --- In-memory store for demonstration purposes ---
# In a real application, this would be a database

# User storage: username -> { password_hash, salt, is_locked }
USERS_DB = {
    "testuser": {
        "password_hash": "$2b$12$fS1n1c1e5p6g7h8i9j0kA.U2aB3c4D5e6F7g8H9i0JkL", # Example hash for 'password123'
        "salt": "some_random_salt",
        "is_locked": False,
        "lockout_until": None # timestamp for when lockout expires
    }
}

# Brute-force protection: username -> { failed_attempts, last_attempt_time }
FAILED_ATTEMPTS = {}
MAX_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

app = FastAPI()

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allow your React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

# Function to simulate password hashing and salting (for demonstration)
def hash_password(password: str, salt: str) -> str:
    # In a real application, use bcrypt or Argon2 for strong hashing
    # This is a simple SHA256 for illustration
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

# Function to simulate email notification
def send_account_lockout_email(username: str):
    print(f"[Email Notification] Account '{username}' has been locked due to multiple failed login attempts.")

@app.post("/api/login")
async def login_user(request: LoginRequest):
    username = request.username
    password = request.password
    
    # Simulate API response delay for performance testing
    await asyncio.sleep(0.5) # Simulate 500ms API processing time

    user_data = USERS_DB.get(username)

    # Brute-force protection logic
    current_time = time.time()
    if user_data:
        if user_data["is_locked"] and user_data["lockout_until"] and current_time < user_data["lockout_until"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account '{username}' is temporarily locked. Try again after "
                       f"{int((user_data['lockout_until'] - current_time) / 60) + 1} minutes."
            )
        elif user_data["is_locked"] and user_data["lockout_until"] and current_time >= user_data["lockout_until"]:
            # Lockout period expired, reset status
            user_data["is_locked"] = False
            user_data["lockout_until"] = None
            FAILED_ATTEMPTS.pop(username, None)
            print(f"Account '{username}' lockout expired and reset.")

    if not user_data:
        # Introduce a small delay for non-existent users to prevent enumeration attacks
        await asyncio.sleep(0.1)
        # Increment failed attempts for non-existent users as well, or a generic 'unknown user' bucket
        FAILED_ATTEMPTS.setdefault("unknown_user", {"failed_attempts": 0, "last_attempt_time": 0})
        FAILED_ATTEMPTS["unknown_user"]["failed_attempts"] += 1
        FAILED_ATTEMPTS["unknown_user"]["last_attempt_time"] = current_time
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password. Please try again.")

    # Password comparison (simulated hashing)
    provided_password_hash = hash_password(password, user_data["salt"])

    if provided_password_hash == user_data["password_hash"]:
        # Successful login: Reset failed attempts
        FAILED_ATTEMPTS.pop(username, None)
        print(f"User '{username}' logged in successfully.")
        return {"message": "Login successful", "token": "mock_jwt_token"}
    else:
        # Failed login: Increment attempts
        FAILED_ATTEMPTS.setdefault(username, {"failed_attempts": 0, "last_attempt_time": 0})
        FAILED_ATTEMPTS[username]["failed_attempts"] += 1
        FAILED_ATTEMPTS[username]["last_attempt_time"] = current_time

        if FAILED_ATTEMPTS[username]["failed_attempts"] >= MAX_ATTEMPTS:
            lockout_until = current_time + LOCKOUT_DURATION_MINUTES * 60
            user_data["is_locked"] = True
            user_data["lockout_until"] = lockout_until
            send_account_lockout_email(username)
            print(f"Account '{username}' locked due to too many failed attempts.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Too many failed login attempts. Your account has been locked for {LOCKOUT_DURATION_MINUTES} minutes."
            )
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password. Please try again.")

@app.get("/api/status")
async def get_status():
    return {"status": "Backend operational", "version": "1.0.0"}

# To run this backend:
# 1. pip install fastapi uvicorn pydantic
# 2. cd backend
# 3. uvicorn main:app --reload --port 8000

# Note on HTTPS/TLS:
# In a production environment, HTTPS (TLS 1.2 or higher) would be configured at the web server (e.g., Nginx, Apache) or load balancer (e.g., AWS ELB, Cloudflare) 
# that sits in front of your FastAPI application. FastAPI itself does not handle HTTPS directly, but it relies on the ASGI server (like Uvicorn) 
# and the surrounding infrastructure to provide a secure connection.