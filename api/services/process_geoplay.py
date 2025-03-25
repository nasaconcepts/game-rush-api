

from datetime import datetime
from api.services.location_service import calculate_distance_between_coordinates_km
from api.db.repositoryimpl.geo_play_repository_Impl import geoPlayRepositoryImpl
from api.util.utils import api_response


class GeoGamePlay:
    geoRepository = geoPlayRepositoryImpl()
    def scorePlayer(self,distance,timeTaken,timeAllowed):
        longest_distance = 220000
        attemptBonus = 50
        score = (longest_distance - distance) /longest_distance*1000+(timeAllowed-timeTaken)/timeAllowed*500+attemptBonus
        return round(score)

    def process_geoplay_submission(self,data):
        # Process the data
        # Get game data
        try:
            gameData = self.geoRepository.fetch_geoplay_round(data["gameId"])

            if gameData == None:
                return api_response(success=False,message="Game does not exist",status=400)

            noOfPlayedGeoGame = len(self.geoRepository.confirm_game_played(data))

            if gameData["totalRound"] == noOfPlayedGeoGame:
                return api_response(success=False,message="Round trip limit exceeded,Game Over!",status=400)
            # Handle zero indexing
            targetLocation = gameData["geoLocations"][noOfPlayedGeoGame-1]

            playerLocation = data["guessedLocation"]

            if playerLocation.get("latitude") ==0 and playerLocation.get("longitude") ==0:
                playerNoAction ={
                    "gameId":gameData["gameId"],
                    "distance":-1,
                    "scorePoint":0,
                    "playerId":data["playerId"],
                    "targetLocation":targetLocation,
                    "guessedLocation":playerLocation,
                    "timeTaken":gameData["timeAllowed"],
                    "playedOn":datetime.now().isoformat(),
                    "roundTrip":(noOfPlayedGeoGame+1),
                    "attempted":False

                }


                self.geoRepository.submit_geoplay(playerNoAction)

                return api_response(success=True,message=f"Round {playerNoAction["roundTrip"]} now played, no action taken by player",status=200)
            # Calculate distance between the two locations
            distance = calculate_distance_between_coordinates_km(playerLocation, targetLocation)

            score = self.scorePlayer(distance,data["timeTaken"],gameData["timeAllowed"])
            playerAction ={
                "gameId":gameData["gameId"],
                "distance":distance,
                "scorePoint":score,
                "playerId":data["playerId"],
                "targetLocation":targetLocation,
                "guessedLocation":playerLocation,
                "timeTaken":data["timeTaken"],
                "playedOn":datetime.now().isoformat(),
                "roundTrip":(noOfPlayedGeoGame+1),
                "attempted":True
            }
            self.geoRepository.submit_geoplay(playerAction)
            return api_response(success=True,message=f"Round {playerAction["roundTrip"]} now played successfully",status=200)
        except Exception as e:
            print(f"Error processing geoplay submission {e}")
            return api_response(success=False,message="Unknown server error",status=500)
    def validated_retrieval(self,data, gameData,geoHistory=[]):
        try:
            if len(geoHistory) ==0:
                response = {
                    "gameId":gameData["gameId"],
                    "roundTrip":1,
                    "targetLocation":gameData["geoLocations"][0],
                    "timeAllowed":gameData["timeAllowed"],
                    "gameType":gameData["gameType"]
                }
                return api_response(success=True,message="Successfully fetched GeoPlay",data=response)
            current_max_round = max(geoHistory,key=lambda x:x["roundTrip"])["roundTrip"]
            print(f"Max current_max_round=>{current_max_round}")
            if current_max_round < gameData["totalRound"]:

                response = {
                    "gameId":gameData["gameId"],
                    "roundTrip":1,
                    "targetLocation":gameData["geoLocations"][current_max_round],
                    "timeAllowed":gameData["timeAllowed"],
                    "gameType":gameData["gameType"]
                }
                return api_response(success=True,message="Successfully fetched GeoPlay",data=response,status=200)

        except Exception as ex:
            print(f"Error validating retrieval {ex}")
            return api_response(success=False,message="Unknown server error",status=500)


    def find_next_geo_round(self,data):
        try:
            gameData = self.geoRepository.fetch_geoplay_round(data["gameId"])

            if not gameData:
                return api_response(success=False,message="Game does not exist",status=400)
            # if gameData["gameType"] != "geoplay":
            #     return api_response(success=False,message="Invalid game type",status=400)
            # if gameData["totalRound"] < data["roundTrip"]:
            #     return api_response(success=False,message="Round trip limit exceeded",status=400)


            checkifRoundTripPlayed = self.geoRepository.confirm_game_played(data)
            print(f" Print checkifRoundTripPlayed => {len(checkifRoundTripPlayed)}")
            print(f" Print Total Round => {gameData["totalRound"] }")
            if gameData["totalRound"] == len(checkifRoundTripPlayed):
                return api_response(success=False,message="No more game to play",status=404)

            return self.validated_retrieval(data,gameData,checkifRoundTripPlayed)


        except Exception as e:
            print(f"Error fetching next geoplay round {e}")
            return api_response(success=False,message="Unknown server error",status=500)
    def fetch_attempted_locations_played_per_round(self,data):
        # fetch the max number of round for this particular player
        # use the max number to filer all geo locations of those who played that round
        # remove people who did not attempt to play and return the list, attempt is false
        output = self.geoRepository.fetch_attempted_geo_locations_per_round(data["gameId"],data["playerId"])
        return output