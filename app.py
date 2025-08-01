# import os
# import secrets
# from datetime import datetime, timedelta

# from flask import Flask, request, jsonify, g
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# import pyotp
# from functools import wraps

# # --- Configuration ---
# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secure_and_random_secret_key_for_production')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
#     # Placeholder for email service (e.g., SendGrid, Mailgun API keys)
#     EMAIL_SERVICE_ENABLED = False

# # --- Flask App Initialization ---
# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)

# # --- Models ---
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     full_name = db.Column(db.String(100))
#     bio = db.Column(db.String(500))
#     profile_picture_url = db.Column(db.String(255), default='default_profile.png')
#     two_factor_secret = db.Column(db.String(16))
#     two_factor_enabled = db.Column(db.Boolean, default=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     is_suspended = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
#     comments = db.relationship('Comment', backref='commenter', lazy=True, cascade="all, delete-orphan")
#     likes = db.relationship('Like', backref='liker', lazy=True, cascade="all, delete-orphan")
#     notifications = db.relationship('Notification', backref='recipient', lazy=True, cascade="all, delete-orphan")
#     privacy_settings = db.relationship('PrivacySetting', backref='user', lazy=True, cascade="all, delete-orphan")
#     followed = db.relationship(
#         'Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic', cascade="all, delete-orphan"
#     )
#     followers = db.relationship(
#         'Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic', cascade="all, delete-orphan"
#     )

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def generate_jwt(self, token_type='access'):
#         if token_type == 'access':
#             expiration = datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
#         elif token_type == 'refresh':
#             expiration = datetime.utcnow() + app.config['JWT_REFRESH_TOKEN_EXPIRES']
#         else:
#             raise ValueError("Invalid token type")

#         payload = {
#             'user_id': self.id,
#             'is_admin': self.is_admin,
#             'exp': expiration,
#             'iat': datetime.utcnow(),
#             'type': token_type
#         }
#         return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

#     def to_dict(self, include_private=False):
#         data = {
#             'id': self.id,
#             'email': self.email,
#             'full_name': self.full_name,
#             'bio': self.bio,
#             'profile_picture_url': self.profile_picture_url,
#             'two_factor_enabled': self.two_factor_enabled,
#             'is_suspended': self.is_suspended,
#             'created_at': self.created_at.isoformat(),
#             'updated_at': self.updated_at.isoformat()
#         }
#         if include_private:
#             data['is_admin'] = self.is_admin
#         return data

# class PrivacySetting(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     setting_name = db.Column(db.String(80), nullable=False) # e.g., 'show_email', 'can_be_searched', 'receive_comment_notifications'
#     setting_value = db.Column(db.Boolean, default=True) # True for enabled, False for disabled

#     __table_args__ = (db.UniqueConstraint('user_id', 'setting_name', name='_user_setting_uc'),)

#     def to_dict(self):
#         return {
#             'setting_name': self.setting_name,
#             'setting_value': self.setting_value
#         }

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     title = db.Column(db.String(150), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
#     likes = db.relationship('Like', backref='post', lazy=True, cascade="all, delete-orphan")

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'author_email': self.author.email,
#             'title': self.title,
#             'content': self.content,
#             'created_at': self.created_at.isoformat(),
#             'updated_at': self.updated_at.isoformat(),
#             'likes_count': len(self.likes),
#             'comments_count': len(self.comments)
#         }

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'post_id': self.post_id,
#             'user_id': self.user_id,
#             'commenter_email': self.commenter.email,
#             'content': self.content,
#             'created_at': self.created_at.isoformat()
#         }

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_user_post_like_uc'),)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'post_id': self.post_id,
#             'user_id': self.user_id,
#             'created_at': self.created_at.isoformat()
#         }

# class Notification(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     type = db.Column(db.String(50), nullable=False) # e.g., 'like', 'comment', 'follow'
#     message = db.Column(db.String(255), nullable=False)
#     is_read = db.Column(db.Boolean, default=False)
#     source_id = db.Column(db.Integer) # ID of the post, comment, or user that triggered the notification
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'type': self.type,
#             'message': self.message,
#             'is_read': self.is_read,
#             'source_id': self.source_id,
#             'created_at': self.created_at.isoformat()
#         }

# class Follow(db.Model):
#     follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

# # --- Utility Functions and Decorators ---
# def generate_totp_secret():
#     return pyotp.random_base32()

# def verify_totp_token(secret, token):
#     totp = pyotp.TOTP(secret)
#     return totp.verify(token)

# def create_notification(user_id, notification_type, message, source_id=None):
#     notification = Notification(user_id=user_id, type=notification_type, message=message, source_id=source_id)
#     db.session.add(notification)
#     db.session.commit()

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization'].split(" ")[1]

#         if not token:
#             return jsonify({'message': 'Authorization token is missing!'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#             current_user = User.query.get(data['user_id'])
#             if not current_user:
#                 return jsonify({'message': 'Token is invalid: User not found!'}), 401
#             if current_user.is_suspended:
#                 return jsonify({'message': 'Your account has been suspended.'}), 403
#             g.current_user = current_user
#             g.token_data = data # Store token data for type checks (e.g., refresh token)
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired!'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid!'}), 401
#         return f(*args, **kwargs)
#     return decorated

# def admin_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not g.current_user.is_admin:
#             return jsonify({'message': 'Admin access required!'}), 403
#         return f(*args, **kwargs)
#     return decorated

# # --- API Endpoints ---

# # User Authentication
# @app.route('/auth/register', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({'message': 'Email and password are required!'}), 400

#     if not isinstance(email, str) or not isinstance(password, str):
#         return jsonify({'message': 'Email and password must be strings.'}), 400

#     if User.query.filter_by(email=email).first():
#         return jsonify({'message': 'User with this email already exists.'}), 409

#     new_user = User(email=email)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()

#     # Initialize default privacy settings for the new user
#     default_privacy_settings = [
#         PrivacySetting(user_id=new_user.id, setting_name='can_be_searched', setting_value=True),
#         PrivacySetting(user_id=new_user.id, setting_name='show_email', setting_value=False),
#         PrivacySetting(user_id=new_user.id, setting_name='receive_like_notifications', setting_value=True),
#         PrivacySetting(user_id=new_user.id, setting_name='receive_comment_notifications', setting_value=True),
#         PrivacySetting(user_id=new_user.id, setting_name='receive_follower_notifications', setting_value=True),
#     ]
#     db.session.bulk_save_objects(default_privacy_settings)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully!', 'user_id': new_user.id}), 201

