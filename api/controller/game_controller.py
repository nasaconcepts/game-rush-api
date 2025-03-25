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
def verify_game(request,gameId):
    return game_service.verify_game(request,gameId)
@api_view(["POST"])
def get_geo_leader_board(request):
    return game_service.fetch_geo_leader_board(request)
@api_view(["GET"])
def get_active_players_session(request,gameId):
    return game_service.fetch_active_players(request,gameId)
@api_view(["POST"])
def submit_question(request):
    return game_service.submit_question(request)
@api_view(["POST"])
def submit_geoplay(request):
    return game_service.submit_geoplay(request)
@api_view(["POST"])
def fetch_next_geoplay(request):
    return game_service.fetch_next_geoplay(request)
@api_view(["POST"])
def fetch_geoplay_session_stat(request):
    return game_service.fetch_geoplay_session_per_round(request)