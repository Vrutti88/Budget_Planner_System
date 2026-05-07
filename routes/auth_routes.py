from flask import request, jsonify
from routes import auth_bp
from models.user import db, User

@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.json

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered"})


@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data['email'],
        password_hash=data['password']
    ).first()

    if user:
        return jsonify({"status": "success", "user_id": user.user_id})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"})