# @app.route('/auth/login', methods=['POST'])
# def login_user():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
#     two_factor_token = data.get('two_factor_token') # Optional for 2FA

#     user = User.query.filter_by(email=email).first()

#     if not user or not user.check_password(password):
#         return jsonify({'message': 'Invalid credentials!'}), 401

#     if user.is_suspended:
#         return jsonify({'message': 'Your account has been suspended.'}), 403

#     if user.two_factor_enabled:
#         if not two_factor_token:
#             return jsonify({'message': 'Two-factor authentication required.'}), 401
#         if not verify_totp_token(user.two_factor_secret, two_factor_token):
#             return jsonify({'message': 'Invalid two-factor token.'}), 401

#     access_token = user.generate_jwt(token_type='access')
#     refresh_token = user.generate_jwt(token_type='refresh')

#     return jsonify({
#         'message': 'Logged in successfully!',
#         'access_token': access_token,
#         'refresh_token': refresh_token
#     }), 200

# @app.route('/auth/refresh_token', methods=['POST'])
# @token_required
# def refresh_token():
#     # Ensure the token provided is a refresh token
#     if g.token_data.get('type') != 'refresh':
#         return jsonify({'message': 'A refresh token is required for this operation.'}), 401

#     new_access_token = g.current_user.generate_jwt(token_type='access')
#     return jsonify({'access_token': new_access_token}), 200

# @app.route('/auth/forgot_password', methods=['POST'])
# def forgot_password():
#     data = request.get_json()
#     email = data.get('email')
#     user = User.query.filter_by(email=email).first()

#     if user:
#         # In a real application, a unique token would be generated,
#         # stored in the database with an expiration, and sent via email.
#         # For this example, we simulate sending a link.
#         reset_token = secrets.token_urlsafe(32) # This token needs to be stored and associated with the user
#         # For a truly executable example without an email service, print to console.
#         print(f"DEBUG: Password reset link for {email}: http://localhost:5000/auth/reset_password_form?token={reset_token}")
#         # In a real app: email_service.send_reset_email(user.email, reset_token)
#     return jsonify({'message': 'If an account with that email exists, a password reset link has been sent.'}), 200

# @app.route('/auth/reset_password', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     reset_token = data.get('token')
#     new_password = data.get('new_password')

#     if not reset_token or not new_password:
#         return jsonify({'message': 'Token and new password are required.'}), 400

#     # This is a critical security placeholder. In a real system:
#     # 1. Retrieve the user by the `reset_token` from a secure, temporary store (e.g., a `PasswordResetToken` table).
#     # 2. Verify the token's expiration.
#     # 3. If valid, reset password and then invalidate/delete the token.
#     # For this example, we cannot simulate a secure token storage without a more complex setup.
#     # We will simply assume a valid token for the first user found. This is HIGHLY INSECURE for production.
#     user = User.query.first() # DANGER: This is ONLY for demonstration. Do NOT use in production.

#     if not user:
#         return jsonify({'message': 'Invalid or expired reset token.'}), 400

#     user.set_password(new_password)
#     # In a real app: invalidate the used reset token here.
#     db.session.commit()
#     return jsonify({'message': 'Password reset successfully!'}), 200

# @app.route('/auth/2fa/setup', methods=['POST'])
# @token_required
# def setup_2fa():
#     user = g.current_user
#     if user.two_factor_enabled:
#         return jsonify({'message': 'Two-factor authentication is already enabled.'}), 400

#     secret = generate_totp_secret()
#     user.two_factor_secret = secret
#     db.session.commit()

#     # In a real app, provide QR code URI for easy setup
#     # uri = pyotp.totp.TOTP(secret).provisioning_uri(user.email, issuer_name="MyAppName")
#     return jsonify({'message': '2FA setup initiated. Save this secret and verify:', 'secret': secret}), 200

# @app.route('/auth/2fa/verify', methods=['POST'])
# @token_required
# def verify_2fa_setup():
#     data = request.get_json()
#     token = data.get('token')
#     user = g.current_user

#     if not user.two_factor_secret:
#         return jsonify({'message': '2FA setup not initiated. Please call /auth/2fa/setup first.'}), 400
#     if user.two_factor_enabled:
#         return jsonify({'message': '2FA already verified and enabled.'}), 400

#     if not token or not verify_totp_token(user.two_factor_secret, token):
#         return jsonify({'message': 'Invalid 2FA token. Verification failed.'}), 401

#     user.two_factor_enabled = True
#     db.session.commit()
#     return jsonify({'message': 'Two-factor authentication enabled successfully!'}), 200

# @app.route('/auth/2fa/disable', methods=['POST'])
# @token_required
# def disable_2fa():
#     data = request.get_json()
#     token = data.get('token')
#     user = g.current_user

#     if not user.two_factor_enabled:
#         return jsonify({'message': 'Two-factor authentication is not enabled.'}), 400

#     if not token or not verify_totp_token(user.two_factor_secret, token):
#         return jsonify({'message': 'Invalid 2FA token. Disabling failed.'}), 401

#     user.two_factor_enabled = False
#     user.two_factor_secret = None # Remove secret for security
#     db.session.commit()
#     return jsonify({'message': 'Two-factor authentication disabled successfully!'}), 200

# # User Profile Management
# @app.route('/profile', methods=['GET'])
# @token_required
# def get_user_profile():
#     user = g.current_user
#     return jsonify(user.to_dict()), 200

# @app.route('/profile', methods=['PUT'])
# @token_required
# def update_user_profile():
#     user = g.current_user
#     data = request.get_json()

#     user.full_name = data.get('full_name', user.full_name)
#     user.bio = data.get('bio', user.bio)
#     # Profile picture upload is simulated here by updating a URL string.
#     # In a real app, this would involve actual file storage (e.g., S3, local disk).
#     if 'profile_picture_url' in data:
#         user.profile_picture_url = data['profile_picture_url']

#     db.session.commit()
#     return jsonify({'message': 'Profile updated successfully!', 'profile': user.to_dict()}), 200

