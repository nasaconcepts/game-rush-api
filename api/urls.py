from django.urls import path
from api import views
from api.controller import admin_controller,game_controller

urlpatterns = [
    path('',views.getData),
    path('/api',views.save_quiz),
    path('save-quiz/', views.save_quiz, name='save-quiz'),
    path('create-subscriber/',admin_controller.create_subscriber,name='create_admin'),
    path('create-questions/',admin_controller.create_questions,name='create-questions'),
    path('create-prepared-game/',admin_controller.generate_regular_game,name='create-prepared-game'),
    path('create-custom-game/',admin_controller.generate_custom_game,name='create-custom-game'),
    path('register-player/',game_controller.register_player,name='register_player'),
    path('next-question/',game_controller.get_next_question,name='get_next_question'),
    path('get-leader-board/',game_controller.get_leader_board,name='get_leader_board'),
    path('active-players/',game_controller.get_active_players_session,name='get_active_players_session'),
]