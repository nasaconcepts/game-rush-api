from ariadne import ObjectType, SubscriptionType, load_schema_from_path,make_executable_schema
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio

query = ObjectType("Query")
mutation = ObjectType("Mutation")
subscription = SubscriptionType()

users = []  # In-memory user storage (replace with database in production)
user_id_counter = 1

@query.field("hello")
def resolve_hello(_, info):
    return "Hello, GraphQL!"

@query.field("getUser")
def resolve_get_user(_, info, id):
    for user in users:
        if str(user["id"]) == id:
            return user
    return None

@query.field("allUsers")
def resolve_all_users(_, info):
    return users

@mutation.field("createUser")
async def resolve_create_user(_, info, username, email):
    global user_id_counter
    new_user = {"id": str(user_id_counter), "username": username, "email": email}
    users.append(new_user)
    user_id_counter += 1
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "user_created", {"type": "user.created", "user": new_user}
    )
    return new_user

@mutation.field("updateUser")
async def resolve_update_user(_, info, id, username=None):
    for user in users:
        if str(user["id"]) == id:
            if username:
                user["username"] = username
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                "user_updated", {"type": "user.updated", "user": user}
            )
            return user
    return None

@subscription.source("userCreated")
async def user_created_source(obj, info):
    channel_layer = get_channel_layer()
    group_name = "user_created"
    while True:
        message = await channel_layer.group_receive(group_name)
        yield message["user"]

@subscription.field("userCreated")
def user_created_resolver(user, info):
    return user

@subscription.source("userUpdated")
async def user_updated_source(obj, info):
    channel_layer = get_channel_layer()
    group_name = "user_updated"
    while True:
        message = await channel_layer.group_receive(group_name)
        yield message["user"]

@subscription.field("userUpdated")
def user_updated_resolver(user, info):
    return user

resolvers = [query, mutation, subscription]

type_defs =load_schema_from_path('api/graphql/ariadne/schemas/schema.graphql')

schema = make_executable_schema(type_defs, resolvers)