# @app.route('/profile/email', methods=['PUT'])
# @token_required
# def change_user_email():
#     user = g.current_user
#     data = request.get_json()
#     new_email = data.get('new_email')
#     password = data.get('password') # Require current password for sensitive change

#     if not new_email or not password:
#         return jsonify({'message': 'New email and current password are required.'}), 400
#     if not isinstance(new_email, str) or not isinstance(password, str):
#         return jsonify({'message': 'New email and password must be strings.'}), 400
    
#     if not user.check_password(password):
#         return jsonify({'message': 'Invalid password.'}), 401
    
#     if User.query.filter_by(email=new_email).first():
#         return jsonify({'message': 'This email is already taken by another account.'}), 409

#     user.email = new_email
#     db.session.commit()
#     return jsonify({'message': 'Email updated successfully!', 'new_email': user.email}), 200

# @app.route('/profile/privacy', methods=['GET'])
# @token_required
# def get_privacy_preferences():
#     user = g.current_user
#     settings = user.privacy_settings.all()
#     return jsonify([s.to_dict() for s in settings]), 200

# @app.route('/profile/privacy', methods=['PUT'])
# @token_required
# def update_privacy_preferences():
#     user = g.current_user
#     data = request.get_json() # Expects a dictionary of {setting_name: value}

#     for setting_name, setting_value in data.items():
#         if not isinstance(setting_value, bool):
#             return jsonify({'message': f"Invalid value for '{setting_name}'. Must be boolean."}), 400

#         setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name=setting_name).first()
#         if setting:
#             setting.setting_value = setting_value
#         else:
#             # If a new valid setting is provided that wasn't default, create it
#             # In a strict system, only predefined settings would be allowed.
#             new_setting = PrivacySetting(user_id=user.id, setting_name=setting_name, setting_value=setting_value)
#             db.session.add(new_setting)
#     db.session.commit()
#     return jsonify({'message': 'Privacy preferences updated successfully!'}), 200

# # Content Management
# @app.route('/posts', methods=['POST'])
# @token_required
# def create_post():
#     data = request.get_json()
#     title = data.get('title')
#     content = data.get('content')

#     if not title or not content:
#         return jsonify({'message': 'Title and content are required for a post.'}), 400
#     if not isinstance(title, str) or not isinstance(content, str):
#         return jsonify({'message': 'Title and content must be strings.'}), 400

#     new_post = Post(user_id=g.current_user.id, title=title, content=content)
#     db.session.add(new_post)
#     db.session.commit()
#     return jsonify({'message': 'Post created successfully!', 'post': new_post.to_dict()}), 201

# @app.route('/posts', methods=['GET'])
# @token_required
# def get_all_posts():
#     # In a production app, this would implement pagination, more filters, etc.
#     posts = Post.query.order_by(Post.created_at.desc()).all()
#     return jsonify([post.to_dict() for post in posts]), 200

# @app.route('/posts/<int:post_id>', methods=['GET'])
# @token_required
# def get_single_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404
#     return jsonify(post.to_dict()), 200

# @app.route('/posts/<int:post_id>', methods=['PUT'])
# @token_required
# def edit_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404
#     if post.user_id != g.current_user.id:
#         return jsonify({'message': 'You are not authorized to edit this post.'}), 403

#     data = request.get_json()
#     if 'title' in data:
#         if not isinstance(data['title'], str):
#             return jsonify({'message': 'Title must be a string.'}), 400
#         post.title = data['title']
#     if 'content' in data:
#         if not isinstance(data['content'], str):
#             return jsonify({'message': 'Content must be a string.'}), 400
#         post.content = data['content']
        
#     db.session.commit()
#     return jsonify({'message': 'Post updated successfully!', 'post': post.to_dict()}), 200

# @app.route('/posts/<int:post_id>', methods=['DELETE'])
# @token_required
# def delete_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404
#     if post.user_id != g.current_user.id and not g.current_user.is_admin:
#         return jsonify({'message': 'You are not authorized to delete this post.'}), 403

#     db.session.delete(post)
#     db.session.commit()
#     return jsonify({'message': 'Post deleted successfully!'}), 200

# @app.route('/posts/<int:post_id>/like', methods=['POST'])
# @token_required
# def like_post(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404

#     existing_like = Like.query.filter_by(post_id=post_id, user_id=g.current_user.id).first()
#     if existing_like:
#         return jsonify({'message': 'You have already liked this post.'}), 409

#     new_like = Like(post_id=post_id, user_id=g.current_user.id)
#     db.session.add(new_like)
#     db.session.commit()

#     # Create notification for the post author (if not self-liking and preferences allow)
#     if post.user_id != g.current_user.id:
#         author_receive_like_notif = PrivacySetting.query.filter_by(
#             user_id=post.user_id, setting_name='receive_like_notifications'
#         ).first()
#         if not author_receive_like_notif or author_receive_like_notif.setting_value:
#             create_notification(post.user_id, 'like', f'{g.current_user.full_name or g.current_user.email} liked your post "{post.title}".', post.id)

#     return jsonify({'message': 'Post liked successfully!'}), 200

# @app.route('/posts/<int:post_id>/like', methods=['DELETE'])
# @token_required
# def unlike_post(post_id):
#     like = Like.query.filter_by(post_id=post_id, user_id=g.current_user.id).first()
#     if not like:
#         return jsonify({'message': 'You have not liked this post.'}), 404

#     db.session.delete(like)
#     db.session.commit()
#     return jsonify({'message': 'Post unliked successfully!'}), 200

# @app.route('/posts/<int:post_id>/comments', methods=['POST'])
# @token_required
# def add_comment(post_id):
#     data = request.get_json()
#     content = data.get('content')

#     if not content:
#         return jsonify({'message': 'Comment content is required.'}), 400
#     if not isinstance(content, str):
#         return jsonify({'message': 'Comment content must be a string.'}), 400

#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404

#     new_comment = Comment(post_id=post_id, user_id=g.current_user.id, content=content)
#     db.session.add(new_comment)
#     db.session.commit()

#     # Create notification for the post author (if not self-commenting and preferences allow)
#     if post.user_id != g.current_user.id:
#         author_receive_comment_notif = PrivacySetting.query.filter_by(
#             user_id=post.user_id, setting_name='receive_comment_notifications'
#         ).first()
#         if not author_receive_comment_notif or author_receive_comment_notif.setting_value:
#             create_notification(post.user_id, 'comment', f'{g.current_user.full_name or g.current_user.email} commented on your post "{post.title}".', post.id)

