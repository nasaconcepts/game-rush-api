from random import choices
from rest_framework import serializers
from ..modelEntity.builder.property_config import question_types,subscriptions,optionTypes,default_score
class Option(serializers.Serializer):
    answerText = serializers.CharField()
    optionId = serializers.CharField(required=False)
    color = serializers.CharField(required=False)

class Question(serializers.Serializer):
    questionId = serializers.CharField(required=False)
    questionType = serializers.ChoiceField(choices=question_types)
    questionMessage = serializers.CharField(required=True)
    timeInterval = serializers.IntegerField(required=True)
    optionType = serializers.ChoiceField(choices=["single", "multiple", "freetext"])
    answers = serializers.ListField(child= serializers.CharField(), allow_empty=False)
    options = Option(many=True)
    questionVideo = serializers.CharField(required=False, allow_null=True)
    questionImage = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False)
    visibility = serializers.ChoiceField(required=False,choices=["public","private"])
    creatorId = serializers.CharField(required=False)
    scorePoint = serializers.ChoiceField(choices=list(default_score.keys()))

class Questions(serializers.Serializer):
    questions = Question(many=True)

class PlayedGameHistory(serializers.Serializer):
    gameId = serializers.CharField()
    userId = serializers.CharField()
    nickname = serializers.CharField()
    quizzId = serializers.CharField()
    timeTaken = serializers.FloatField()
    score = serializers.FloatField()
    passed = serializers.BooleanField()
    dateCreated = serializers.DateTimeField()
    optionsSelected = serializers.ListField(child = serializers.CharField())

class GameSummary(serializers.Serializer):
    userId = serializers.CharField()
    nickname = serializers.CharField()
    score = serializers.FloatField()
    totalTime = serializers.FloatField()

class AIAnswerTrail(serializers.Serializer):
    userId = serializers.CharField()
    quizzId = serializers.CharField()
    AiFeedback = serializers.CharField()
    dateCreated = serializers.DateTimeField()

class Subscriber (serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
    subscriptionPlan = serializers.ChoiceField(choices=subscriptions)
class Game(serializers.Serializer):
    gameTitle = serializers.CharField()
    gameOwnerId = serializers.CharField()
    questions = Question(many=True)
    timerEnabled = serializers.BooleanField()
    source = serializers.CharField()
    gameType = serializers.ChoiceField(choices=["quiz","geoplay"])
class GeoGameRequest(serializers.Serializer):
    gameTitle = serializers.CharField()
    gameOwnerId = serializers.CharField()
    timerEnabled = serializers.BooleanField()
    gameType = serializers.ChoiceField(choices=["quiz","geoplay"])
    source = serializers.CharField()
    totalLocations = serializers.IntegerField()
    timeAllowed = serializers.IntegerField()


class LocationPoint(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class GameRegular(serializers.Serializer):
    gameTitle = serializers.CharField()
    gameOwnerId = serializers.CharField()
    questionIds = serializers.ListField(child=serializers.CharField())
    timerEnabled = serializers.BooleanField()
class SubmittedAnswer(serializers.Serializer):
    gameId = serializers.CharField()
    optionType = serializers.ChoiceField(choices=optionTypes)
    playerId = serializers.CharField()
    questionId = serializers.CharField()
    timeTaken = serializers.IntegerField()
    optionIds = serializers.ListField(child=serializers.CharField())
class SubmittedGeoPlay(serializers.Serializer):
    gameId = serializers.CharField()
    gameType = serializers.ChoiceField(choices=["geoplay"])
    playerId = serializers.CharField()
    guessedLocation = LocationPoint()
    timeTaken = serializers.IntegerField()

class PlayerRegistration(serializers.Serializer):
    gameId = serializers.CharField()
    nickname = serializers.CharField()

class LeaderBoard(serializers.Serializer):
    gameId = serializers.CharField()

class NextQuestion(serializers.Serializer):
    gameId = serializers.CharField()
    playerId = serializers.CharField()
class GeoLeaderRequest(serializers.Serializer):
    gameId = serializers.CharField()
    playerId = serializers.CharField()
class NextGeoPlay(serializers.Serializer):
    gameId = serializers.CharField()
    playerId = serializers.CharField()
    # roundTrip = serializers.IntegerField()
class AIQuizRequestModel(serializers.Serializer):
    quizCount = serializers.IntegerField()
    category = serializers.CharField()
    optionTypes =serializers.ListField(child=serializers.CharField())
    quizDescription = serializers.CharField()
class CreateGeoPlayRequest(serializers.Serializer):
    gameOwnerId = serializers.CharField()
    gameTitle = serializers.CharField(required=False)
    totalLocations = serializers.IntegerField()
    timerEnabled = serializers.BooleanField()
    timeAllowed = serializers.IntegerField()
class PreviewRequest(serializers.Serializer):
    gameType = serializers.ChoiceField(choices=["quiz","geoplay"])
    gameId = serializers.CharField()
    roundTrip = serializers.IntegerField()
class SubscriberGamesRequest(serializers.Serializer):
    gameOwnerId = serializers.CharField()
    page = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)
class InvitePlayerRequest(serializers.Serializer):
    gameOwnerId= serializers.CharField()
    gameId = serializers.CharField()
    emails = serializers.ListField(child=serializers.CharField())
class FetchGameDetailsRequest(serializers.Serializer):
    gameOwnerId= serializers.CharField()
    gameId = serializers.CharField()







