from config import mongo

class UserModel:
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email

    @classmethod
    def create_user(cls, user_id: str, email: str) -> dict:
        """Create a new user in the database."""
        user = {
            "user_id": user_id,
            "email": email,
            "linked_accounts": []
        }
        result = mongo.db.users.insert_one(user)
        return {"_id": str(result.inserted_id), "user_id": user_id, "email": email}

    @classmethod
    def get_user_by_id(cls, user_id: str) -> dict:
        """Retrieve a user from the database by user_id."""
        user = mongo.db.users.find_one({"user_id": user_id})
        if user:
            return {
                "user_id": user["user_id"],
                "email": user["email"],
                "linked_accounts": user["linked_accounts"]
            }
        return None

    @classmethod
    def link_account(cls, user_id: str, account_data: dict) -> dict:
        """Link an account to the user."""
        user = mongo.db.users.find_one({"user_id": user_id})
        if user:
            user["linked_accounts"].append(account_data)
            mongo.db.users.update_one({"user_id": user_id}, {"$set": user})
            return user
        return None

    @classmethod
    def unlink_account(cls, user_id: str, account_number: str) -> dict:
        """Unlink an account from the user."""
        user = mongo.db.users.find_one({"user_id": user_id})
        if user:
            user["linked_accounts"] = [account for account in user["linked_accounts"] if account["account_number"] != account_number]
            mongo.db.users.update_one({"user_id": user_id}, {"$set": user})
            return user
        return None