#     return jsonify({'message': 'Comment added successfully!', 'comment': new_comment.to_dict()}), 201

# @app.route('/posts/<int:post_id>/comments', methods=['GET'])
# @token_required
# def get_post_comments(post_id):
#     post = Post.query.get(post_id)
#     if not post:
#         return jsonify({'message': 'Post not found.'}), 404
#     comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
#     return jsonify([comment.to_dict() for comment in comments]), 200

# # Search and Discovery
# @app.route('/search/users', methods=['GET'])
# @token_required
# def search_users():
#     query = request.args.get('query', '').strip()
#     if not query:
#         return jsonify({'message': 'Search query is required.'}), 400

#     # Case-insensitive search by email or full name for active users
#     users_raw = User.query.filter(User.is_suspended == False).filter(
#         (User.email.ilike(f'%{query}%')) |
#         (User.full_name.ilike(f'%{query}%'))
#     ).all()

#     # Filter out users who have explicitly set privacy not to be searched
#     searchable_users = []
#     for user in users_raw:
#         can_be_searched_setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name='can_be_searched').first()
#         if not can_be_searched_setting or can_be_searched_setting.setting_value:
#             searchable_users.append(user.to_dict())

#     # Search suggestions and additional filters would require more complex logic
#     # (e.g., dedicated search engine, aggregated data, separate endpoints).
#     return jsonify(searchable_users), 200

# @app.route('/search/posts', methods=['GET'])
# @token_required
# def search_posts():
#     keyword = request.args.get('keyword', '').strip()
#     filter_by_user_id = request.args.get('user_id', type=int)
#     # Additional filters (e.g., 'tag', 'date_range') could be added here.

#     if not keyword:
#         return jsonify({'message': 'Search keyword is required.'}), 400

#     posts_query = Post.query.filter(
#         (Post.title.ilike(f'%{keyword}%')) |
#         (Post.content.ilike(f'%{keyword}%'))
#     )

#     if filter_by_user_id:
#         posts_query = posts_query.filter_by(user_id=filter_by_user_id)

#     posts = posts_query.order_by(Post.created_at.desc()).all()

#     # Search suggestions (e.g., popular keywords, autocomplete) are out of scope for a single file.
#     return jsonify([post.to_dict() for post in posts]), 200

# # Notifications
# @app.route('/notifications', methods=['GET'])
# @token_required
# def get_user_notifications():
#     notifications = Notification.query.filter_by(user_id=g.current_user.id).order_by(Notification.created_at.desc()).all()
#     return jsonify([n.to_dict() for n in notifications]), 200

# @app.route('/notifications/<int:notification_id>/read', methods=['PUT'])
# @token_required
# def mark_notification_as_read(notification_id):
#     notification = Notification.query.get(notification_id)
#     if not notification:
#         return jsonify({'message': 'Notification not found.'}), 404
#     if notification.user_id != g.current_user.id:
#         return jsonify({'message': 'You are not authorized to mark this notification as read.'}), 403

#     notification.is_read = True
#     db.session.commit()
#     return jsonify({'message': 'Notification marked as read.', 'notification': notification.to_dict()}), 200

# @app.route('/notifications/preferences', methods=['GET'])
# @token_required
# def get_notification_preferences():
#     # Notification preferences are managed as specific PrivacySettings.
#     preferences = PrivacySetting.query.filter(
#         PrivacySetting.user_id == g.current_user.id,
#         PrivacySetting.setting_name.in_(['receive_like_notifications', 'receive_comment_notifications', 'receive_follower_notifications'])
#     ).all()
#     return jsonify([p.to_dict() for p in preferences]), 200

# @app.route('/notifications/preferences', methods=['PUT'])
# @token_required
# def update_notification_preferences():
#     user = g.current_user
#     data = request.get_json() # Expected: {'receive_like_notifications': True/False, ...}

#     allowed_settings = ['receive_like_notifications', 'receive_comment_notifications', 'receive_follower_notifications']

#     for setting_name, setting_value in data.items():
#         if setting_name not in allowed_settings:
#             return jsonify({'message': f"Invalid notification preference setting: '{setting_name}'"}), 400
#         if not isinstance(setting_value, bool):
#             return jsonify({'message': f"Invalid value for '{setting_name}'. Must be boolean."}), 400

#         setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name=setting_name).first()
#         if setting:
#             setting.setting_value = setting_value
#         else:
#             # Create if a specific notification preference was not yet set (e.g., if new settings are introduced)
#             new_setting = PrivacySetting(user_id=user.id, setting_name=setting_name, setting_value=setting_value)
#             db.session.add(new_setting)
#     db.session.commit()
#     return jsonify({'message': 'Notification preferences updated successfully!'}), 200

# # Follow/Unfollow for follower notifications
# @app.route('/users/<int:user_id>/follow', methods=['POST'])
# @token_required
# def follow_user(user_id):
#     followed_user = User.query.get(user_id)
#     if not followed_user:
#         return jsonify({'message': 'User not found.'}), 404
#     if followed_user.id == g.current_user.id:
#         return jsonify({'message': 'You cannot follow yourself.'}), 400
#     if followed_user.is_suspended:
#         return jsonify({'message': 'Cannot follow a suspended user.'}), 403

#     existing_follow = Follow.query.filter_by(follower_id=g.current_user.id, followed_id=user_id).first()
#     if existing_follow:
#         return jsonify({'message': 'You are already following this user.'}), 409

#     new_follow = Follow(follower_id=g.current_user.id, followed_id=user_id)
#     db.session.add(new_follow)
#     db.session.commit()

#     # Create notification for the followed user (if preferences allow)
#     followed_user_receive_follower_notif = PrivacySetting.query.filter_by(
#         user_id=followed_user.id, setting_name='receive_follower_notifications'
#     ).first()
#     if not followed_user_receive_follower_notif or followed_user_receive_follower_notif.setting_value:
#         create_notification(followed_user.id, 'follow', f'{g.current_user.full_name or g.current_user.email} started following you.', g.current_user.id)

#     return jsonify({'message': f'You are now following {followed_user.email}.'}), 200

