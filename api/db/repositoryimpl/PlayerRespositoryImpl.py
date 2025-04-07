from typing import Optional, List

from ..repository.PlayerRepository import Player
from ..db_config import db
from api.modelEntity.builder.property_config import user_session_allows


class PlayerRepositoryData(Player):
    player_register = db["playerRegisteredSession"]
    game_register = db["gameRegister"]
    subscriber_collection = db["userDetail"]
    play_history_collection = db["playHistory"]
    questionsCollection = db["questionBucket"]

    def register_player(self, data: dict):
        try:
            self.player_register.insert_one(data)
            # fetch game details
            gameQuery = {"gameId": data["gameId"]}
            game_response = self.game_register.find_one(gameQuery, {"_id": 0})
            print(f"Game Response: {game_response}")

            output = {
                "playerId": data["playerId"],
                "gameId": game_response["gameId"],
                "timerEnabled": game_response["timerEnabled"],
                "gameTitle": game_response.get("gameTitle"),
                "nickname": data["nickname"],
                "gameType": game_response["gameType"],
                "geoAllowedTime": game_response.get("timeAllowed", 0),
                "totalQuestion": game_response.get("totalQuestion")
            }
            # print(f"Player registered successfully {response}")
            return output
        except Exception as e:
            print(f"Error registering the player {e}")

    def fetch_leader_board(self, gameId: str) -> dict:
        try:

            leader_board_query = [
                # Match documents for the specified game
                {"$match": {"gameId": gameId}},

                # Lookup nickname from the playerRegistrationsession collection
                {
                    "$lookup": {
                        "from": "playerRegisteredSession",  # Join with this collection
                        "localField": "playerId",  # Use playerId for lookup
                        "foreignField": "playerId",  # Match with playerId in registrations
                        "as": "registration_details"  # Output array field
                    }
                },

                # Unwind the registration_details array
                {
                    "$unwind": {
                        "path": "$registration_details",
                        "preserveNullAndEmptyArrays": True  # Include players even if no registration data
                    }
                },

                # Group by playerId and aggregate points and time, including nickname
                {
                    "$group": {
                        "_id": "$playerId",  # Group by playerId
                        "totalPoints": {"$sum": "$points"},  # Sum points
                        "totalTime": {"$sum": "$timeTaken"},  # Sum time taken
                        "nickname": {"$first": "$registration_details.nickname"}  # Get the first nickname
                    }
                },

                # Project the final output
                {
                    "$project": {
                        "_id": 0,  # Exclude the _id field
                        "playerId": "$_id",  # Include playerId
                        "totalPoints": 1,  # Include totalPoints
                        "totalTime": 1,  # Include totalTime
                        "nickname": {"$ifNull": ["$nickname", "Unknown"]}  # Default value if no match
                    }
                }
            ]

            play_hist_response = list(self.play_history_collection.aggregate(leader_board_query))
            response = {"leaderBoard": play_hist_response}
            print(f"Game registered successfully {response}")
            return {"leaderBoard": play_hist_response}
        except Exception as e:
            print(f"Error in fetching leder board {e}")

    def submit_question(self, data: dict) -> dict:
        try:
            countPlayHistory = self.play_history_collection.count_documents(
                {"gameId": data["gameId"], "playerId": data["playerId"]})

            data["roundTrip"] = countPlayHistory + 1

            self.play_history_collection.insert_one(data)
        except Exception as ex:
            print(f"Error in registering game {e}")

    def fetch_next_unplayed_question(self, data: dict) -> dict:
        try:
            # Step 1: Get questionIds from gameRegister for the gameId
            game_register = db["gameRegister"].find_one({"gameId": data["gameId"]}, {"questionIds": 1, "_id": 0})

            if not game_register or not game_register.get("questionIds"):
                return {"unplayed_questions": [], "playHistoryCount": 0}

            question_ids = game_register["questionIds"]

            # Step 2: Get played questionIds from playHistory for the gameId and playerId
            played_questions = db["playHistory"].find(
                {"gameId": data["gameId"], "playerId": data["playerId"]},
                {"questionId": 1, "_id": 0}
            )
            # subtract played Id from game Question Ids

            played_question_ids = [doc["questionId"] for doc in played_questions]
            # print(f"played IDs {played_question_ids}")
            # print(f"GameIds=> {question_ids}")

            remaining_ids = list(set(question_ids) - set(played_question_ids))
            print(f"Remaining ids {remaining_ids}")

            # Step 3: Query questionBucket for unplayed questions
            unplayed_questions = list(db["questionBucket"].find(
                {"questionId": {"$in": remaining_ids}},
                {"_id": 0}
            ))

            # Step 4: Count playHistory entries for the gameId and playerId
            play_history_count = db["playHistory"].count_documents(
                {"gameId": data["gameId"], "playerId": data["playerId"]})
            next_question = [] if not unplayed_questions else unplayed_questions[0]

            return {"unplayedQuestions": next_question, "playHistoryCount": play_history_count}

        except Exception as ex:
            print(f"error fetch next question {ex}")
            return {}

    def close_game(self, game_id: str, initiator: str) -> None:
        pass

    def check_all_player_submitted(self, game_id) -> dict:
        pass

    def confirm_game_open(self, game_id) -> dict:
        pass

    def find_active_game_player(self, game_id: str) -> List[dict]:
        try:
            pipeline = [
                # Match documents with the specified gameId
                {"$match": {"gameId": game_id}},

                # Project only the nickname and playerId fields
                {
                    "$project": {
                        "_id": 0,  # Exclude the _id field
                        "nickname": 1,  # Include the nickname field
                        "playerId": 1  # Include the playerId field
                    }
                }
            ]

            # Execute the aggregation
            players = list(self.player_register.aggregate(pipeline))
            print(f"Spill players {players}")
            return players if players else []
        except Exception as ex:
            print(f"Error occurred fetching active users {ex}")
            return []

    def retrieve_game_details(self, game_id) -> dict:
        try:
            game_result = self.game_register.find_one(
                {"gameId": game_id},
                {"_id": 0}
            )
            
            if not game_result:

                return {}
            # Query the `userDetail` collection
            if game_result:
                subscriber = self.subscriber_collection.find_one(
                    {"subscriberId": game_result.get("gameOwnerId")},
                    {"_id": 0, "active": 1, "subscriptionPlan": 1})

                if subscriber:
                    # Merge the results
                    result = {
                        "gameId": game_result["gameId"],
                        "totalQuestion": game_result.get("totalQuestion"),
                        "gameOpen": game_result["gameOpen"],
                        "timerEnabled": game_result["timerEnabled"],
                        "active": subscriber["active"],
                        "subscriptionPlan": subscriber["subscriptionPlan"],
                        "gameType": game_result["gameType"],
                        # "geoLocations": game_result["geoLocations"]
                    }
                    return result

            result = {
                "gameId": game_result["gameId"],
                "totalQuestion": game_result.get("totalQuestion"),
                "gameOpen": game_result["gameOpen"],
                "timerEnabled": game_result["timerEnabled"],
                "gameType": game_result["gameType"]
            }

            return result
        except Exception as ex:
            print(f"Error fetching game details {ex}")
            return {}

    def find_registered_player_per_game(self, data: dict) -> Optional[dict]:
        try:
            record = self.player_register.find_one(
                {"gameId": data.get("gameId"),
                 "nickname": {"$regex": f"^{data.get('nickname')}$", "$options": "i"}},
                {"_id": 0, "playerId": 1, "nickname": 1, "gameId": 1, "gameOwnerId": 1, "gameType": 1,
                 "subscriptionPlan": 1}
                # Case-insensitive regex}
            )
            if record:
                return record
            else:
                return {}

        except Exception as ex:
            return {}

    def max_session_limit_exceeded(self, subscriptionPlan, gameId) -> bool:
        try:
            total_count = self.player_register.count_documents({"gameId": gameId})
            return total_count == user_session_allows[subscriptionPlan]

        except Exception as ex:
            print(f"Error fetching session {ex}")
            return False

    def find_question(self, question_id: str) -> Optional[dict]:
        try:
            question_record = self.questionsCollection.find_one({"questionId": question_id})
            if question_record:
                return question_record
            else:
                return {}
        except Exception as ex:
            return {}
