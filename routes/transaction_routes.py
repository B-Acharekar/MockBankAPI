from flask import Blueprint, request, jsonify
from utils.socketio_instance import socketio
from models.transaction_model import TransactionModel
from models.account_model import AccountModel
from config import mongo

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/create', methods=['POST'])
def create_transaction():
    data = request.json
    account_id = data.get('account_id')
    amount = data.get('amount')
    txn_type = data.get('type')  # "credit" or "debit"
    description = data.get('description')

    if not all([account_id, amount, txn_type, description]):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate account exists
    account = AccountModel.get_account_by_number(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Extract user_id from the account (this assumes 'user_id' exists in the account data)
    user_id = account.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID not found for the account"}), 404

    # Add transaction (pass user_id to associate the transaction with the user)
    txn = TransactionModel.add_transaction(
        account_id=account_id,
        user_id=user_id,  # Pass the user_id to the transaction model
        amount=amount,
        txn_type=txn_type,
        description=description
    )

    # Update account balance
    multiplier = 1 if txn_type == 'credit' else -1
    new_balance = account['balance'] + (amount * multiplier)
    mongo.db.accounts.update_one(
        {"account_number": account_id},
        {"$set": {"balance": new_balance}}
    )

    # Emit real-time update to frontend (using user_id as the room)
    socketio.emit('new_transaction', {
        'account_id': account_id,
        'amount': amount,
        'type': txn_type,
        'description': description,
        'timestamp': str(txn['timestamp'])
    }, room=user_id)  # Emit to user_id's room, assuming the user joined this room

    return jsonify(txn), 201


@transaction_bp.route('/account/<account_id>', methods=['GET'])
def get_transactions(account_id):
    """Get latest 20 transactions for an account."""
    txns = TransactionModel.get_transactions_by_account(account_id)
    return jsonify(txns), 200


@transaction_bp.route('/user/<user_id>', methods=['GET'])
def get_transactions_by_user(user_id):
    """Get latest 20 transactions for a user (across all accounts)."""
    txns = TransactionModel.get_transactions_by_user(user_id)
    if not txns:
        return jsonify({"error": "No transactions found for this user."}), 404
    return jsonify(txns), 200


@transaction_bp.route('/<txn_id>', methods=['GET'])
def get_transaction_by_id(txn_id):
    txn = TransactionModel.get_transaction_by_id(txn_id)
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(txn), 200