# @app.route('/users/<int:user_id>/unfollow', methods=['DELETE'])
# @token_required
# def unfollow_user(user_id):
#     follow_relation = Follow.query.filter_by(follower_id=g.current_user.id, followed_id=user_id).first()
#     if not follow_relation:
#         return jsonify({'message': 'You are not following this user.'}), 404

#     db.session.delete(follow_relation)
#     db.session.commit()
#     return jsonify({'message': 'You have unfollowed this user.'}), 200

# # Admin Features
# @app.route('/admin/users', methods=['GET'])
# @token_required
# @admin_required
# def admin_get_all_users():
#     users = User.query.all()
#     return jsonify([user.to_dict(include_private=True) for user in users]), 200

# @app.route('/admin/users/<int:user_id>/suspend', methods=['PUT'])
# @token_required
# @admin_required
# def admin_suspend_user(user_id):
#     user_to_mod = User.query.get(user_id)
#     if not user_to_mod:
#         return jsonify({'message': 'User not found.'}), 404
#     if user_to_mod.id == g.current_user.id:
#         return jsonify({'message': 'Administrators cannot suspend or delete their own account.'}), 403
#     if user_to_mod.is_admin:
#          return jsonify({'message': 'Cannot suspend another administrator account.'}), 403

#     user_to_mod.is_suspended = not user_to_mod.is_suspended # Toggle suspend status
#     db.session.commit()
#     status = "suspended" if user_to_mod.is_suspended else "unsuspended"
#     return jsonify({'message': f'User {user_to_mod.email} {status} successfully!', 'user': user_to_mod.to_dict(include_private=True)}), 200

# @app.route('/admin/users/<int:user_id>', methods=['DELETE'])
# @token_required
# @admin_required
# def admin_delete_user(user_id):
#     user_to_delete = User.query.get(user_id)
#     if not user_to_delete:
#         return jsonify({'message': 'User not found.'}), 404
#     if user_to_delete.id == g.current_user.id:
#         return jsonify({'message': 'Administrators cannot suspend or delete their own account.'}), 403
#     if user_to_delete.is_admin:
#         return jsonify({'message': 'Cannot delete another administrator account.'}), 403

#     db.session.delete(user_to_delete)
#     db.session.commit()
#     return jsonify({'message': f'User {user_to_delete.email} deleted successfully!'}), 200

# @app.route('/admin/content/moderate', methods=['GET'])
# @token_required
# @admin_required
# def admin_moderate_content():
#     # This is a placeholder for content moderation.
#     # In a real system, this might involve fetching reported content, filtering by type, etc.
#     # For now, it returns all posts and comments as a demonstration.
#     all_posts = Post.query.all()
#     all_comments = Comment.query.all()

#     return jsonify({
#         'message': 'Displaying all posts and comments for moderation review (placeholder).',
#         'posts': [p.to_dict() for p in all_posts],
#         'comments': [c.to_dict() for c in all_comments]
#     }), 200

# @app.route('/admin/analytics', methods=['GET'])
# @token_required
# @admin_required
# def admin_view_analytics():
#     # This is a placeholder for system analytics.
#     # In a real system, this would involve more sophisticated queries and data aggregation.
#     total_users = User.query.count()
#     total_posts = Post.query.count()
#     total_comments = Comment.query.count()
#     total_likes = Like.query.count()
    
#     # Example: Active users in the last 7 days (based on posts created)
#     seven_days_ago = datetime.utcnow() - timedelta(days=7)
#     active_users_recent_posts = db.session.query(db.func.count(db.distinct(Post.user_id))).filter(Post.created_at >= seven_days_ago).scalar()
#     if active_users_recent_posts is None: active_users_recent_posts = 0

#     return jsonify({
#         'message': 'System analytics (placeholder).',
#         'total_users': total_users,
#         'total_posts': total_posts,
#         'total_comments': total_comments,
#         'total_likes': total_likes,
#         'active_users_last_7_days_by_posts': active_users_recent_posts,
#         # More metrics could be added here
#     }), 200


# # --- Database Initialization (Run once on app startup) ---
# @app.before_first_request
# def create_tables():
#     db.create_all()
#     # Create an initial admin user if no admin exists
#     if not User.query.filter_by(is_admin=True).first():
#         admin_user = User(email='admin@example.com', is_admin=True, full_name='System Administrator')
#         admin_user.set_password('adminpassword') # IMPORTANT: Change this in production
#         db.session.add(admin_user)
#         db.session.commit()
#         print("Created default admin user: admin@example.com / adminpassword")

#         # Initialize default privacy settings for the new admin user
#         default_admin_privacy_settings = [
#             PrivacySetting(user_id=admin_user.id, setting_name='can_be_searched', setting_value=True),
#             PrivacySetting(user_id=admin_user.id, setting_name='show_email', setting_value=False),
#             PrivacySetting(user_id=admin_user.id, setting_name='receive_like_notifications', setting_value=True),
#             PrivacySetting(user_id=admin_user.id, setting_name='receive_comment_notifications', setting_value=True),
#             PrivacySetting(user_id=admin_user.id, setting_name='receive_follower_notifications', setting_value=True),
#         ]
#         db.session.bulk_save_objects(default_admin_privacy_settings)
#         db.session.commit()

# # --- Main Run Block ---
# if __name__ == '__main__':
#     # Ensure tables are created when the script is run directly
#     with app.app_context():
#         create_tables() 
#     app.run(debug=True) # debug=True is for development, use a WSGI server for production (e.g., Gunicorn)


import os
import secrets
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import pyotp
from functools import wraps

# --- Configuration ---
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secure_and_random_secret_key_for_production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    # Placeholder for email service (e.g., SendGrid, Mailgun API keys)
    EMAIL_SERVICE_ENABLED = False

