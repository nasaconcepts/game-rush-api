from ..db.repositoryimpl.PlayerRespositoryImpl import PlayerRepositoryData
from ..db.repositoryimpl.geo_play_repository_Impl import geoPlayRepositoryImpl
from ..modelEntity.quizz_entities import SubmittedAnswer, PlayerRegistration, LeaderBoard, NextQuestion, NextGeoPlay,SubmittedGeoPlay,GeoLeaderRequest

from api.util.utils import api_response

from rest_framework.response import Response
from ..modelEntity.builder.Builder import build_player
from ..services.contextStrategy import processQuiz
from api.services.process_geoplay import GeoGamePlay


class GamePlay:
    game_play_repo = PlayerRepositoryData()
    geoGamePlay = GeoGamePlay()
    geoRepository =geoPlayRepositoryImpl()


    def join_game_player(self,valid_data):
        try:

            # create session for player
            player_data = build_player(valid_data)

            response = self.game_play_repo.register_player(player_data)
            print(f"Player data=>{response}")
            return api_response(success=True,message="Player has successfully join the game",data=response,status=201)
        except Exception as ex:
            return api_response(success=False,errors=ex,status=500)

    def create_and_join_game(self,request):
       try:
           print(f"Request data: {request.data}")
           serializer = PlayerRegistration(data=request.data)
           if not serializer.is_valid():
               return api_response(success=False,message="Validation failure",errors=serializer.error,status=400)

           valid_data = serializer.validated_data
           print(f"Register Output: {valid_data}")

           # check if game exist => Implement Caching later
           game_output = self.game_play_repo.retrieve_game_details(valid_data["gameId"])
           print(f"Print the Output: {game_output}")

           if not game_output.get("gameId"):
               return api_response(success=False,message=f"Game ID [{valid_data["gameId"]}] does not exists",status=400)

           # check if game is open or closed. Implement Caching later
           if not game_output.get("gameOpen"):
               return api_response(success=False,message=f"Game ID [{valid_data["gameId"]}] has been closed",status=400)


           # check if nickname exist --Implement caching
           print(f"Registered user {self.game_play_repo.find_registered_player_per_game(valid_data)}")
           if self.game_play_repo.find_registered_player_per_game(valid_data):
               return api_response(False,message=f"Player nickname [{valid_data["nickname"]}] has already been taken",status=403)
           # check if limit of session is exceeded
           if self.game_play_repo.max_session_limit_exceeded(game_output.get("subscriptionPlan"),game_output.get("gameId")):
               return api_response(success=False,message=f"Maximum number of players for this game has been exceeded",status=403)

           valid_data["gameType"]= game_output.get("gameType")
           print(f"Valid data=>{valid_data}")
           return self.join_game_player(valid_data)

       except Exception as ex:
              return api_response(success=False,message="Unknown server error", errors=ex,status=500)



    def fetch_leader_board(self,request,gameId):
        if not gameId:
            return api_response(success=False,message="Information provided is incorrect",status=404)
        leader_board_data = self.game_play_repo.fetch_leader_board(gameId)
        if not leader_board_data["leaderBoard"]:

            return api_response(success=False,message="No valid game Id or player provided",status=403)
        if leader_board_data["leaderBoard"]:
            sorted_data = sorted(leader_board_data["leaderBoard"], key=lambda x: (-x["totalPoints"], x["totalTime"]))
            leader_board_data["leaderBoard"] = sorted_data
        return   api_response(success=True,data=leader_board_data,message="leader board retrieved",status=200)

    def fetch_geo_leader_board(self,request):
        serializer = GeoLeaderRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",status=404)
        valid_data = serializer.validated_data
        leader_board_data = self.geoRepository.fetch_geo_leader_board(valid_data["gameId"])
        if not leader_board_data["leaderBoard"]:

            return api_response(success=False,message="No valid game Id or player provided",status=403)
        if leader_board_data["leaderBoard"]:
            sorted_data = sorted(leader_board_data["leaderBoard"], key=lambda x: (-x["totalPoints"], x["totalTime"]))
            leader_board_data["leaderBoard"] = sorted_data
        # process the attempted guessed locations for this round
        # Retrieve Game
        game_output = self.game_play_repo.retrieve_game_details(valid_data["gameId"])


        outputGeoLocations = self.geoGamePlay.fetch_attempted_locations_played_per_round(valid_data)
        roundTrip = outputGeoLocations["currentRoundTrip"]-1 if outputGeoLocations["currentRoundTrip"]>0 else outputGeoLocations["currentRoundTrip"]
        targetLocation =  game_output["geoLocations"][roundTrip] if outputGeoLocations["currentRoundTrip"]>0 else None

        leader_board_data["pinnedGeoLocations"] =outputGeoLocations["playerLocations"]
        leader_board_data["currentRoundTrip"] = outputGeoLocations["currentRoundTrip"]
        leader_board_data["targetLocation"] =targetLocation

        return   api_response(success=True,data=leader_board_data,message="leader board retrieved",status=200)


    def submit_question(self,request):
        serializer = SubmittedAnswer(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",errors=serializer.errors,status=400)

        valid_data = serializer.validated_data
        submit_response = processQuiz(valid_data)
        return api_response(True,data=submit_response,message="Submitted Successfully", status=200)


    def fetch_next_question(self,request):
        serializer = NextQuestion(data =request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",errors=serializer.errors,status=400)
        valid_data = serializer.validated_data

        response_data = self.game_play_repo.fetch_next_unplayed_question(valid_data)
        if response_data["unplayedQuestions"]:
            response_data["unplayedQuestions"].pop("answers")
        return api_response(success=True, data=response_data,status=200)

    def fetch_active_players(self,request,gameId):

        if not gameId:
            return api_response(success=False,message="Game Id provided is incorrect",status=400)

        print(f"Valid data=>{gameId}")
        response_data = self.game_play_repo.find_active_game_player(gameId)
        if not response_data:
            return api_response(success=False,message="No active players available",status=404)

        return  api_response(success=True,data=response_data,status=200)
    def submit_geoplay(self,request):
        serializer = SubmittedGeoPlay(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",errors=serializer.errors,status=400)

        valid_data = serializer.validated_data
        return self.geoGamePlay.process_geoplay_submission(valid_data)

    def fetch_next_geoplay(self,request):
        serializer = NextGeoPlay(data =request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",errors=serializer.errors,status=400)
        valid_data = serializer.validated_data
        return self.geoGamePlay.find_next_geo_round(valid_data)
    def fetch_geoplay_session_per_round(self,request):
        serializer = GeoLeaderRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False,message="Information provided is incorrect",errors=serializer.errors,status=400)
        valid_date = serializer.validated_data
        db_response = self.geoRepository.get_stat_of_player_per_round(valid_date["gameId"],valid_date["playerId"])
        return api_response(success=True,data=db_response,status=200,message="Successful")
    def verify_game(self,request,gameId):
        if not gameId:
            return api_response(success=False,message="Information provided is incorrect",status=400)
        response_data = self.game_play_repo.retrieve_game_details(gameId)
        if not response_data:
            return api_response(success=False,message="No valid game Id provided",status=403)
        return api_response(success=True,data=response_data,status=200)
