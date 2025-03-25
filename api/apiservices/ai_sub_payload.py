import json
from unicodedata import category

quiz_sample = {
    "single": {
        "questionType": "quiz",
        "category": "mathematics",
        "timeInterval": 30,
        "questionMessage": "What is 8 + 6?",
        "optionType": "single",
        "answers": [
            "14"
        ],
        "scorePoint": "simple",
        "options": [
            {
                "answerText": "12"
            },
            {
                "answerText": "14"
            },
            {
                "answerText": "16"
            },
            {
                "answerText": "18"
            }
        ]
    },
    "multiple": {
        "questionType": "quiz",
        "category": "mathematics",
        "timeInterval": 20,
        "questionMessage": "What are factors of 6?",
        "optionType": "mutiple",
        "answers": [
            "2",
            "3"
        ],
        "scorePoint": "simple",
        "options": [
            {
                "answerText": "2"
            },
            {
                "answerText": "5"
            },
            {
                "answerText": "3"
            },
            {
                "answerText": "35"
            }
        ]
    },
    "freetext": {
        "questionType": "quiz",
        "category": "mathematics",
        "timeInterval": 25,
        "questionMessage": "What is the name of triangle with two equal sides?",
        "optionType": "freetext",
        "answers": [
            "Isosceles triangle"
        ],
        "scorePoint": "simple",
        "options": []
    },
    "trueorfalse": {
        "questionType": "quiz",
        "category": "Fine Art",
        "timeInterval": 25,
        "questionMessage": "Red is a primary color",
        "optionType": "trueorfalse",
        "answers": [
            "True"
        ],
        "scorePoint": "simple",
        "options": [  {
            "answerText": "True"
        },
            {
                "answerText": "False"
            }]
    }
}

def generate_quiz_format(optionTypes=["single"]) ->str:

    sample_payload = [quiz_sample.get(sample) for sample in optionTypes]
    return json.dumps(sample_payload)

def ai_user_message(payload:dict)->str:

    generatedSampleFormat = generate_quiz_format(payload["optionTypes"])

    if not payload["quizDescription"]:
        payload["quizDescription"] =payload["category"]
    user_message_variable = f"Generate {payload["quizCount"]} quiz in the subject of {payload["category"]} with further  description as {payload["quizDescription"]} given the following format , {generatedSampleFormat} and assign timeInterval values according to quiz difficulty level. Also scorePoint can only be simple, medium, hard or advanced according to level of difficulty of quiz. Optiontypes should only include {payload["optionTypes"]}"
    return user_message_variable

