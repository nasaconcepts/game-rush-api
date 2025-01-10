import uuid
from datetime import datetime
from ..builder.property_config import default_score,option_colors
from ..builder.util import generate_unique_id

def build_question(data:dict):
    data["questionId"]=str(uuid.uuid4())
    data["created_at"] = datetime.now().isoformat()
    data["answerCount:"] = len(data["answers"])
    # The color is selected using option_colors[i % len(option_colors)] to ensure it cycles through the option_colors list.
    if data["options"]:
        data["options"] = [{"optionId":str(uuid.uuid4()), "answerText":option["answerText"],"color":option_colors[color_index % len(option_colors)] } for color_index, option in enumerate(data["options"]) ]

    return data
def build_subscriber(data:dict):
    data["subscriber_id"] =str(uuid.uuid4())
    data["created_at"] = datetime.now().isoformat()
    data["active"] = True
    return data

def build_player(data:dict):
    data["playerId"] = str(uuid.uuid4())
    data["created_on"] = datetime.now().isoformat()
    return data

def build_game(data:dict):
    data["game_id"] = generate_unique_id(10)
    data["created_on"] =datetime.now().isoformat()
    data["game_open"] = True
    # Remove the questions objects since it has been inserted into the database. and replace by questionIds
    if data.get("questions"):
        data.pop("questions",None)
    return data
def build_play(data:dict):
    data["played_on"] = datetime.now().isoformat()
    return data

