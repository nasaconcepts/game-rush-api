from rest_framework.decorators import api_view
from ..services.gameplay_service import GamePlay

game_service = GamePlay()
@api_view(["POST"])
def register_player(request):
    return game_service.create_and_join_game(request)
@api_view(["POST"])
def get_next_question(request):
    return game_service.fetch_next_question(request)
@api_view(["GET"])
def get_leader_board(request,gameId):
    return game_service.fetch_leader_board(request,gameId)
@api_view(["GET"])
def get_active_players_session(request,gameId):
    return game_service.fetch_active_players(request,gameId)
@api_view(["POST"])
def submit_question(request):
    return game_service.submit_question(request)