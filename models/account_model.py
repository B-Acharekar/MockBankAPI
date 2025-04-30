from config import mongo
from datetime import datetime

class AccountModel:
    def __init__(self, user_id: str, bank_id: str, account_number: str, masked_account_number: str, balance: float):
        self.user_id = user_id
        self.bank_id = bank_id
        self.account_number = account_number
        self.masked_account_number = masked_account_number
        self.balance = balance
        self.linked_at = datetime.utcnow()

    @classmethod
    def link_account(cls, user_id: str, bank_id: str, account_number: str, masked_account_number: str, balance: float) -> dict:
        """Link an account to a user."""
        account_data = {
            "user_id": user_id,
            "bank_id": bank_id,
            "account_number": account_number,
            "masked_account_number": masked_account_number,
            "balance": balance,
            "linked_at": datetime.utcnow()
        }
        result = mongo.db.accounts.insert_one(account_data)
        return {"_id": str(result.inserted_id), "user_id": user_id, "account_number": account_number}

    @classmethod
    def get_account_by_number(cls, account_number: str) -> dict:
        """Retrieve an account by account number."""
        account = mongo.db.accounts.find_one({"account_number": account_number})
        if account:
            return {
                "_id": str(account["_id"]),
                "user_id": account["user_id"],
                "bank_id": account["bank_id"],
                "account_number": account["account_number"],
                "masked_account_number": account["masked_account_number"],
                "balance": account["balance"],
                "linked_at": account["linked_at"]
            }
        return None

    @classmethod
    def get_user_accounts(cls, user_id: str) -> list:
        """Retrieve all linked accounts for a user."""
        accounts = mongo.db.accounts.find({"user_id": user_id})
        return [{"_id": str(account["_id"]), "bank_id": account["bank_id"], "account_number": account["account_number"], "masked_account_number": account["masked_account_number"], "balance": account["balance"], "linked_at": account["linked_at"]} for account in accounts]

    @classmethod
    def unlink_account(cls, user_id: str, account_number: str) -> dict:
        """Unlink an account from the user."""
        account = mongo.db.accounts.find_one({"user_id": user_id, "account_number": account_number})
        if account:
            mongo.db.accounts.delete_one({"_id": account["_id"]})
            return {"message": f"Account {account_number} unlinked successfully."}
        return {"error": "Account not found."}
