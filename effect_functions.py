from config.constants import ConstColors, ConstTexts


# TODO: texte "heal" dans l'objet, peut etre plutot dans l'effet de la potion (Sur Fighter?)
def heal(*args, **kwargs):
    print('effect : heal : args, kwargs ', *args, **kwargs)
    entity = args[0]
    power = args[1]

    if entity.fighter.hp == entity.fighter.max_hp:
        return {'consume_item': False,
                'message': ConstTexts.FULL_HEAL_ALREADY,
                'color': ConstColors.FULL_HEAL_ALREADY}
    else:
        entity.fighter.heal(power)
        return {'consume_item': True,
                'message': ConstTexts.WOUND_HEALED,
                "color": ConstColors.WOUND_HEALED}
