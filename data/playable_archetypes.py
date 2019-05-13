def get_player_stats(type):
    player_archetype = {
        'base_player': {
            'hp': 30
        }
    }
    try:
        return player_archetype[type]
    except:
        return None
