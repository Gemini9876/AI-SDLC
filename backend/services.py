from models import UserInDB, Article
from datetime import datetime, timedelta
from auth import get_password_hash # Import for initial user setup

# --- In-memory "Database" for demonstration ---
# In a real application, this would be a proper database (SQL, NoSQL)
# Passwords stored as hashes
users_db = {
    "frieda@example.com": UserInDB(
        id="user-free-1", username="frieda@example.com", email="frieda@example.com", 
        password_hash=get_password_hash("securePassword123"), subscription_level="Free"
    ),
    "patty@example.com": UserInDB(
        id="user-paid-1", username="patty@example.com", email="patty@example.com", 
        password_hash=get_password_hash("securePassword456"), subscription_level="Basic"
    ),
    "secure.susan@example.com": UserInDB(
        id="user-secure-1", username="secure.susan@example.com", email="secure.susan@example.com", 
        password_hash=get_password_hash("correctSecurePassword"), subscription_level="Free"
    ),
}

articles_db = {
    "article-free-1": Article(
        id="article-free-1", title="Free Article 1 Title", content="This is free content for everyone.", 
        article_type="Free", image_url="/images/free-article-1.png", image_alt_text="A person reading a book happily",
        url="/articles/free-article-1"
    ),
    "article-paid-1": Article(
        id="article-paid-1", title="Paid Article 1 Title", content="This is premium content for paid subscribers.", 
        article_type="Paid", image_url="/images/paid-article-1.png", image_alt_text="A detailed graph showing market trends",
        url="/articles/paid-article-exclusive"
    ),
    "article-free-2": Article(
        id="article-free-2", title="Free Article 2 Title", content="Another free piece of content.", 
        article_type="Free", image_url="/images/free-article-2.png", image_alt_text="People collaborating on a project",
        url="/articles/free-article-2"
    ),
    "article-paid-2": Article(
        id="article-paid-2", title="Paid Article 2 Title", content="More exclusive content.", 
        article_type="Paid", image_url="/images/paid-article-2.png", image_alt_text="An abstract art piece in vibrant colors",
        url="/articles/paid-article-premium"
    ),
}

# --- User Service Functions ---

def get_user_by_username(username: str) -> Optional[UserInDB]:
    return users_db.get(username)

def update_user_failed_attempts(username: str):
    user = users_db.get(username)
    if user:
        user.failed_login_attempts += 1
        users_db[username] = user

def reset_user_failed_attempts(username: str):
    user = users_db.get(username)
    if user:
        user.failed_login_attempts = 0
        user.is_locked = False
        user.locked_until = None
        users_db[username] = user

def lock_user_account(username: str, duration_minutes: int = 15):
    user = users_db.get(username)
    if user:
        user.is_locked = True
        user.locked_until = datetime.now() + timedelta(minutes=duration_minutes)
        users_db[username] = user

def unlock_user_account(username: str) -> bool:
    user = users_db.get(username)
    if user and user.is_locked:
        user.is_locked = False
        user.locked_until = None
        user.failed_login_attempts = 0 # Also reset attempts on manual unlock
        users_db[username] = user
        return True
    return False

# --- Article Service Functions ---

def get_all_articles() -> List[Article]:
    return list(articles_db.values())

def get_article_by_id(article_id: str) -> Optional[Article]:
    return articles_db.get(article_id)
