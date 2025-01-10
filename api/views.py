
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.modelEntity.quizz_entities import Option,Questions
from .db.save_to_db import save_option



# Create your views here.
@api_view(['GET'])
def getData(request):
    options = [
        {"optionId": "123", "answerText": "My name is Chinasa"},
        {"optionId": "124", "answerText": "My name is Nasa"},
    ]

    # Create quiz data
    quiz_data = {
        "quizId": "1200",
        "quizMessage": "What is your name?",
        "optionType": "single",
        "options": options,
        # "quizVideo": "https://example.com/video",  # Optional field
        "quizImage": "https://example.com/image"
    }

    # Use the Quizz serializer to serialize data
    quizz_serializer = Quizz(data=quiz_data)
    if quizz_serializer.is_valid():
        return Response(quizz_serializer.data)
    else:
        return Response(quizz_serializer.errors, status=400)


@api_view(["POST"])
def save_quiz(request):

    try:
        # Parse incoming data
        data = request.data

        # Extract quiz and options data
        quiz = {
            "quizId": data["quizId"],
            "quizMessage": data["quizMessage"],
            "optionType": data["optionType"],
            "quizImage": data.get("quizImage"),
            "quizVideo": data.get("quizVideo"),
        }
        options = data.get("options", [])

        # Save to MongoDB
        save_option(quiz, options)

        return Response({"message": "Quiz saved successfully!"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)