from abc import ABC, abstractmethod

class QuizzStrategy(ABC):
    @abstractmethod
    def process(self,request):
        pass
