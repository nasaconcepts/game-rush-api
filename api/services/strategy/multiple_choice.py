from ..quizz_service import QuizzStrategy
from api.db.repositoryimpl.PlayerRespositoryImpl import PlayerRepositoryData
from api.modelEntity.builder.util import  calculate_point

class MultipleChoice(QuizzStrategy):
    player_repo = PlayerRepositoryData()
    def process(self,data):
        question = self.player_repo.find_question(data.questionId)
        if len(data["optionIds"]) != question["answerCount"]:
            data["points"] = 0
            data["validity"] ="Incorrect"
            self.player_repo.submit_question(data)
            return {"message":"InCorrect","questionId":data["questionId"]}
            # save result as failed and returned the status saying Incorrect

        answers = [answer["answerText"] for answer in question["optionIds"]]
        is_answer_correct = sorted(answers) == sorted(data["optionIds"])
        if is_answer_correct:
            score_value = calculate_point(question["scorePoint"], question["timeInterval"],data["timeTaken"])
            data["points"] = score_value
            data["validity"] ="Correct"
            self.player_repo.submit_question(data)
            return {"message":"Correct","questionId":data["questionId"]}
        else:
            data["points"] = 0
            data["validity"] ="Incorrect"
            self.player_repo.submit_question(data)
            return {"message":"InCorrect","questionId":data["questionId"]}