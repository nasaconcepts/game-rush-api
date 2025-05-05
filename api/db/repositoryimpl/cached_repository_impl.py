from api.db.repository.CachedRespository import cached_reposity
from api.db.read_from_db import db
from api.cache.Redis_Client import get_from_redis,store_in_redis
class cached_repository_impl(cached_reposity):
    db_game_register = db["gameRegister"]
    def get_game_cached_or_db(self,gameId):
        try:
            cached_game = get_from_redis(gameId)
            print(f"Cached game {cached_game}")
            if not cached_game:
                fetched_game = self.db_game_register.find_one({"gameId":gameId},{"_id":0})
                print(f"Fetched game {fetched_game}")
                if fetched_game:
                    store_in_redis(gameId,fetched_game,1200)
                    return fetched_game
                else:
                    return {"error":"No game Id found"}

            return cached_game
        except Exception as ex:
            print(f"Error retrieving game (get_game_cached_or_db) {ex}")
            return {"error":"Error occurred while retrieving game"}

