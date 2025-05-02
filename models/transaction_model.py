from config import mongo
from datetime import datetime
from bson import ObjectId

class TransactionModel:
    def __init__(self, account_id: str, user_id: str, amount: float, txn_type: str, description: str, timestamp: datetime = None):
        self.account_id = account_id
        self.user_id = user_id  # Include user_id in the transaction model
        self.amount = amount
        self.txn_type = txn_type
        self.description = description
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "user_id": self.user_id,  # Include user_id in the dict
            "amount": self.amount,
            "type": self.txn_type,
            "description": self.description,
            "timestamp": self.timestamp
        }

    @classmethod
    def add_transaction(cls, account_id: str, user_id: str, amount: float, txn_type: str, description: str) -> dict:
        """Insert a new transaction and return the inserted data."""
        transaction = {
            "account_id": account_id,
            "user_id": user_id,  # Store user_id in the transaction
            "amount": amount,
            "type": txn_type,
            "description": description,
            "timestamp": datetime.utcnow()
        }
        result = mongo.db.transaction.insert_one(transaction)
        transaction["_id"] = str(result.inserted_id)
        return transaction

    @classmethod
    def get_transactions_by_user(cls, user_id: str, limit: int = 20) -> list:
        """Fetch recent transactions for a given user (across all accounts)."""
        transactions = mongo.db.transaction.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        return [
            {
                "_id": str(txn["_id"]),
                "account_id": txn["account_id"],
                "user_id": txn["user_id"],
                "amount": txn["amount"],
                "type": txn["type"],
                "description": txn["description"],
                "timestamp": txn["timestamp"]
            }
            for txn in transactions
        ]

    @classmethod
    def get_transactions_by_account(cls, account_id: str, limit: int = 20) -> list:
        """Fetch recent transactions for a given account."""
        transactions = mongo.db.transaction.find({"account_id": account_id}).sort("timestamp", -1).limit(limit)
        return [
            {
                "_id": str(txn["_id"]),
                "account_id": txn["account_id"],
                "user_id": txn["user_id"],
                "amount": txn["amount"],
                "type": txn["type"],
                "description": txn["description"],
                "timestamp": txn["timestamp"]
            }
            for txn in transactions
        ]
