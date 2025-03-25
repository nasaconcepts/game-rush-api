from abc import ABC, abstractmethod
from typing import Optional,List

class GeoPlay(ABC):
    @abstractmethod
    def register_geo_player(self,data:dict) -> dict:
        pass
    @abstractmethod
    def fetch_geo_leader_board(self, game_id: str):
        pass
    @abstractmethod
    def submit_geoplay(self,data:dict) ->dict:
        pass
    @abstractmethod
    def fetch_geoplay_round(self,gameId:str) ->Optional[dict]:
        pass


