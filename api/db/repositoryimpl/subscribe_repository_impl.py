from api.db.repository.SubscribeRepository import subscribe_repository
from api.db.db_config import db

class subscribe_repository_impl(subscribe_repository):
    db_invite = db["invitePlayers"]
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