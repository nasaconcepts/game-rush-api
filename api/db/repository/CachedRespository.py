from abc import ABC, abstractmethod
class cached_reposity(ABC):
    def get_game_cached_or_db(self,gameId):
        pass