from .strategy import *

STRATEGY_REGISTRY ={
    "single":SingleChoice(),
    "multiple":MultipleChoice(),
    "freeText":SpeechChoice(),
}

def processQuiz(self,request):
    strategy = STRATEGY_REGISTRY.get(request.optionType)

    if not strategy:
        raise ValueError(f"No strategy configured {request.optionType}")
    return strategy.process(request)