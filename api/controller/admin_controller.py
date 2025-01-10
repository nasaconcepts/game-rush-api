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
    return admin.create_custom_game(request)
@api_view(["POST"])
def generate_regular_game(request):
    return admin.create_regular_game(request)