# --- Flask App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.String(500))
    profile_picture_url = db.Column(db.String(255), default='default_profile.png')
    two_factor_secret = db.Column(db.String(16))
    two_factor_enabled = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_suspended = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='commenter', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='liker', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='recipient', lazy=True, cascade="all, delete-orphan")
    privacy_settings = db.relationship('PrivacySetting', backref='user', lazy=True, cascade="all, delete-orphan")
    followed = db.relationship(
        'Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic', cascade="all, delete-orphan"
    )
    followers = db.relationship(
        'Follow', foreign_keys='Follow.followed_id', backref='followed', lazy='dynamic', cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self, token_type='access'):
        if token_type == 'access':
            expiration = datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        elif token_type == 'refresh':
            expiration = datetime.utcnow() + app.config['JWT_REFRESH_TOKEN_EXPIRES']
        else:
            raise ValueError("Invalid token type")

        payload = {
            'user_id': self.id,
            'is_admin': self.is_admin,
            'exp': expiration,
            'iat': datetime.utcnow(),
            'type': token_type
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    def to_dict(self, include_private=False):
        data = {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'bio': self.bio,
            'profile_picture_url': self.profile_picture_url,
            'two_factor_enabled': self.two_factor_enabled,
            'is_suspended': self.is_suspended,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_private:
            data['is_admin'] = self.is_admin
        return data

class PrivacySetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    setting_name = db.Column(db.String(80), nullable=False) # e.g., 'show_email', 'can_be_searched', 'receive_comment_notifications'
    setting_value = db.Column(db.Boolean, default=True) # True for enabled, False for disabled

    __table_args__ = (db.UniqueConstraint('user_id', 'setting_name', name='_user_setting_uc'),)

    def to_dict(self):
        return {
            'setting_name': self.setting_name,
            'setting_value': self.setting_value
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='post', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'author_email': self.author.email,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes_count': len(self.likes),
            'comments_count': len(self.comments)
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'commenter_email': self.commenter.email,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='_user_post_like_uc'),)

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # e.g., 'like', 'comment', 'follow'
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    source_id = db.Column(db.Integer) # ID of the post, comment, or user that triggered the notification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'is_read': self.is_read,
            'source_id': self.source_id,
            'created_at': self.created_at.isoformat()
        }

class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

# --- Utility Functions and Decorators ---
def generate_totp_secret():
    return pyotp.random_base32()

