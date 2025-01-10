from typing import Optional
from rest_framework.response import Response

from ..repository.UserRepository import User
from ..db_config import db

class UserRepositoryImpl(User):
    user_collection = db["userDetail"]
    question_collection = db["questionBucket"]
    game_collection = db["games"]
    def create_subscriber(self,data:dict):
        try:
            user_exist_query = {"username":data["username"]}

            user = self.user_collection.find_one(user_exist_query)

            if user:
                print(f"My User Detail => {user}")
                raise ValueError("User already exist")
            else:
                # new_user = self.user_collection.insert_one(data)
                new_user = db.userDetail.insert_one(data)
                return new_user

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def create_questions(self,data:list):
        try:
            # validate the the none of the array id already exist in the database
            self.question_collection.insert_many(data)

        except Exception as ex:
            print(f"Error while inserting bulk question record {ex}")

    def get_user(self,username)->Optional[dict]:
        try:
            user_query = {"username":username}
            user =  self.user_collection.find_one(user_query)
            return user
        except Exception as e:
            print(f"Error retrieving user {e}")
    def create_game(self,data:dict):
        try:
            self.game_collection.insert_one(data)
        except Exception as ex:
            print(f"Error creating game user {e}")