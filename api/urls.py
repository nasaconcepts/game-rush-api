from django.urls import path
from api import views
from api.controller import admin_controller,game_controller,authenticate_controller
from graphene_django.views import GraphQLView
from api.graphql.schema import schema






# Explicit WebSocket handler


urlpatterns = [
    path('create-subscriber',admin_controller.create_subscriber,name='create_admin'),
    path('create-questions',admin_controller.create_questions,name='create-questions'),
    path('create-prepared-game',admin_controller.generate_regular_game,name='create-prepared-game'),
    path('create-quiz-game',admin_controller.generate_custom_game,name='create-custom-game'),
    path('verify-game/<str:gameId>',game_controller.verify_game,name='verify_game'),
    path('register-player',game_controller.register_player,name='register_player'),
    path('next-question',game_controller.get_next_question,name='get_next_question'),
    path('get-leader-board/<str:gameId>',game_controller.get_leader_board,name='get_leader_board'),
    path('get-geo-leader-board',game_controller.get_geo_leader_board,name='get_geo_leader_board'),
    path('active-players/<str:gameId>',game_controller.get_active_players_session,name='get_active_players_session'),
    path('submit-question',game_controller.submit_question,name='submit_question'),
    path('ai-generate-quiz',admin_controller.generate_quiz_with_ai,name='ai_quiz'),
    path('fetch-my-games/<str:gameOwnerId>',admin_controller.fetch_my_games,name='fetch-my-games'),
    path('create-geoplay-games',admin_controller.create_geoplay_game,name='create-geoplay-games'),
    path('submit-geoplay',game_controller.submit_geoplay,name='submit-geoplay-games'),
    path('fetch-next-geoplay',game_controller.fetch_next_geoplay,name='fetch-next-geoplay'),
    path('fetch-geoplay-session-stat',game_controller.fetch_geoplay_session_stat,name='fetch-geoplay-session-sta'),

    path('fetch-next-preview-playground',admin_controller.fetch_next_preview_playground,name='fetch-next-preview-playground'),
    path('fetch-preview-leaderboard',admin_controller.fetch_preview_leaderboard,name='fetch-preview-leaderboard'),
    path('fetch-preview-players',admin_controller.fetch_preview_players,name='fetch-preview-players'),


    path('fetch-subscriber-game-list',admin_controller.fetch_subscriber_games,name='fetch-subscriber-game-list'),
    path('invite-player',admin_controller.initiate_players_invite,name='invite-players'),

#     Authentication Services
    path('login', authenticate_controller.login_user),
    path('register', authenticate_controller.register_user),
    path('google-login', authenticate_controller.google_login),
    path('token/refresh', authenticate_controller.generate_access_token, name='token_refresh'),
    path('verify-email/<str:token>', authenticate_controller.verify_email),
    
       path("graphql/", GraphQLView.as_view(
        schema=schema,
        graphiql=True,
        subscription_path="/graphql/"
    )),



]