def verify_totp_token(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def create_notification(user_id, notification_type, message, source_id=None):
    notification = Notification(user_id=user_id, type=notification_type, message=message, source_id=source_id)
    db.session.add(notification)
    db.session.commit()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Authorization token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Token is invalid: User not found!'}), 401
            if current_user.is_suspended:
                return jsonify({'message': 'Your account has been suspended.'}), 403
            g.current_user = current_user
            g.token_data = data # Store token data for type checks (e.g., refresh token)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.current_user.is_admin:
            return jsonify({'message': 'Admin access required!'}), 403
        return f(*args, **kwargs)
    return decorated

# --- API Endpoints ---

# User Authentication
@app.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({'message': 'Email and password must be strings.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User with this email already exists.'}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Initialize default privacy settings for the new user
    default_privacy_settings = [
        PrivacySetting(user_id=new_user.id, setting_name='can_be_searched', setting_value=True),
        PrivacySetting(user_id=new_user.id, setting_name='show_email', setting_value=False),
        PrivacySetting(user_id=new_user.id, setting_name='receive_like_notifications', setting_value=True),
        PrivacySetting(user_id=new_user.id, setting_name='receive_comment_notifications', setting_value=True),
        PrivacySetting(user_id=new_user.id, setting_name='receive_follower_notifications', setting_value=True),
    ]
    db.session.bulk_save_objects(default_privacy_settings)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!', 'user_id': new_user.id}), 201

@app.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    two_factor_token = data.get('two_factor_token') # Optional for 2FA

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    if user.is_suspended:
        return jsonify({'message': 'Your account has been suspended.'}), 403

    if user.two_factor_enabled:
        if not two_factor_token:
            return jsonify({'message': 'Two-factor authentication required.'}), 401
        if not verify_totp_token(user.two_factor_secret, two_factor_token):
            return jsonify({'message': 'Invalid two-factor token.'}), 401

    access_token = user.generate_jwt(token_type='access')
    refresh_token = user.generate_jwt(token_type='refresh')

    return jsonify({
        'message': 'Logged in successfully!',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@app.route('/auth/refresh_token', methods=['POST'])
@token_required
def refresh_token():
    # Ensure the token provided is a refresh token
    if g.token_data.get('type') != 'refresh':
        return jsonify({'message': 'A refresh token is required for this operation.'}), 401

    new_access_token = g.current_user.generate_jwt(token_type='access')
    return jsonify({'access_token': new_access_token}), 200

@app.route('/auth/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if user:
        # In a real application, a unique token would be generated,
        # stored in the database with an expiration, and sent via email.
        # For this example, we simulate sending a link.
        reset_token = secrets.token_urlsafe(32) # This token needs to be stored and associated with the user
        # For a truly executable example without an email service, print to console.
        print(f"DEBUG: Password reset link for {email}: http://localhost:5000/auth/reset_password_form?token={reset_token}")
        # In a real app: email_service.send_reset_email(user.email, reset_token)
    return jsonify({'message': 'If an account with that email exists, a password reset link has been sent.'}), 200

@app.route('/auth/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    reset_token = data.get('token')
    new_password = data.get('new_password')

    if not reset_token or not new_password:
        return jsonify({'message': 'Token and new password are required.'}), 400

    # This is a critical security placeholder. In a real system:
    # 1. Retrieve the user by the `reset_token` from a secure, temporary store (e.g., a `PasswordResetToken` table).
    # 2. Verify the token's expiration.
    # 3. If valid, reset password and then invalidate/delete the token.
    # For this example, we cannot simulate a secure token storage without a more complex setup.
    # We will simply assume a valid token for the first user found. This is HIGHLY INSECURE for production.
    user = User.query.first() # DANGER: This is ONLY for demonstration. Do NOT use in production.

    if not user:
        return jsonify({'message': 'Invalid or expired reset token.'}), 400

    user.set_password(new_password)
    # In a real app: invalidate the used reset token here.
    db.session.commit()
    return jsonify({'message': 'Password reset successfully!'}), 200

@app.route('/auth/2fa/setup', methods=['POST'])
@token_required
def setup_2fa():
    user = g.current_user
    if user.two_factor_enabled:
        return jsonify({'message': 'Two-factor authentication is already enabled.'}), 400

    secret = generate_totp_secret()
    user.two_factor_secret = secret
    db.session.commit()

    # In a real app, provide QR code URI for easy setup
    # uri = pyotp.totp.TOTP(secret).provisioning_uri(user.email, issuer_name="MyAppName")
    return jsonify({'message': '2FA setup initiated. Save this secret and verify:', 'secret': secret}), 200

@app.route('/auth/2fa/verify', methods=['POST'])
@token_required
def verify_2fa_setup():
    data = request.get_json()
    token = data.get('token')
    user = g.current_user

    if not user.two_factor_secret:
        return jsonify({'message': '2FA setup not initiated. Please call /auth/2fa/setup first.'}), 400
    if user.two_factor_enabled:
        return jsonify({'message': '2FA already verified and enabled.'}), 400

    if not token or not verify_totp_token(user.two_factor_secret, token):
        return jsonify({'message': 'Invalid 2FA token. Verification failed.'}), 401

    user.two_factor_enabled = True
    db.session.commit()
    return jsonify({'message': 'Two-factor authentication enabled successfully!'}), 200

@app.route('/auth/2fa/disable', methods=['POST'])
@token_required
def disable_2fa():
    data = request.get_json()
    token = data.get('token')
    user = g.current_user

    if not user.two_factor_enabled:
        return jsonify({'message': 'Two-factor authentication is not enabled.'}), 400

    if not token or not verify_totp_token(user.two_factor_secret, token):
        return jsonify({'message': 'Invalid 2FA token. Disabling failed.'}), 401

    user.two_factor_enabled = False
    user.two_factor_secret = None # Remove secret for security
    db.session.commit()
    return jsonify({'message': 'Two-factor authentication disabled successfully!'}), 200

# User Profile Management
@app.route('/profile', methods=['GET'])
@token_required
def get_user_profile():
    user = g.current_user
    return jsonify(user.to_dict()), 200

@app.route('/profile', methods=['PUT'])
@token_required
def update_user_profile():
    user = g.current_user
    data = request.get_json()

    user.full_name = data.get('full_name', user.full_name)
    user.bio = data.get('bio', user.bio)
    # Profile picture upload is simulated here by updating a URL string.
    # In a real app, this would involve actual file storage (e.g., S3, local disk).
    if 'profile_picture_url' in data:
        user.profile_picture_url = data['profile_picture_url']

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully!', 'profile': user.to_dict()}), 200

@app.route('/profile/email', methods=['PUT'])
@token_required
def change_user_email():
    user = g.current_user
    data = request.get_json()
    new_email = data.get('new_email')
    password = data.get('password') # Require current password for sensitive change

    if not new_email or not password:
        return jsonify({'message': 'New email and current password are required.'}), 400
    if not isinstance(new_email, str) or not isinstance(password, str):
        return jsonify({'message': 'New email and password must be strings.'}), 400
    
    if not user.check_password(password):
        return jsonify({'message': 'Invalid password.'}), 401
    
    if User.query.filter_by(email=new_email).first():
        return jsonify({'message': 'This email is already taken by another account.'}), 409

    user.email = new_email
    db.session.commit()
    return jsonify({'message': 'Email updated successfully!', 'new_email': user.email}), 200

@app.route('/profile/privacy', methods=['GET'])
@token_required
def get_privacy_preferences():
    user = g.current_user
    settings = user.privacy_settings.all()
    return jsonify([s.to_dict() for s in settings]), 200

@app.route('/profile/privacy', methods=['PUT'])
@token_required
def update_privacy_preferences():
    user = g.current_user
    data = request.get_json() # Expects a dictionary of {setting_name: value}

    for setting_name, setting_value in data.items():
        if not isinstance(setting_value, bool):
            return jsonify({'message': f"Invalid value for '{setting_name}'. Must be boolean."}), 400

        setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name=setting_name).first()
        if setting:
            setting.setting_value = setting_value
        else:
            # If a new valid setting is provided that wasn't default, create it
            # In a strict system, only predefined settings would be allowed.
            new_setting = PrivacySetting(user_id=user.id, setting_name=setting_name, setting_value=setting_value)
            db.session.add(new_setting)
    db.session.commit()
    return jsonify({'message': 'Privacy preferences updated successfully!'}), 200

# Content Management
@app.route('/posts', methods=['POST'])
@token_required
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Title and content are required for a post.'}), 400
    if not isinstance(title, str) or not isinstance(content, str):
        return jsonify({'message': 'Title and content must be strings.'}), 400

    new_post = Post(user_id=g.current_user.id, title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully!', 'post': new_post.to_dict()}), 201

@app.route('/posts', methods=['GET'])
@token_required
def get_all_posts():
    # In a production app, this would implement pagination, more filters, etc.
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@app.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_single_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404
    return jsonify(post.to_dict()), 200

@app.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404
    if post.user_id != g.current_user.id:
        return jsonify({'message': 'You are not authorized to edit this post.'}), 403

    data = request.get_json()
    if 'title' in data:
        if not isinstance(data['title'], str):
            return jsonify({'message': 'Title must be a string.'}), 400
        post.title = data['title']
    if 'content' in data:
        if not isinstance(data['content'], str):
            return jsonify({'message': 'Content must be a string.'}), 400
        post.content = data['content']
        
    db.session.commit()
    return jsonify({'message': 'Post updated successfully!', 'post': post.to_dict()}), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404
    if post.user_id != g.current_user.id and not g.current_user.is_admin:
        return jsonify({'message': 'You are not authorized to delete this post.'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully!'}), 200

@app.route('/posts/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404

    existing_like = Like.query.filter_by(post_id=post_id, user_id=g.current_user.id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this post.'}), 409

    new_like = Like(post_id=post_id, user_id=g.current_user.id)
    db.session.add(new_like)
    db.session.commit()

    # Create notification for the post author (if not self-liking and preferences allow)
    if post.user_id != g.current_user.id:
        author_receive_like_notif = PrivacySetting.query.filter_by(
            user_id=post.user_id, setting_name='receive_like_notifications'
        ).first()
        if not author_receive_like_notif or author_receive_like_notif.setting_value:
            create_notification(post.user_id, 'like', f'{g.current_user.full_name or g.current_user.email} liked your post "{post.title}".', post.id)

    return jsonify({'message': 'Post liked successfully!'}), 200

@app.route('/posts/<int:post_id>/like', methods=['DELETE'])
@token_required
def unlike_post(post_id):
    like = Like.query.filter_by(post_id=post_id, user_id=g.current_user.id).first()
    if not like:
        return jsonify({'message': 'You have not liked this post.'}), 404

    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Post unliked successfully!'}), 200

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(post_id):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'message': 'Comment content is required.'}), 400
    if not isinstance(content, str):
        return jsonify({'message': 'Comment content must be a string.'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404

    new_comment = Comment(post_id=post_id, user_id=g.current_user.id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    # Create notification for the post author (if not self-commenting and preferences allow)
    if post.user_id != g.current_user.id:
        author_receive_comment_notif = PrivacySetting.query.filter_by(
            user_id=post.user_id, setting_name='receive_comment_notifications'
        ).first()
        if not author_receive_comment_notif or author_receive_comment_notif.setting_value:
            create_notification(post.user_id, 'comment', f'{g.current_user.full_name or g.current_user.email} commented on your post "{post.title}".', post.id)

    return jsonify({'message': 'Comment added successfully!', 'comment': new_comment.to_dict()}), 201

@app.route('/posts/<int:post_id>/comments', methods=['GET'])
@token_required
def get_post_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found.'}), 404
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

# Search and Discovery
@app.route('/search/users', methods=['GET'])
@token_required
def search_users():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'message': 'Search query is required.'}), 400

    # Case-insensitive search by email or full name for active users
    users_raw = User.query.filter(User.is_suspended == False).filter(
        (User.email.ilike(f'%{query}%')) |
        (User.full_name.ilike(f'%{query}%'))
    ).all()

    # Filter out users who have explicitly set privacy not to be searched
    searchable_users = []
    for user in users_raw:
        can_be_searched_setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name='can_be_searched').first()
        if not can_be_searched_setting or can_be_searched_setting.setting_value:
            searchable_users.append(user.to_dict())

    # Search suggestions and additional filters would require more complex logic
    # (e.g., dedicated search engine, aggregated data, separate endpoints).
    return jsonify(searchable_users), 200

@app.route('/search/posts', methods=['GET'])
@token_required
def search_posts():
    keyword = request.args.get('keyword', '').strip()
    filter_by_user_id = request.args.get('user_id', type=int)
    # Additional filters (e.g., 'tag', 'date_range') could be added here.

    if not keyword:
        return jsonify({'message': 'Search keyword is required.'}), 400

    posts_query = Post.query.filter(
        (Post.title.ilike(f'%{keyword}%')) |
        (Post.content.ilike(f'%{keyword}%'))
    )

    if filter_by_user_id:
        posts_query = posts_query.filter_by(user_id=filter_by_user_id)

    posts = posts_query.order_by(Post.created_at.desc()).all()

    # Search suggestions (e.g., popular keywords, autocomplete) are out of scope for a single file.
    return jsonify([post.to_dict() for post in posts]), 200

# Notifications
@app.route('/notifications', methods=['GET'])
@token_required
def get_user_notifications():
    notifications = Notification.query.filter_by(user_id=g.current_user.id).order_by(Notification.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notifications]), 200

@app.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@token_required
def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found.'}), 404
    if notification.user_id != g.current_user.id:
        return jsonify({'message': 'You are not authorized to mark this notification as read.'}), 403

    notification.is_read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked as read.', 'notification': notification.to_dict()}), 200

@app.route('/notifications/preferences', methods=['GET'])
@token_required
def get_notification_preferences():
    # Notification preferences are managed as specific PrivacySettings.
    preferences = PrivacySetting.query.filter(
        PrivacySetting.user_id == g.current_user.id,
        PrivacySetting.setting_name.in_(['receive_like_notifications', 'receive_comment_notifications', 'receive_follower_notifications'])
    ).all()
    return jsonify([p.to_dict() for p in preferences]), 200

@app.route('/notifications/preferences', methods=['PUT'])
@token_required
def update_notification_preferences():
    user = g.current_user
    data = request.get_json() # Expected: {'receive_like_notifications': True/False, ...}

    allowed_settings = ['receive_like_notifications', 'receive_comment_notifications', 'receive_follower_notifications']

    for setting_name, setting_value in data.items():
        if setting_name not in allowed_settings:
            return jsonify({'message': f"Invalid notification preference setting: '{setting_name}'"}), 400
        if not isinstance(setting_value, bool):
            return jsonify({'message': f"Invalid value for '{setting_name}'. Must be boolean."}), 400

        setting = PrivacySetting.query.filter_by(user_id=user.id, setting_name=setting_name).first()
        if setting:
            setting.setting_value = setting_value
        else:
            # Create if a specific notification preference was not yet set (e.g., if new settings are introduced)
            new_setting = PrivacySetting(user_id=user.id, setting_name=setting_name, setting_value=setting_value)
            db.session.add(new_setting)
    db.session.commit()
    return jsonify({'message': 'Notification preferences updated successfully!'}), 200

# Follow/Unfollow for follower notifications
@app.route('/users/<int:user_id>/follow', methods=['POST'])
@token_required
def follow_user(user_id):
    followed_user = User.query.get(user_id)
    if not followed_user:
        return jsonify({'message': 'User not found.'}), 404
    if followed_user.id == g.current_user.id:
        return jsonify({'message': 'You cannot follow yourself.'}), 400
    if followed_user.is_suspended:
        return jsonify({'message': 'Cannot follow a suspended user.'}), 403

    existing_follow = Follow.query.filter_by(follower_id=g.current_user.id, followed_id=user_id).first()
    if existing_follow:
        return jsonify({'message': 'You are already following this user.'}), 409

    new_follow = Follow(follower_id=g.current_user.id, followed_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    # Create notification for the followed user (if preferences allow)
    followed_user_receive_follower_notif = PrivacySetting.query.filter_by(
        user_id=followed_user.id, setting_name='receive_follower_notifications'
    ).first()
    if not followed_user_receive_follower_notif or followed_user_receive_follower_notif.setting_value:
        create_notification(followed_user.id, 'follow', f'{g.current_user.full_name or g.current_user.email} started following you.', g.current_user.id)

    return jsonify({'message': f'You are now following {followed_user.email}.'}), 200

@app.route('/users/<int:user_id>/unfollow', methods=['DELETE'])
@token_required
def unfollow_user(user_id):
    follow_relation = Follow.query.filter_by(follower_id=g.current_user.id, followed_id=user_id).first()
    if not follow_relation:
        return jsonify({'message': 'You are not following this user.'}), 404

    db.session.delete(follow_relation)
    db.session.commit()
    return jsonify({'message': 'You have unfollowed this user.'}), 200
    
# --- Application startup ---
def initialize_database():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)

