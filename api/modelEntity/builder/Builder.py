import uuid
import random
from datetime import datetime
from ..builder.property_config import default_score,option_colors
from ..builder.util import generate_unique_id
from api.services.location_service import generate_random_valid_location
from api.qrcode.qrcode_client import generate_qr_code

def build_question(data:dict,all_quiz_data:dict):
    if not data.get("questionId"):
        data["questionId"]=str(uuid.uuid4())
    data["created_at"] = datetime.now().isoformat()
    data["answerCount"] = len(data["answers"])
    if all_quiz_data["source"] =="AI":
        data["visibility"] = "public"
    if all_quiz_data["source"] == "MANUAL":
        data["visibility"] = "private"
    if all_quiz_data["gameOwnerId"]:
        data["gameOwnerId"] = all_quiz_data["gameOwnerId"]

        


    # The color is selected using option_colors[i % len(option_colors)] to ensure it cycles through the option_colors list.
    if data["options"]:
        # Shuffle the colors
        random.shuffle(option_colors)
        data["options"] = [{"optionId":str(uuid.uuid4()), "answerText":option["answerText"],"color":option_colors[color_index % len(option_colors)] } for color_index, option in enumerate(data["options"]) ]

    return data
def build_subscriber(data:dict):
    data["subscriberId"] =str(uuid.uuid4())
    data["createdAt"] = datetime.now().isoformat()
    data["active"] = True
    return data

def build_player(data:dict):

    data["playerId"] = str(uuid.uuid4())
    data["created_on"] = datetime.now().isoformat()
    return data

def build_game(data:dict):
    data["gameId"] = generate_unique_id(10)
    data["createdOn"] =datetime.now().isoformat()
    data["gameOpen"] = True
    data["totalQuestion"] =len(data["questions"])
    data["qrData"] = generate_qr_code(data["gameId"])

    # Remove the questions objects since it has been inserted into the database. and replace by questionIds
    if data.get("questions"):
        data.pop("questions",None)
    return data
def build_play(data:dict):
    data["played_on"] = datetime.now().isoformat()
    return data
def build_ai_question(questions:list)->list:
    for question in questions:
        question["questionId"] = str(uuid.uuid4())
    return questions
def create_geoplay_game(data:dict):
    data["gameId"] = generate_unique_id(10)
    data["createdOn"] =datetime.now().isoformat()
    data["gameOpen"] = True
    data["geoLocations"] = generate_random_valid_location(data["totalLocations"])
    data["totalRound"] =len(data["geoLocations"])
    data["qrData"] = generate_qr_code(data["gameId"])
    return data
def subscriber_game_list(data:dict):
    total_round =0
    if data["gameType"] == "geoplay":
        total_round = data["totalRound"]
    elif data["gameType"] == "quiz":
        total_round = data["totalQuestion"]
    output = {
        "gameId":data["gameId"],
        "gameOwnerId":data["gameOwnerId"],
        "gameTitle":data["gameTitle"],
        "gameType":data["gameType"],
        "gameOpen":data["gameOpen"],
        "createdOn":data["createdOn"],
        "totalRound": total_round
    }
    return output
def build_subscriber_game_details(data:dict):
    total_round =0
    if data["gameType"] == "geoplay":
            total_round = data["totalRound"]
    elif data["gameType"] == "quiz":
            total_round = data["totalQuestion"]
    output={
        "gameId":data["gameId"],
        "gameOwnerId":data["gameOwnerId"],
        "gameTitle":data["gameTitle"],
        "gameType":data["gameType"],
        "gameOpen":data["gameOpen"],
        "createdOn":data["createdOn"],
        "totalRound": total_round
    }
    return output

def build_invitation_details(data:dict):
    total_round =0
    if data["gameType"] == "geoplay":
        total_round = data["totalRound"]
    elif data["gameType"] == "quiz":
        total_round = data["totalQuestion"]
    output={
        "gameId":data["gameId"],
        "gameOwnerId":data["gameOwnerId"],
        "gameTitle":data["gameTitle"],
        "gameType":data["gameType"],
        "gameOpen":data["gameOpen"],
        "createdOn":data["createdOn"],
        "totalRound": total_round,
        "qrData":data["qrData"]
    }
    return output