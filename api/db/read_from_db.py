from re import match
from tokenize import group

from db_config import db

def fetchQuiz(queryQuiz):
    pass
def getPlayer(playerRequest):
    pass
def getOverallQuizzSummary(game_session):
    dbOutput = db.playedGameHistory.aggregate([
        # Match records for the specified gameId
        {
            "$match": {
                "gameId": game_session.gameId
            }
        },
        # Group by userId and calculate totalScore and totalTimeTaken
        {
            "$group": {
                "_id": "$userId",  # Group by userId
                "totalScore": {"$sum": "$score"},  # Sum scores for each user
                "totalTimeTaken": {"$sum": "$timeTaken"},  # Sum time taken for each user
                "nickname": {"$first": "$nickname"}  # Keep the first nickname
            }
        },
        # Sort by totalScore (descending) and totalTimeTaken (ascending)
        {
            "$sort": {
                "totalScore": -1,  # Sort by totalScore in descending order
                "totalTimeTaken": 1  # Sort by totalTimeTaken in ascending order
            }
        }
    ])

    return list(dbOutput)  # Convert the cursor to a list for easier handling