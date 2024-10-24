from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import bcrypt
from models import Account

user_bp = Blueprint("user", __name__)

@user_bp.route("/api/v1/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        result = User.create_user(data["name"], data["email"], data["password"])

        if isinstance(result, dict) and "error" in result:
            return jsonify({"message": result["error"]}), 400

        if result is None:
            return jsonify({"message": "Internal server error"}), 500

        user_id = result
        Account.create_account_for_user(user_id)
        return jsonify({"message": "User registered successfully and account created!"}), 201
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"message": "Internal server error"}), 500


@user_bp.route("/api/v1/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.verify_user(data["email"], data["password"])
    if user:
        access_token = create_access_token(identity=user["id"])
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route("/api/v1/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    data = request.get_json()
    user_id = get_jwt_identity()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    user = User.get_user_by_id(user_id)
    if not user or not bcrypt.check_password_hash(user["password"], current_password):
        return jsonify({"message": "Current password is incorrect"}), 401

    hashed_new_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    User.update_password(user_id, hashed_new_password)

    return jsonify({"message": "Password changed successfully!"}), 200
