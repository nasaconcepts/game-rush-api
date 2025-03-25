from ariadne import QueryType, MutationType, SubscriptionType, make_executable_schema
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Sample data storage (non-ORM)
players = []

query = QueryType()
mutation = MutationType()
subscription = SubscriptionType()

# Query: Get active players in a game
@query.field("activePlayers")
def resolve_active_players(_, info, game):
    return [player for player in players if player["game"] == game]

# Mutation: Player logs into the game
@mutation.field("playerLogin")
def resolve_player_login(_, info, username, game):
    new_player = {"username": username, "game": game}
    players.append(new_player)

    # Publish event for subscriptions
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"players_{game}",
        {"type": "player.joined", "player": new_player}
    )

    return new_player

# Subscription: Notify when a new player joins
@subscription.source("playerJoined")
async def subscribe_player_joined(_, info, game):
    channel_layer = get_channel_layer()
    group_name = f"players_{game}"

    # Join the WebSocket group
    async_to_sync(channel_layer.group_add)(group_name, info.context["channel_name"])

    try:
        while True:
            message = await info.context["channel_layer"].receive(info.context["channel_name"])
            if message["type"] == "player.joined":
                yield message["player"]
    finally:
        async_to_sync(channel_layer.group_discard)(group_name, info.context["channel_name"])

# Build schema
# type_defs = open("schema.graphql").read()
type_defs = """
type Player {
    username: String!
    game: String!
}

type Query {
    activePlayers(game: String!): [Player!]!
}

type Mutation {
    playerLogin(username: String!, game: String!): Player!
}

type Subscription {
    playerJoined(game: String!): Player!
}
"""

schema = make_executable_schema(type_defs,query, mutation, subscription)
