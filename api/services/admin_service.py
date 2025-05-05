from ..modelEntity.quizz_entities import Subscriber, Questions, Game, GameRegular, AIQuizRequestModel, GeoGameRequest, \
    PreviewRequest, SubscriberGamesRequest, FetchGameDetailsRequest, InvitePlayerRequest
from ..modelEntity.builder.Builder import build_subscriber, build_question, build_game, build_ai_question,\
create_geoplay_game, build_invitation_details, build_subscriber_game_details
from ..db.repositoryimpl.UserRepositoryImpl import UserRepositoryImpl
from api.db.repositoryimpl.user_athenticate_repo_impl import authenticate_repository
from api.db.repositoryimpl.subscribe_repository_impl import subscribe_repository_impl
from api.apiservices.openaiapi import ai_generate_questions
import json
from rest_framework.response import Response
from rest_framework import status
from ..util.utils import api_response
from api.notifications.email_notification import email_notifier
from api.db.repositoryimpl.cached_repository_impl import cached_repository_impl
import uuid


class admin_service:
    userRepo = UserRepositoryImpl()
    email_notifier_service = email_notifier()
    subscriber_repo = subscribe_repository_impl()
    cache_service = cached_repository_impl()
    authenticate_repo = authenticate_repository()

    def create_subscriber(self, request):
        serializer = Subscriber(data=request.data, many=isinstance(request.data, list))

        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data",errors=serializer.errors, status=400)
       
        response_data = build_subscriber(request.data)
