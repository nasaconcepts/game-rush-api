from ..db_config import db
from ..repository.GeoPlayRepository import GeoPlay
from typing import Optional
class geoPlayRepositoryImpl(GeoPlay):
    player_register = db["playerRegisteredSession"]
    geo_game_register = db["gameRegister"]
    geo_play_history = db["geoPlayHistory"]
    def register_geo_player(self, data: dict) -> dict:
        try:
            self.player_register.insert_one(data)
            # fetch game details

            game_response = self.geo_game_register.insert_one(data)
            output = {
                "playerId": data["playerId"],
                "gameId": game_response["game_id"],
                "gameTitle": game_response.get("gameTitle"),
                "nickname": data["nickname"]
            }
            return output
        except Exception as e:
            print(f"Error registering the player {e}")
    def fetch_geo_leader_board(self, gameId: str):
        try:
            leader_board_query = [
                # Match documents for the specified game
                {"$match": {"gameId": gameId}},

                # Lookup nickname from the geoPlayerSession collection
                {
                    "$lookup": {
                        "from": "playerRegisteredSession",  # Join with this collection
                        "localField": "playerId",   # Use playerId for lookup
                        "foreignField": "playerId", # Match with playerId in registrations
                        "as": "registration_details"  # Output array field
                    }
                },

                # Unwind the registration_details array (ensure null values are preserved)
                {
                    "$unwind": {
                        "path": "$registration_details",
                        "preserveNullAndEmptyArrays": True
                    }
                },

                # Group by playerId and aggregate points and time, including nickname
                {
                    "$group": {
                        "_id": "$playerId",
                        "totalPoints": {"$sum": "$scorePoint"},
                        "totalTime": {"$sum": "$timeTaken"},
                        "nickname": {"$first": "$registration_details.nickname"}  # Use after unwinding
                    }
                },

                # Project the final output
                {
                    "$project": {
                        "_id": 0,
                        "playerId": "$_id",
                        "totalPoints": 1,
                        "totalTime": 1,
                        "nickname": {"$ifNull": ["$nickname", "Unknown"]}  # Default to "Unknown"
                    }
                }
            ]

            leader_board = list(self.geo_play_history.aggregate(leader_board_query))
            return {"leaderBoard": leader_board}
        except Exception as e:
            print(f"Error fetching leader board {e}")

    def submit_geoplay(self, data: dict) -> dict:
        try:
            self.geo_play_history.insert_one(data)
        except Exception as e:
            print(f"Error saving play history {e}")
    def fetch_geoplay_round(self, gameId: str) -> Optional[dict]:
      try:
          gameQuery= {"gameId":gameId}
          game_details = self.geo_game_register.find_one(gameQuery, {"_id": 0})
          return game_details
      except Exception as e:
          print(f"Error fetch game details")

    def confirm_game_played(self, data: dict) -> Optional[list[dict]]:
        try:
            history_query = {"gameId": data["gameId"], "playerId": data["playerId"]}
            history = self.geo_play_history.find(history_query, {"_id": 0})
            return list(history)
        except Exception as e:
            print(f"Error fetching play history {e}")
    def fetch_attempted_geo_locations_per_round(self,gameId,playerId):
            try:
            # 1️⃣ Get the max roundTrip for the player
                max_round_doc = self.geo_play_history.find_one(
                    {"gameId": gameId, "playerId": playerId},
                    sort=[("roundTrip", -1)]  # Sort in descending order to get the max round
                )

                if not max_round_doc:
                    return {"error": "No game history found for this player."}

                max_round = max_round_doc["roundTrip"]
                print(f"Max Number {max_round}")

                # 2️⃣ Fetch all players who played this round & attempted the game
                pipeline = [
                    {"$match": {"gameId": gameId, "roundTrip": max_round, "attempted": True}},

                    # 3️⃣ Lookup player details from PlayerSession
                    {
                        "$lookup": {
                            "from": "playerRegisteredSession",
                            "localField": "playerId",
                            "foreignField": "playerId",
                            "as": "player_details"
                        }
                    },

                    # 4️⃣ Unwind player_details (if no match, keep empty)
                    {"$unwind": {"path": "$player_details", "preserveNullAndEmptyArrays": True}},

                    # 5️⃣ Project required fields
                    {
                        "$project": {
                            "_id": 0,
                            "playerId": 1,
                            "nickname": {"$ifNull": ["$player_details.nickname", "Unknown"]},
                            "distance": 1,
                            "scorePoint": 1,
                            "guessedLocation": 1,
                            "timeTaken": 1,
                            "roundTrip": 1,
                            "attempted": 1
                        }
                    }
                ]

                result = list(self.geo_play_history.aggregate(pipeline))


                return {"currentRoundTrip":max_round,"playerLocations":result }

            except Exception as e:
                return {"error while fetching attempted locations": str(e)}
    def get_stat_of_player_per_round(self,gameId,playerId):

        try:
            # 1️⃣ Find the max roundTrip for the player
            max_round_doc = self.geo_play_history.find_one(
                {"gameId": gameId, "playerId": playerId},
                sort=[("roundTrip", -1)]  # Sort descending to get the max roundTrip
            )

            if not max_round_doc:
                return {"error": "No game history found for this player."}

            max_round = max_round_doc["roundTrip"]

            # 2️⃣ Count records in geoHistory where roundTrip == max_round
            geo_history_count = self.geo_play_history.count_documents(
                {"gameId": gameId, "roundTrip": max_round}
            )

            # Count the number of player records in PlayerSession for this game
            player_session_count = self.player_register.count_documents(
                {"gameId": gameId}
            )

            return {
                "currentRound": max_round,
                "geoPlayedHistoryCount": geo_history_count,
                "playerSessionCount": player_session_count
            }

        except Exception as e:
            return {"error": str(e)}

