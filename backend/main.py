from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Optional
import jwt
from auth import authenticate_user, create_access_token, get_current_user_from_token, verify_password, get_password_hash
from models import User, Article, UserInDB, Token
from services import (get_user_by_username, update_user_failed_attempts, 
                      reset_user_failed_attempts, lock_user_account, 
                      unlock_user_account, get_all_articles, get_article_by_id)

app = FastAPI(
    title="Subscription Content Access API",
    description="API for managing user subscriptions and content access."
)

# OAuth2PasswordBearer for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Routes ---

@app.post("/token", response_model=Token, summary="User Login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns an access token.
    Handles account lockout policy.
    """
    user_in_db = get_user_by_username(form_data.username)

    if not user_in_db:
        # Fails without revealing user existence
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user_in_db.is_locked and user_in_db.locked_until and user_in_db.locked_until > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account locked until {user_in_db.locked_until.strftime('%Y-%m-%d %H:%M:%S')}.",
        )

    # Validate password, also acts as SQL/XSS prevention by using hashed passwords and proper validation
    if not verify_password(form_data.password, user_in_db.password_hash):
        # Increment failed attempts
        update_user_failed_attempts(user_in_db.username)
        
        # Check for lockout
        if user_in_db.failed_login_attempts + 1 >= 5: # +1 because it's about to be incremented
            lock_user_account(user_in_db.username)
            # Simulate email notification
            print(f"[SIMULATED EMAIL] Account locked notification sent to {user_in_db.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account locked for 15 minutes due to multiple failed attempts.",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If successful, reset failed attempts
    reset_user_failed_attempts(user_in_db.username)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_in_db.username, "scope": user_in_db.subscription_level.value},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer", "user": user_in_db.dict(exclude={'password_hash', 'failed_login_attempts', 'is_locked', 'locked_until'})}

@app.get("/articles", response_model=List[Article], summary="Get Articles based on Subscription")
async def read_articles(current_user: User = Depends(get_current_user_from_token)):
    """
    Retrieves articles accessible to the current user's subscription level.
    Optimized for performance with in-memory data, scalable to DB queries.
    """
    all_articles = get_all_articles()
    
    if current_user.subscription_level == "Free":
        # Free users only see Free articles
        return [article for article in all_articles if article.article_type == "Free"]
    elif current_user.subscription_level in ["Basic", "Premium"]:
        # Paid users see all articles
        return all_articles
    return [] # Should not happen

@app.get("/articles/{article_id}", response_model=Article, summary="Get Specific Article Content")
async def read_article_content(article_id: str, current_user: User = Depends(get_current_user_from_token)):
    """
    Retrieves a specific article's content.
    Enforces content access based on subscription level.
    """
    article = get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Security: Prevent direct access to paid content for free users
    if article.article_type == "Paid" and current_user.subscription_level == "Free":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Please upgrade your subscription to view this content."
        )
    
    return article

@app.get("/users/me", response_model=User, summary="Get Current User Info")
async def read_users_me(current_user: User = Depends(get_current_user_from_token)):
    """
    Retrieves information about the currently logged-in user.
    """
    return current_user

@app.post("/admin/unlock-account", summary="Admin Unlock Account (for testing)")
async def admin_unlock_account(username: str):
    """
    Admin endpoint to manually unlock a user's account for testing purposes.
    (In a real app, this would be behind proper admin authentication).
    """
    user_unlocked = unlock_user_account(username)
    if not user_unlocked:
        raise HTTPException(status_code=404, detail="User not found or not locked")
    return {"message": f"Account for {username} has been unlocked.", "unlocked": True}

# --- Security Considerations --- 
# SQL Injection: FastAPI with Pydantic and ORMs (like SQLAlchemy if used) inherently protects against SQL injection
# as parameters are bound, not concatenated directly into queries. Our simple in-memory DB uses dictionary lookups.
# XSS: Backend should return JSON data, not HTML. Frontend frameworks (like React Native) handle escaping for display.
# User inputs for login are validated against stored hashes, not directly executed.
