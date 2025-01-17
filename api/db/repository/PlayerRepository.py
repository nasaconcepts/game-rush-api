from abc import ABC, abstractmethod
from typing import Optional,List


class Player(ABC):

    @abstractmethod
    def register_player(self,data:dict) -> dict:
        pass
    @abstractmethod
    def fetch_leader_board(self, game_id: str):
        pass
    @abstractmethod
    def close_game(self,game_id:str,initiator:str) -> None:
        pass
    @abstractmethod
    def submit_question(self,data:dict) ->dict:
        pass
    @abstractmethod
    def fetch_next_unplayed_question(self,player_id:str) ->Optional[List[dict]]:
        pass
    @abstractmethod
    def check_all_player_submitted(self,game_id) ->dict:
        pass
    @abstractmethod
    def confirm_game_open(self,game_id) ->dict:
        pass
    @abstractmethod
    def find_active_game_player(self,game_id:str) ->List[dict]:
        pass
    @abstractmethod
    def retrieve_game_details(self,game_id) -> dict:
        pass
    @abstractmethod
    def find_registered_player_per_game(self,data:dict) ->Optional[dict]:
        pass
    def max_session_limit_exceeded(self,subscriptionPlan:str,gameId:str)->bool:
        pass
    def find_question(self,questionId:str) ->Optional[dict]:
        pass