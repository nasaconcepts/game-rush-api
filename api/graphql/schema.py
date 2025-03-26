import graphene
from graphene import ObjectType, String, ID, Field, List
# from graphene_django import DjangoObjectType
# from graphql_jwt.decorators import login_required
# from channels_graphql_ws import Subscription

# In-memory storage for players
players = [
    {"playerId": "1", "name": "Player One"},
    {"playerId": "2", "name": "Player Two"},
]

# Player Type
class PlayerType(ObjectType):
    playerId = ID(required=True)
    name = String(required=True)

# Query
class Query(ObjectType):
    players = List(PlayerType)
    player = Field(PlayerType, playerId=ID(required=True))

    def resolve_players(root, info):
        return players

    def resolve_player(root, info, playerId):
        return next((p for p in players if p["playerId"] == playerId), None)

# Mutation
class CreatePlayer(graphene.Mutation):
    class Arguments:
        name = String(required=True)

    player = Field(PlayerType)

    def mutate(root, info, name):
        player_id = str(len(players) + 1)
        player = {"playerId": player_id, "name": name}
        players.append(player)
        
        # # Notify subscribers
        # OnPlayerCreated.broadcast(
        #     group="player_updates",
        #     payload={"player": player}
        # )
        
        return CreatePlayer(player=player)

class UpdatePlayer(graphene.Mutation):
    class Arguments:
        playerId = ID(required=True)
        name = String()

    player = Field(PlayerType)

    def mutate(root, info, playerId, name=None):
        player = next((p for p in players if p["playerId"] == playerId), None)
        if not player:
            raise Exception("Player not found")
        
        if name:
            player["name"] = name
        
        # # Notify subscribers
        # OnPlayerUpdated.broadcast(
        #     group="player_updates",
        #     payload={"player": player}
        # )
        
        return UpdatePlayer(player=player)

class Mutation(ObjectType):
    create_player = CreatePlayer.Field()
    update_player = UpdatePlayer.Field()

# Subscriptions
# class OnPlayerCreated(Subscription):
#     class Arguments:
#         pass

    player = Field(PlayerType)

    @staticmethod
    def subscribe(root, info):
        return ["player_updates"]

    @staticmethod
    def publish(payload, info):
        return OnPlayerCreated(player=payload["player"])

# class OnPlayerUpdated(Subscription):
#     class Arguments:
#         pass

    player = Field(PlayerType)

    @staticmethod
    def subscribe(root, info):
        return ["player_updates"]

    @staticmethod
    def publish(payload, info):
        return OnPlayerUpdated(player=payload["player"])

# class Subscription(ObjectType):
#     on_player_created = OnPlayerCreated.Field()
#     on_player_updated = OnPlayerUpdated.Field()

# schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
schema = graphene.Schema(query=Query, mutation=Mutation)