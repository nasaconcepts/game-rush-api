from ..modelEntity.quizz_entities import Subscriber,Questions,Game,GameRegular
from ..modelEntity.builder.Builder import build_subscriber, build_question,build_game
from ..db.repositoryimpl.UserRepositoryImpl import UserRepositoryImpl

from rest_framework.response import Response
from rest_framework import status

class admin_service:
    userRepo = UserRepositoryImpl()
    def create_subscriber(self,request):
        serializer = Subscriber(data=request.data, many=isinstance(request.data,list))

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        response_data = build_subscriber(request.data)

        db_data = self.userRepo.create_subscriber(response_data)

        return Response(
            {"message": "Admin user(s) created successfully", "subscriberId":response_data.get("subscriber_id")},
            status=status.HTTP_201_CREATED
        )

    def create_questions(self,request):
        questions = request.data
        print(f"questions =>{questions}")
        serializer = Questions(data=request.data, many=isinstance(request.data,list))
        if not serializer.is_valid():
            return Response({"message":"validation failed","error":serializer.errors})
        else:
            valid_data = serializer.validated_data
            validated_questions = [build_question(question) for question in valid_data["questions"]]
            print(f"Response {validated_questions}")
            self.userRepo.create_questions(validated_questions)

        return Response({"message","Successfully created questions"},status=201)
    def create_custom_game(self,request):
        # create records in the question database
        # generate game ID extract the question ids and form game payload.
        # send email to the subscriber with game detail
        serializer = Game(data=request.data)
        if not serializer.is_valid():
            return Response({"message":"validation failed","error":serializer.errors})
        else:
            valid_data = serializer.validated_data
            validated_questions = [build_question(question) for question in valid_data["questions"]]
            print(f"Response {validated_questions}")
            self.userRepo.create_questions(validated_questions)

            question_ids = [question["questionId"] for question in validated_questions]
            valid_data["questionIds"] = question_ids

            gameData = build_game(valid_data)
            self.userRepo.create_game(gameData)
        #     send email
        return Response({"message":"Game has been created successfully"},status=201)
    def create_regular_game(self,request):
        # create records in the question database
        # generate game ID extract the question ids and form game payload.
        # send email to the subscriber with game detail
        print(f"Output => {request.data}")
        serializer = GameRegular(data=request.data)
        if not serializer.is_valid():
            return Response({"message":"validation failed","error":serializer.errors})
        else:
            valid_data = serializer.validated_data

            gameData = build_game(valid_data)
            self.userRepo.create_game(gameData)
        #     send email
        return Response({"message":"Game has been created successfully"},status=201)