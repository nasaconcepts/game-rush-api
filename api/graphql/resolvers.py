from .models import Game,Player
from datetime import datetime

def resolve_games(_,info):
    return Game.objects.all()
def resolve_players(_,info,gameId=None):
    if gameId:
        return Player.objects.filter(game_id=gameId)
    return Player.objects.all()
def resolve_join_game(_, info, name, gameId):
    game = Game.objects.get(id=gameId)
    player = Player.objects.create(name=name, game=game)
    return player

# Subscription resolver (real-time updates)
async def resolve_player_joined(_, info, gameId):
    async for player in Player.objects.filter(game_id=gameId).order_by('-joined_at'):
        yield player