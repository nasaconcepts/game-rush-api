from abc import ABC, abstractmethod

class subscribe_repository(ABC):
    @abstractmethod
    def create_or_update_invite(self,data:dict):
        pass
    @abstractmethod
    def fetch_invitation(self,data:dict):
        pass

