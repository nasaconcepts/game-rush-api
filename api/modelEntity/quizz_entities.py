from random import choices
from rest_framework import serializers
from ..modelEntity.builder.property_config import question_types,subscriptions,optionTypes
class Option(serializers.Serializer):
    answerText = serializers.CharField()
    optionId = serializers.CharField(required=False)
    color = serializers.CharField(required=False)

class Question(serializers.Serializer):
    questionId = serializers.CharField(required=False)
    questionType = serializers.ChoiceField(choices=question_types)
    questionMessage = serializers.CharField(required=True)
    timeInterval = serializers.FloatField(required=True)
    optionType = serializers.ChoiceField(choices=["single", "multiple", "freetextInput"])
    answers = serializers.ListField(child= serializers.CharField(), allow_empty=False)
    options = Option(many=True)
    questionVideo = serializers.CharField(required=False, allow_null=True)
    questionImage = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False)
    visibility = serializers.ChoiceField(choices=["public","private"])
    creatorId = serializers.CharField()
    scorePoint = serializers.ChoiceField(choices=["simple","medium","advanced"])
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

class GameRegular(serializers.Serializer):
    gameTitle = serializers.CharField()
    gameOwnerId = serializers.CharField()
    questionIds = serializers.ListField(child=serializers.CharField())
class SubmittedAnswer(serializers.Serializer):
    gameId = serializers.CharField()
    optionType = serializers.ChoiceField(choices=optionTypes)
    playerId = serializers.CharField()
    questionId = serializers.CharField()
    timeTaken = serializers.FloatField()
    optionIds = serializers.CharField()

class PlayerRegistration(serializers.Serializer):
    gameId = serializers.CharField()
    nickname = serializers.CharField()
class LeaderBoard(serializers.Serializer):
    gameId = serializers.CharField()
    playerId = serializers.CharField()

