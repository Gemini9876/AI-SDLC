import pytest
from app import app, db, User, Post, Comment, Like, Follow, PrivacySetting
import json
from datetime import datetime

# A test client fixture for making requests
@pytest.fixture
def client():
    # Use an in-memory SQLite database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key' # Use a consistent secret key for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables before the test runs
        yield client
        with app.app_context():
            db.drop_all()  # Drop all tables after the test runs

# A fixture to create a test user and return a valid access token
@pytest.fixture
def auth_tokens(client):
    with app.app_context():
        # Create a user directly in the database
        user = User(email='test@example.com', full_name='Test User')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    # Generate tokens by calling the login endpoint
    response = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password123'})
    tokens = json.loads(response.data)
    
    return tokens['access_token'], tokens['refresh_token']

def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post('/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'strongpassword'
    })
    assert response.status_code == 201
    assert 'User registered successfully!' in response.get_json()['message']

def test_register_user_with_existing_email(client):
    """Test registration with an email that already exists."""
    client.post('/auth/register', json={'email': 'exist@example.com', 'password': 'testpassword'})
    response = client.post('/auth/register', json={'email': 'exist@example.com', 'password': 'testpassword'})
    assert response.status_code == 409
    assert 'User with this email already exists.' in response.get_json()['message']

def test_login_success(client):
    """Test successful user login."""
    client.post('/auth/register', json={'email': 'login@example.com', 'password': 'password123'})
    response = client.post('/auth/login', json={'email': 'login@example.com', 'password': 'password123'})
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_credentials(client):
    """Test login with incorrect password."""
    client.post('/auth/register', json={'email': 'invalid@example.com', 'password': 'password123'})
    response = client.post('/auth/login', json={'email': 'invalid@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert 'Invalid credentials!' in response.get_json()['message']

def test_get_user_profile_success(client, auth_tokens):
    """Test fetching the current user's profile with a valid token."""
    access_token, _ = auth_tokens
    response = client.get('/profile', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.get_json()['email'] == 'test@example.com'

def test_update_user_profile_success(client, auth_tokens):
    """Test updating the user's full name and bio."""
    access_token, _ = auth_tokens
    update_data = {
        'full_name': 'New Full Name',
        'bio': 'A new bio for testing purposes.'
    }
    response = client.put('/profile', headers={'Authorization': f'Bearer {access_token}'}, json=update_data)
    assert response.status_code == 200
    assert 'Profile updated successfully!' in response.get_json()['message']
    assert response.get_json()['profile']['full_name'] == 'New Full Name'

def test_create_post_success(client, auth_tokens):
    """Test creating a new post."""
    access_token, _ = auth_tokens
    post_data = {
        'title': 'My First Post',
        'content': 'This is the content of my first post.'
    }
    response = client.post('/posts', headers={'Authorization': f'Bearer {access_token}'}, json=post_data)
    assert response.status_code == 201
    assert 'Post created successfully!' in response.get_json()['message']
    assert response.get_json()['post']['title'] == 'My First Post'

def test_get_all_posts(client, auth_tokens):
    """Test fetching all posts."""
    access_token, _ = auth_tokens
    # Create a post first
    client.post('/posts', headers={'Authorization': f'Bearer {access_token}'}, json={
        'title': 'Test Post',
        'content': 'This is a test post.'
    })
    
    response = client.get('/posts', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]['title'] == 'Test Post'

def test_delete_post_success(client, auth_tokens):
    """Test deleting a post created by the user."""
    access_token, _ = auth_tokens
    # Create a post
    post_data = {
        'title': 'Post to be deleted',
        'content': 'Content of the post to be deleted.'
    }
    create_response = client.post('/posts', headers={'Authorization': f'Bearer {access_token}'}, json=post_data)
    post_id = create_response.get_json()['post']['id']
    
    # Delete the post
    delete_response = client.delete(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert delete_response.status_code == 200
    assert 'Post deleted successfully!' in delete_response.get_json()['message']

    # Verify the post is gone
    get_response = client.get(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert get_response.status_code == 404

def test_like_post_success(client, auth_tokens):
    """Test liking a post."""
    access_token, _ = auth_tokens
    
    # First, create another user and a post by that user
    with app.app_context():
        user2 = User(email='test2@example.com')
        user2.set_password('password123')
        db.session.add(user2)
        db.session.commit()
        
        post = Post(user_id=user2.id, title='A post to like', content='Content')
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        
    response = client.post(f'/posts/{post_id}/like', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert 'Post liked successfully!' in response.get_json()['message']

    # Verify like count
    post_response = client.get(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert post_response.get_json()['likes_count'] == 1

def test_add_comment_success(client, auth_tokens):
    """Test adding a comment to a post."""
    access_token, _ = auth_tokens
    
    # Create a post
    post_data = {
        'title': 'Post with comments',
        'content': 'Content for a test comment.'
    }
    create_response = client.post('/posts', headers={'Authorization': f'Bearer {access_token}'}, json=post_data)
    post_id = create_response.get_json()['post']['id']

    # Add a comment
    comment_data = {'content': 'This is a test comment.'}
    response = client.post(f'/posts/{post_id}/comments', headers={'Authorization': f'Bearer {access_token}'}, json=comment_data)
    assert response.status_code == 201
    assert 'Comment added successfully!' in response.get_json()['message']

    # Verify comment count
    post_response = client.get(f'/posts/{post_id}', headers={'Authorization': f'Bearer {access_token}'})
    assert post_response.get_json()['comments_count'] == 1

def test_follow_user_success(client, auth_tokens):
    """Test following another user."""
    access_token, _ = auth_tokens
    
    # Create a user to follow
    with app.app_context():
        user_to_follow = User(email='followme@example.com', full_name='Follow Me')
        user_to_follow.set_password('password123')
        db.session.add(user_to_follow)
        db.session.commit()
        user_to_follow_id = user_to_follow.id

    response = client.post(f'/users/{user_to_follow_id}/follow', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert 'You are now following followme@example.com' in response.get_json()['message']

def test_update_privacy_preferences(client, auth_tokens):
    """Test updating privacy settings."""
    access_token, _ = auth_tokens
    update_data = {
        'show_email': True,
        'receive_like_notifications': False
    }
    response = client.put('/profile/privacy', headers={'Authorization': f'Bearer {access_token}'}, json=update_data)
    assert response.status_code == 200
    assert 'Privacy preferences updated successfully!' in response.get_json()['message']
