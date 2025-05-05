from rest_framework.decorators import api_view
from ..services.admin_service import admin_service

admin = admin_service()
@api_view(["POST"])
def create_subscriber(request):

    return admin.create_subscriber(request)
@api_view(["POST"])
def create_questions(request):
    return admin.create_questions(request)
@api_view(["POST"])
def generate_custom_game(request):
    return admin.create_question_and_game(request)
@api_view(["POST"])
def generate_regular_game(request):
    return admin.create_regular_game(request)
@api_view(["POST"])
def generate_quiz_with_ai(request):
    return admin.generate_ai_quiz(request)
@api_view(["GET"])
def fetch_my_games(request,gameOwnerId):
    return admin.fetch_my_games(request,gameOwnerId)
@api_view(["POST"])
def create_geoplay_game(request):
    return admin.create_geoplay_game(request)
@api_view(["POST"])
def fetch_next_preview_playground(request):
    return admin.getNextPreviewPlayground(request)
@api_view(["POST"])
def fetch_preview_leaderboard(request):
    return admin.getNextPreviewLeaderboard(request)
@api_view(["POST"])
def fetch_preview_players(request):
    return admin.fetchPreviewPlayers(request)
@api_view(["POST"])
def fetch_subscriber_games(request):
    return admin.fetch_subscriber_games(request)
@api_view(["POST"])
def initiate_players_invite(request):
    return admin.do_invite_players(request)
@api_view(["GET"])
def fetch_game_details(request,gameId):
    return admin.fetch_game_details(gameId)
@api_view(["GET"])
def fetch_business_categories(request):
    return admin.fetch_business_categories(request)
@api_view(["POST"])
def create_business_category(request):
    return admin.create_business_category(request)