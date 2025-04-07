from tokenize import group
from typing import Optional
from rest_framework.response import Response
import math

from ..repository.UserRepository import User
from ..db_config import db
from api.modelEntity.builder.Builder import subscriber_game_list


class UserRepositoryImpl(User):
    user_collection = db["userDetail"]
    question_collection = db["questionBucket"]
    game_collection = db["gameRegister"]
    player_register = db["playerRegisteredSession"]
    play_geo_history = db["geoPlayHistory"]
    play_quiz_history = db["playHistory"]

    def create_subscriber(self, data: dict):
        try:
            user_exist_query = {"subscriberId": data["subscriberId"]}

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

    def create_questions(self, data: list):
        try:
            # validate the the none of the array id already exist in the database
            self.question_collection.insert_many(data)

        except Exception as ex:
            print(f"Error while inserting bulk question record {ex}")

    def get_user(self, username) -> Optional[dict]:
        try:
            user_query = {"username": username}
            user = self.user_collection.find_one(user_query)
            return user
        except Exception as e:
            print(f"Error retrieving user {e}")

    def create_game(self, data: dict):
        try:
            print(f"Print before creation {data}")
            self.game_collection.insert_one(data)
        except Exception as ex:
            print(f"Error creating game user {ex}")

    def get_games(self, gameOwnerId: str) -> Optional[list]:
        try:
            game_query = {"gameOwnerId": gameOwnerId}
            games = self.game_collection.find(game_query)
            return games
        except Exception as e:
            print(f"Error retrieving game {e}")
            return []

    def get_players_per_gameType(self, data: dict):
        try:

            game_query = {"gameType": data["gameType"], "gameId": data["gameId"]}
            players = list(self.player_register.find(game_query, {"_id": 0}))
            return players if players else []
        except Exception as e:
            print(f"Error retrieving game {e}")
            return []

    def get_playground_play(self, data: dict):
        try:
            game_query = {"gameId": data["gameId"]}
            game = self.game_collection.find_one(game_query)
            if not game:
                return {"error": "Game not found"}

            if game:
                if game["gameType"] == "geoplay":
                    # handle bound beyong max play
                    if data["roundTrip"] > game["totalRound"]:
                        return {"error": "Max roundTrip exceeded"}
                    # extra the target location
                    targetLocation = game["geoLocations"][data["roundTrip"] - 1]
                    game["targetLocation"] = targetLocation
                    playGeoHistoryQuery = [{"$match": {"gameId": data["gameId"]}},
                                           {"$group": {"_id": "$playerId"}},
                                           {"$count": "maxRoundPlayed"}]
                    playHistoryGeoCount = list(self.play_geo_history.aggregate(playGeoHistoryQuery))

                    output = {
                        "gameId": game["gameId"],
                        "gameType": game["gameType"],
                        "targetLocation": game["targetLocation"],
                        "maxRound": game["totalRound"],
                        "maxRoundPlayed": playHistoryGeoCount[0]["maxRoundPlayed"] if len(
                            playHistoryGeoCount) > 0 else 0
                    }
                    print(f"output Data preview=>{output}")
                    return output
                if game["gameType"] == "quiz":

                    # handle bound beyong max play
                    if data["roundTrip"] > game["totalQuestion"]:
                        return {"error": "Max roundTrip exceeded"}
                    questionId = game["questionIds"][data["roundTrip"] - 1]
                    print(f"Question preview=>{questionId}")
                    questionQuery = {"questionId": questionId}
                    question = self.question_collection.find_one(questionQuery, {"_id": 0})
                    print(f"Question preview 2=>{question}")
                    playQuizHistoryQuery = [{"$match": {"gameId": data["gameId"]}},
                                            {"$group": {"_id": "$playerId"}},
                                            {"$count": "maxRoundPlayed"}]
                    playHistoryGeoCount = list(self.play_quiz_history.aggregate(playQuizHistoryQuery))
                    print(f"playHistoryGeoCount preview =>{playHistoryGeoCount}")

                    output = {
                        "gameId": game["gameId"],
                        "gameType": game["gameType"],
                        "question": question,
                        "maxRound": game["totalQuestion"],
                        "maxRoundPlayed": playHistoryGeoCount[0]["maxRoundPlayed"] if len(
                            playHistoryGeoCount) > 0 else 0
                    }

                    return output
        except Exception as e:
            print(f"Error retrieving game {e}")
            return {"error": "Game encountered an error"}

    def get_playground_geo_leaderboard(self, data: dict):
        try:
            game_result = self.game_collection.find_one(
                {"gameId": data.get("gameId")},
                {"_id": 0}
            )
            if not game_result:
                return {"error": "Game not found"}
            # check if roundTrip is greater than totalRound

            if data.get("roundTrip") > game_result.get("totalRound"):
                return {"error": "Max roundTrip exceeded"}
            pipeline_summary = [
                {"$match": {"gameId": data["gameId"], "roundTrip": {"$lte": data.get("roundTrip")}}},
                # Filter gameId and roundTrip

                # Group by playerId to calculate total score and total time
                {
                    "$group": {
                        "_id": "$playerId",
                        "totalPoints": {"$sum": "$scorePoint"},
                        "totalTime": {"$sum": "$timeTaken"},
                    }
                },

                # Lookup player nickname from playerRegisteredSession
                {
                    "$lookup": {
                        "from": "playerRegisteredSession",
                        "localField": "_id",
                        "foreignField": "playerId",
                        "as": "playerInfo"
                    }
                },

                # Unwind playerInfo array to get the first element (nickname)
                {"$unwind": {"path": "$playerInfo", "preserveNullAndEmptyArrays": True}},

                # Add nickname field
                {
                    "$project": {
                        "_id": 0,
                        "playerId": "$_id",
                        "totalPoints": 1,
                        "totalTime": 1,
                        "nickname": {"$ifNull": ["$playerInfo.nickname", "Unknown"]}
                    }
                },

                # Sort by totalPoints in descending order (leaderboard)
                {"$sort": {"totalPoints": -1}}
            ]

            # Execute the aggregation
            leaderboard = list(self.play_geo_history.aggregate(pipeline_summary))

            # Aggregation pipeline for guessed locations
            guessed_location_pipeline = [
                {"$match": {"gameId": data["gameId"], "roundTrip": {"$lte": data.get("roundTrip")}}},
                # Filter by game and roundTrip
                {
                    "$lookup": {
                        "from": "playerRegisteredSession",
                        "localField": "playerId",
                        "foreignField": "playerId",
                        "as": "playerInfo"
                    }
                },
                {"$unwind": {"path": "$playerInfo", "preserveNullAndEmptyArrays": True}},
                {
                    "$project": {
                        "_id": 0,
                        "distance": 1,
                        "scorePoint": 1,
                        "playerId": 1,
                        "guessedLocation": 1,
                        "timeTaken": 1,
                        "roundTrip": 1,
                        "attempted": 1,
                        "nickname": {"$ifNull": ["$playerInfo.nickname", "Unknown"]}
                    }
                }
            ]

            # Execute the aggregation
            pinned_geo_locations = list(self.play_geo_history.aggregate(guessed_location_pipeline))
            #  calculate maximum played game. Pick the the highest roundTrip
            playQuizHistoryQuery = [{"$match": {"gameId": data["gameId"]}},
                                                        {"$group": {"_id": "$playerId"}},
                                                        {"$count": "maxRoundPlayed"}]
            playHistoryGeoCount = list(self.play_quiz_history.aggregate(playQuizHistoryQuery))

            output = {
                "leaderBoard": leaderboard,
                "pinnedGeoLocations": pinned_geo_locations,
                "currentRoundTrip": data.get("roundTrip"),
                "targetLocation": game_result.get("geoLocations")[data.get("roundTrip") - 1],
                "maxRound": game_result.get("totalRound",0),
                "maxRoundPlayed":playHistoryGeoCount[0]["maxRoundPlayed"] if len(
                                                             playHistoryGeoCount) > 0 else 0
            }

            return output
        except Exception as e:
            print(f"Error retrieving game {e}")
            return {"error": "Error retrieving board"}

    def get_playground_quiz_leaderboard(self, data: dict):
        try:
            game_result = self.game_collection.find_one(
                {"gameId": data.get("gameId")},
                {"_id": 0}
            )
            if not game_result:
                return {"error": "Game not found"}
            # check if roundTrip is greater than totalRound

            if data.get("roundTrip") > game_result.get("totalQuestion"):
                return {"error": "Max roundTrip exceeded"}
            pipeline_summary = [
                {"$match": {"gameId": data["gameId"], "roundTrip": {"$lte": data.get("roundTrip")}}},
                # Filter gameId and roundTrip

                # Group by playerId to calculate total score and total time
                {
                    "$group": {
                        "_id": "$playerId",
                        "totalPoints": {"$sum": "$scorePoint"},
                        "totalTime": {"$sum": "$timeTaken"},
                    }
                },

                # Lookup player nickname from playerRegisteredSession
                {
                    "$lookup": {
                        "from": "playerRegisteredSession",
                        "localField": "_id",
                        "foreignField": "playerId",
                        "as": "playerInfo"
                    }
                },

                # Unwind playerInfo array to get the first element (nickname)
                {"$unwind": {"path": "$playerInfo", "preserveNullAndEmptyArrays": True}},

                # Add nickname field
                {
                    "$project": {
                        "_id": 0,
                        "playerId": "$_id",
                        "totalPoints": 1,
                        "totalTime": 1,
                        "nickname": {"$ifNull": ["$playerInfo.nickname", "Unknown"]}
                    }
                },

                # Sort by totalPoints in descending order (leaderboard)
                {"$sort": {"totalPoints": -1}}
            ]

            # Execute the aggregation
            leaderboard = list(self.play_quiz_history.aggregate(pipeline_summary))

            # Aggregation total played games for the game
            #  calculate maximum played game. Pick the the highest roundTrip
            playQuizHistoryQuery = [{"$match": {"gameId": data["gameId"]}},
                                    {"$group": {"_id": "$playerId"}},
                                    {"$count": "maxRoundPlayed"}]
            playHistoryQuizCount = list(self.play_quiz_history.aggregate(playQuizHistoryQuery))



            # Execute the aggregation

            output = {
                "leaderBoard": leaderboard,
                "currentRoundTrip": data.get("roundTrip"),
                "maxRound": game_result.get("totalQuestion",0),
                "maxRoundPlayed":playHistoryQuizCount[0]["maxRoundPlayed"] if len(
                    playHistoryQuizCount) > 0 else 0
            }

            return output
        except Exception as e:
            print(f"Error retrieving game {e}")
            return {"error": "Error retrieving board"}
    def get_games_pagination(self,data:dict):
        try:
            page = data.get("page",1)
            limit = data.get("limit",10)
            skip = (page - 1) * limit

            # order by create date descending
            query_pagination= {"gameOwnerId":data["gameOwnerId"]}
            countGames = self.game_collection.count_documents(query_pagination)
            if countGames == 0:
                return {"games":[],"pagination": {
                    "currentPage": 0,
                    "pageSize": limit,
                    "totalPages": 0,
                    "totalItems": 0,
                    "hasNextPage": False,
                    "hasPrevPage": False
                }}
            games = list(self.game_collection.find(query_pagination,{"_id": 0}).skip(skip).limit(limit).sort([("createdOn",-1)]))
            
        
            if games:
                list_my_games = [subscriber_game_list(game) for game in games]
                totalPages = math.ceil(countGames / limit)
                return {"games": list_my_games,"pagination": {
                    "currentPage": page,
                    "pageSize": limit,
                    "totalPages": totalPages,
                    "totalItems": countGames,
                    "hasNextPage": page <totalPages,
                    "hasPrevPage": page > 1
                }}
            return []
        except Exception as e:
            print(f"Error retrieving game {e}")
            return []