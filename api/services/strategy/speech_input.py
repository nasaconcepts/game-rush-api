from ..quizz_service import QuizzStrategy
from api.db.repositoryimpl.PlayerRespositoryImpl import PlayerRepositoryData
from api.modelEntity.builder.util import  calculate_point
from api.apiservices.openaiapi import ai_compare_answer

class SpeechChoice(QuizzStrategy):
    player_repo = PlayerRepositoryData()
    def process(self,data):
        question = self.player_repo.find_question(data["questionId"])
        if len(data["optionIds"]) !=1:
            data["points"] = 0
            data["validity"] ="Incorrect"
            self.player_repo.submit_question(data)
            return {"message":"InCorrect","questionId":data["questionId"]}
            # save result as failed and returned the status saying Incorrect

        ai_response = ai_compare_answer(data["optionIds"][0],question["answers"][0])
        print(f"AI Response => {ai_response}")

        if ai_response.startswith("Yes,"):
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