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