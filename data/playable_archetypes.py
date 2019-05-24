def get_player_stats(type='base_player'):
    player_archetype = {
        'base_player': {
            'hp': 300
        }
    }
    try:
        return player_archetype[type]
    except:
        return None
