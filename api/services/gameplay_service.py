from ..db.repositoryimpl.PlayerRespositoryImpl import PlayerRepositoryData
from ..modelEntity.quizz_entities import SubmittedAnswer,PlayerRegistration,LeaderBoard
from ..services.contextStrategy import processQuiz
from ..modelEntity.builder.property_config import user_session_allows
from rest_framework.response import Response
from ..modelEntity.builder.Builder import build_player
from ..services.contextStrategy import processQuiz

class GamePlay:
    game_play_repo = PlayerRepositoryData()

    def create_and_join_game(self,request):
        serializer = PlayerRegistration(data =request.data)
        if not serializer.is_valid():
            return Response({"error":serializer.error},status=400)

        valid_data = serializer.validated_data
        # check if game exist => Implement Caching later
        if not self.game_play_repo.confirm_game_exists(valid_data.gameId):
            return Response({"message":f"Game ID [{valid_data.gameId}] does not exists"},status=400)

        # check if game is open or closed. Implement Caching later
        if not self.game_play_repo.confirm_game_open(valid_data.gameId):
            return Response({"message":f"Game ID [{valid_data.gameId}] has been closed"},status=400)

        # check if limit of session is exceeded
        if self.game_play_repo.max_session_limit_exceeded(valid_data):
            return Response({"message":f"Maximum number of players for this game has been exceeded"},status=403)

        # check if nickname exist --Implement caching
        if self.game_play_repo.find_registered_player_per_game(valid_data):
            return Response({"message":f"Player nickname [{valid_data.nickname}] has already been taken"},status=403)

        # create session for player
        player_data = build_player(valid_data)
        self.game_play_repo.register_player(player_data)
        return Response({"message":"User has successfully join the game","playerId":player_data.playerId,"timerEnabled":""},status=201)


    def fetch_leader_board(self,request):
        serializer = LeaderBoard(data =request.data)
        if serializer.is_valid():
            Response({"message":"Information provided is incorrect","errors":serializer.errors},status=400)
        leader_board_data = self.game_play_repo.fetch_leader_board(serializer.validated_data)
        if not leader_board_data:
            Response({"message":"No valid game Id or player provided"},status=404)
        return  leader_board_data


    def submit_question(self,request):
        serializer = SubmittedAnswer(data=request.data)
        if serializer.is_valid():
            Response({"message":"Information provided is incorrect","errors":serializer.errors},status=400)

        valid_data = serializer.validated_data
        submit_response = processQuiz(valid_data)
        return Response({"message":"Submitted Successfully","response":submit_response}, status=200)


    def fetch_next_question(self,request):
        serializer = LeaderBoard(data =request.data)
        if not serializer.is_valid():
            Response({"message":"Information provided is incorrect","errors":serializer.errors},status=400)
        valid_data = serializer.validated_data
        response_data = self.game_play_repo.fetch_next_question(valid_data)
        Response(response_data,status=200)

    def fetch_active_players(self,request):
        # request.data ={"gameId":"value"}
        if request.data.get("gameId"):
            Response({"message":"Game Id provided is incorrect"},status=400)
        response_data = self.game_play_repo.find_active_game_player(request.data.get("gameId"))
        if not response_data:
            return Response({"message":"No active players available"},status=404)
        return Response(response_data, status=200)