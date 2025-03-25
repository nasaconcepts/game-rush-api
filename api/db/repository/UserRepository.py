from abc import ABC,abstractmethod
from typing import Optional


class User(ABC):
    @abstractmethod
    def create_subscriber(self,data:dict):
        pass
    @abstractmethod
    def get_user(self,username) ->Optional[dict]:
        pass
    @abstractmethod
    def create_questions(self,data:list):
        pass
    @abstractmethod
    def create_game(self,data:dict):
        pass
    @abstractmethod
    def get_games(self,gameOwnerId:str):
        pass
    def get_games_pagination(self,data:dict):
        pass
    @abstractmethod
    def get_players_per_gameType(self,data:dict):
        pass
    def get_playground_play(self,data:dict):
        pass
    def get_playground_geo_leaderboard(self,data:dict):
        pass
    def get_playground_quiz_leaderboard(self,data:dict):
        pass
