from api.db.read_from_db import db



class authenticate_repository:

    user_collection = db["Users"]

    def fetch_user(self, email: str):
        try:
            print(f"Printing email receive in fetch argument {email}")
            user = self.user_collection.find_one({"email": email}, {"_id": 0})
            return user
        except Exception as ex:
            print(f"Unable to fetch user: {ex}")
            return None

    def verify_email(self, token):
        try:
            user = self.user_collection.find_one({"verificationToken": token}, {"_id": 0})
            if user:
                self.user_collection.update_one({"verificationToken": token},
                                                {"$set": {"isVerified": True, "verificationToken": None}})
                return True
            return False
        except Exception as ex:
            print(f"Unable to verify email: {ex}")
            return False

    def create_user(self, data):
        try:
            self.user_collection.insert_one(data)
            user = self.user_collection.find_one({"email": data.get("email")}, {"_id": 0})
            return user
        except Exception as ex:
            print(f"Unable to create user: {ex}")
            return None

    def update_user_profile_status(self, userId):
        try:
            update_query = {"$set": {"isProfiled": True}}
            filter_query = {"userId": userId}
            self.user_collection.update_one(filter_query, update_query)
        except Exception as ex:
            print(f"Unable to create user: {ex}")
    def find_user_by_id(self, user_id):
        try:
            user = self.user_collection.find_one({"userId": user_id}, {"_id": 0})
            return user
        except Exception as ex:
            print(f"Unable to fetch user: {ex}")
            return None
