from api.db.repository.SubscribeRepository import subscribe_repository
from api.db.db_config import db

class subscribe_repository_impl(subscribe_repository):
    db_invite = db["invitePlayers"]
    business_categories = db["businessCategories"]
    def create_or_update_invite(self,data):
        try:
            inviteFilter = {"gameId":data["gameId"]}
            invitation = self.db_invite.find_one(inviteFilter,{"_id":0})
            if not invitation:
                return self.db_invite.insert_one(data)


            update_query = {"$addToSet": {"emails": {"$each": data["emails"]}}}
            self.db_invite.update_one(inviteFilter, update_query)
            invitation = self.db_invite.find_one(inviteFilter,{"_id":0})
            return invitation
        except Exception as ex:
            print(f"Error creating invite")
            return {"error":"Error saving invite"}
    def fetch_invitation(self,data):
        try:
            inviteFilter = {"gameId":data["gameId"]}
            invitation = self.db_invite.find_one(inviteFilter,{"_id":0})
            return invitation
        except Exception as ex:
            print(f"Error occurred while fetching invitations details {ex}")
    def fetch_business_categories(self):
        try:
            categories = self.business_categories.find({},{"_id":0})
            return list(categories)
        except Exception as ex:
            print(f"Error occurred while fetching business categories {ex}")
            return None
    def create_business_category(self,data):
        try:
            
            if isinstance(data, list):
                self.business_categories.insert_many(data)
                return  [{key: value for key, value in doc.items() if key != "_id"} for doc in data]
        except Exception as ex:
            print(f"Error occurred while creating business category {ex}")
            return None