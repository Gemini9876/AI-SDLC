```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    two_factor_auth = db.Column(db.Boolean, default=False)
    profile_info = db.relationship('ProfileInfo', backref='user', uselist=False)

class ProfileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_picture = db.Column(db.String(100))
    email_address = db.Column(db.String(50))
    privacy_preferences = db.Column(db.String(50))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    if user:
        # Implement password reset logic here
        return jsonify({'message': 'Password reset successful'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    two_factor_auth = data.get('two_factor_auth', False)
    
    new_user = User(email=email, password=password, two_factor_auth=two_factor_auth)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    email = data.get('email')
    profile_picture = data.get('profile_picture')
    new_email = data.get('new_email')
    privacy_preferences = data.get('privacy_preferences')
    
    user = User.query.filter_by(email=email).first()
    if user:
        user.profile_info.profile_picture = profile_picture
        user.profile_info.email_address = new_email
        user.profile_info.privacy_preferences = privacy_preferences
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    db.create_all()
    app.run()
```