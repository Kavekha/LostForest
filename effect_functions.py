import libtcodpy as libtcod


# TODO: texte "heal" dans l'objet, peut etre plutot dans l'effet de la potion (Sur Fighter?)
def heal(*args, **kwargs):
    print('effect : heal : args, kwargs ', *args, **kwargs)
    entity = args[0]
    power = args[1]

    results = None

    if entity.fighter.hp == entity.fighter.max_hp:
        return {'consume_item': False,
                'message': 'You are already at full health',
                'color': libtcod.yellow}
    else:
        entity.fighter.heal(power)
        return {'consume_item': True,
                'message': 'Your wounds start to feel better!',
                "color": libtcod.green}
