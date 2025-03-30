from ariadne import ObjectType, SubscriptionType, load_schema_from_path,make_executable_schema
subscription = SubscriptionType()

@subscription.source("messageAdded")
async def message_added_source(obj, info):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    while True:
        message = await channel_layer.receive("messages")
        yield message["text"]

@subscription.field("messageAdded")
def message_added_resolver(message, info):
    return {"message": message}

query = ObjectType("Query")

resolvers = [query, subscription]

type_defs =load_schema_from_path('api/graphql/ariadne/schemas/schema.graphql')

schema = make_executable_schema(type_defs, resolvers)