#        # Check if the User already exists
        if self.authenticate_repo.find_user_by_id(response_data["subscriberId"]):
            
            db_data = self.userRepo.create_subscriber(response_data)
            print(f"Data from DB => {db_data}")
            self.authenticate_repo.update_user_profile_status(response_data["subscriberId"])
    

            return api_response(success=True, message="Subscriber created successfully", data=db_data, status=201)
        return api_response(success=False, message="User is yet to be signed on", status=400)

    def create_questions(self, request):
        questions = request.data

        serializer = Questions(data=request.data, many=isinstance(request.data, list))
        if not serializer.is_valid():
            return Response({"message": "validation failed", "error": serializer.errors})
        else:
            valid_data = serializer.validated_data
            validated_questions = [build_question(question) for question in valid_data["questions"]]

            self.userRepo.create_questions(validated_questions)

        return Response({"message", "Successfully created questions"}, status=201)

    def create_question_and_game(self, request):
        # create records in the question database
        # generate game ID extract the question ids and form game payload.
        # send email to the subscriber with game detail
        serializer = Game(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="validation failed", errors=serializer.errors, status=400)
        else:
            valid_data = serializer.validated_data
            validated_questions = [build_question(question, valid_data) for question in valid_data["questions"]]

            self.userRepo.create_questions(validated_questions)

            question_ids = [question["questionId"] for question in validated_questions]
            valid_data["questionIds"] = question_ids

            gameData = build_game(valid_data)
            self.userRepo.create_game(gameData)
            #     send email
            response = {"gameId": gameData["gameId"], "gameOwnerId": gameData["gameOwnerId"]}
            return api_response(success=True, message="Game has been created successfully", data=response, status=201)

    def create_regular_game(self, request):
        # create records in the question database
        # generate game ID extract the question ids and form game payload.
        # send email to the subscriber with game detail
        print(f"Output => {request.data}")
        serializer = GameRegular(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "validation failed", "error": serializer.errors})
        else:
            valid_data = serializer.validated_data

            gameData = build_game(valid_data)
            self.userRepo.create_game(gameData)
        #     send email
        return Response({"message": "Game has been created successfully"}, status=201)

    def generate_ai_quiz(self, request):
        serializer = AIQuizRequestModel(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="validation failed", errors=serializer.errors, status=400)
        ai_response = ai_generate_questions(serializer.validated_data)
        if not ai_response:
            return api_response(success=False, message="No quiz found", status=404)
        print(f"{ai_response}")
        raw_data = ai_response.strip("```json\n```")
        parsed_data = json.loads(raw_data)
        rebuilt_question = build_ai_question(parsed_data)

        return api_response(success=True, message="Quiz generated successfully", data=rebuilt_question, status=200)

    def create_geoplay_game(self, request):
        serializer = GeoGameRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)
        valid_data = serializer.validated_data
        gameData = create_geoplay_game(valid_data)
        self.userRepo.create_game(gameData)
        response = {"gameId": gameData["gameId"], "gameOwnerId": gameData["gameOwnerId"]}
        return api_response(success=True, message="Game has been created successfully", data=response, status=201)

    def fetch_my_games(self, request, gameOwnerrId):
        if not gameOwnerrId:
            return api_response(success=False, message="Invalid data provided", status=400)
        games = self.userRepo.fetch_my_games(gameOwnerrId)
        pass

    def getNextPreviewPlayground(self, request):
        gameType = request.data.get("gameType")
        if not gameType:
            return api_response(success=False, message="Invalid data provided", status=400)
        serializer = PreviewRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)

        valid_data = serializer.validated_data

        response = self.userRepo.get_playground_play(valid_data)
        if response.get("error"):
            return api_response(success=False, message=response.get("error"), status=400)
        print(f"Data from DB Preview => {response}")
        return api_response(success=True, message="Preview Playground successful", data=response, status=200)

    def getNextPreviewLeaderboard(self, request):
        try:
            serializer = PreviewRequest(data=request.data)
            if not serializer.is_valid():
                return api_response(success=False, message="Invalid data provided", status=400)

            valid_data = serializer.validated_data
            gameId = valid_data.get("gameId")
            gameType = valid_data.get("gameType")

            if not gameId:
                return api_response(success=False, message="Invalid data provided", status=400)

            if gameType == "geoplay":
                response_geo = self.userRepo.get_playground_geo_leaderboard(valid_data)
                if response_geo.get("error"):
                    return api_response(success=False, message=response_geo.get("error"), status=400)
                return api_response(success=True, message="Preview Leaderboard successful", data=response_geo,
                                    status=200)
            if gameType == "quiz":
                response_quiz = self.userRepo.get_playground_quiz_leaderboard(valid_data)
                if response_quiz.get("error"):
                    return api_response(success=False, message=response_quiz.get("error"), status=400)
                return api_response(success=True, message="Preview Leaderboard successful", data=response_quiz,
                                    status=200)
        except Exception as ex:
            print(f"Error => {ex}")
            return api_response(success=False, message="An error occurred", errors=ex, status=500)

    def fetch_subscriber_games(self, request):
        # implement error validation
        serializer = SubscriberGamesRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)
        valid_data = serializer.validated_data

        games = self.userRepo.get_games_pagination(valid_data)
    
        if not games or len(games.get("games")) == 0:
            return api_response(success=False, message="No games found", status=404)
        return api_response(success=True, message="Games retrieved successfully", data=games, status=200)

    def do_invite_players(self, request):
        serializer = InvitePlayerRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)
        valid_data = serializer.validated_data
        #     Check if game exist
        game = self.cache_service.get_game_cached_or_db(valid_data["gameId"])
        if not game:
            return api_response(success=False, message="Game does not exist", status=404)

        #     Asynchronous send emails to invitees, inject another email service
        #     set game Url
        valid_data["gameUrl"] = game["qrData"]["gameUrl"]
        successful_emails = self.email_notifier_service.send_email_notifications(valid_data)
        valid_data["emails"] = successful_emails
        update_response = self.subscriber_repo.create_or_update_invite(valid_data)
        if update_response.get("error"):
            return api_response(success=False, message=update_response.get("error"), status=403)

        return api_response(success=True, data=update_response, message="Invitation was successful", status=200)

    # yet to implement
    def load_game_details(self, request):
        serializer = FetchGameDetailsRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)
        valid_data = serializer.validated_data
        game = self.cache_service.get_game_cached_or_db(valid_data["gameId"])
        response = build_subscriber_game_details(game)
        return api_response(success=True,data=response,message="Successful",status=200)

    def load_game_invite_details(self, request):
        serializer = FetchGameDetailsRequest(data=request.data)
        if not serializer.is_valid():
            return api_response(success=False, message="Invalid data provided", status=400)
        valid_data = serializer.validated_data
        game = self.cache_service.get_game_cached_or_db(valid_data["gameId"])
        response = build_invitation_details(game)
        invitation_response = self.subscriber_repo.fetch_invitation(valid_data)
        if invitation_response:
            response["emails"]=invitation_response["emails"]
            return response
        return response

    def fetch_game_details(self, gameId):
        if not gameId:
            return api_response(success=False, message="Invalid data provided", status=400)
        game = self.cache_service.get_game_cached_or_db(gameId)
        if not game:
            return api_response(success=False, message="Game does not exist", status=404)
        
        return api_response(success=True, data=game, message="Game retrieved successfully", status=200)
    def fetch_business_categories(self, request):
        categories = self.subscriber_repo.fetch_business_categories()
        if not categories:
            return api_response(success=False, data=categories,message="No categories found", status=404)
        return api_response(success=True, data=categories, message="Categories retrieved successfully", status=200)
    def create_business_category(self, request):
        
        data = request.data
        categories = data.get("categoryNames")
        if data.get("categoryNames"):
            if not isinstance(categories, list) or not all(isinstance(category, str) for category in categories):
                return api_response(success=False, message="Invalid data provided", status=400)

            categories_data = [{"categoryId":str(uuid.uuid4()), "categoryName": category.strip()} for category in categories if category.strip()]
            if not categories_data:
                return api_response(success=False, message="No valid categories provided", status=400)

            created_categories = self.subscriber_repo.create_business_category(categories_data)
            
            if not created_categories:
                return api_response(success=False, message="Failed to create categories", status=500)

            return api_response(success=True, data=created_categories, message="Categories created successfully", status=201)