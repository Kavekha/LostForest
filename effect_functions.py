from config.constants import ConstColors, ConstTexts


# TODO: texte "heal" dans l'objet, peut etre plutot dans l'effet de la potion (Sur Fighter?)
def heal(user, power, target):

    if target.fighter.hp == target.fighter.max_hp:
        return {'consume_item': False,
                'message': ConstTexts.FULL_HEAL_ALREADY,
                'color': ConstColors.FULL_HEAL_ALREADY}
    else:
        target.fighter.heal(power)
        return {'consume_item': True,
                'message': ConstTexts.WOUND_HEALED,
                "color": ConstColors.WOUND_HEALED}


def grease(user, power, target):
    print('effect: grease: args, kwargs ')

