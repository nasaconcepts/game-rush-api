from typing import Optional, List

from ..repository.PlayerRepository import Player
from ..db_config import db

class PlayerRepositoryData(Player):
    player_register = db["playerRegisteredSession"]
    game_register = db["gameRegister"]
    games_collection = db["games"]
    def register_player(self,data:dict) -> dict:
        try:
            response = self.player_register.insert_one(data)
            # fetch game details

            print(f"Player registered successfully {response}")
            return response
        except Exception as e:
            print(f"Error registering the player {e}")
    def fetch_leader_board(self, data: dict) -> dict:
        try:
            response = self.game_register.insert_one(data)
            print(f"Game registered successfully {response}")
            return response
        except Exception as e:
            print(f"Error in registering game {e}")
    def submit_question(self,data:dict) ->dict:
        pass
    def fetch_next_question(self,player_id:str) ->Optional[List[dict]]:
        pass
    def close_game(self,game_id:str,initiator:str) -> None:
        pass
    def check_all_player_submitted(self,game_id) ->dict:
        pass
    def confirm_game_open(self,game_id)->dict:
        pass
    def find_active_game_player(self,game_id:str) ->List[dict]:
        pass
    def confirm_game_exists(self,game_id) -> bool:
        pass
    def find_registered_player_per_game(self,data:dict) ->Optional[dict]:
        pass
    def max_session_limit_exceeded(self,data) ->bool:
        pass
    def find_question(self,question_id:str) ->Optional[dict]:
        pass