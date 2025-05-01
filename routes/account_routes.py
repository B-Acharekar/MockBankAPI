from flask import Blueprint, request, jsonify
from models.account_model import AccountModel
from emailsend import send_email_otp


account_bp = Blueprint('account', __name__)

@account_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    otp = "123456"  # You can randomize and store later
    response = send_email_otp(email, otp)

    if response.status_code == 200:
        return jsonify({"message": "OTP sent"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500


@account_bp.route('/link', methods=['POST'])
def link_account():
    # Receive data from the frontend
    data = request.json
    bank_id = data.get('bank_id')
    account_type = data.get('account_type')
    account_number = data.get('account_number')
    email = data.get('email')
    otp = data.get('otp')  # Example OTP for validation
    
    # Validate OTP (mock OTP validation)
    generated_otp = "123456"  # Or: str(random.randint(100000, 999999))
    send_email_otp(email, generated_otp)

    if otp != generated_otp:
        return jsonify({"error": "Invalid OTP"}), 400

    # For now, we assume the logged-in user ID is retrieved from session or context
    user_id = "935adb18-046c-4dbe-b263-f8e387cbdd84"  # Example user_id for now

    # Mask the account number
    masked_account_number = "XXXXXX" + account_number[-4:]

    # Link the account directly using AccountModel
    result = AccountModel.link_account(
        user_id=user_id,
        bank_id=bank_id,
        account_number=account_number,
        masked_account_number=masked_account_number,
        balance=0.00  # Assume initial balance is 0
    )

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@account_bp.route('/unlink', methods=['POST'])
def unlink_account():
    data = request.json
    account_number = data.get('account_number')
    # For now, we assume the logged-in user ID is retrieved from session or context
    user_id = "935adb18-046c-4dbe-b263-f8e387cbdd84"  # Example user_id for now

    result = AccountModel.unlink_account(user_id=user_id, account_number=account_number)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@account_bp.route('/<account_number>', methods=['GET'])
def get_account(account_number: str):
    """Fetch an account by account number."""
    account = AccountModel.get_account_by_number(account_number)
    if not account:
        return jsonify({"error": "Account not found."}), 404
    return jsonify(account), 200

@account_bp.route('/user/<user_id>', methods=['GET'])
def get_user_accounts(user_id: str):
    """Fetch all accounts linked to a user."""
    accounts = AccountModel.get_user_accounts(user_id)
    return jsonify(accounts), 200
