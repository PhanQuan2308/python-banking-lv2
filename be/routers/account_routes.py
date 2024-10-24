from flask import Blueprint, jsonify
from flask_jwt_extended import (get_jwt_identity,  # Sử dụng JWT để lấy user_id
                                jwt_required)
from models import Account

account_bp = Blueprint('account', __name__)

@account_bp.route('/api/v1/balance', methods=['GET'])
@jwt_required() 
def get_balance():
    user_id = get_jwt_identity() 
    
    account_id = Account.get_account_id_by_user(user_id)
    if account_id:
        balance = Account.get_balance(account_id)
        if balance is not None:
            return jsonify({'balance': balance}), 200
        else:
            return jsonify({'message': 'Account not found'}), 404
    return jsonify({'message': 'User does not have an account'}), 404
