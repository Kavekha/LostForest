from config.constants import ConstColors, ConstTexts
from random import randint


'''
Targeting retourne un tuple (dict_target, valid_target)
dictionnaire : 
        results = {
            'requested': None,
            'not_requested': [],
            'tile': None
            }

# Requested : contient l'entité type reclamée.
# Not requested : contient une liste d'entités non reclammées, pour messages "flavor".
# Tile : toujours presente.

valid_target = True s'il y a bien un Requested, False sinon (L'effet n'aur apas lieux mais des messages peuvent etre donnés)
'''


# v0.0.20
# TODO: texte "heal" dans l'objet, peut etre plutot dans l'effet de la potion (Sur Fighter?)
def heal(user, source_of_effect, dict_results, events):
    # source of effect is an item_component for now.
    power = source_of_effect.power
    target = dict_results.get('requested')

    if target.fighter.hp == target.fighter.max_hp:
        return {'consume_item': False,
                'message': ConstTexts.FULL_HEAL_ALREADY,
                'color': ConstColors.FULL_HEAL_ALREADY}
    else:
        events.add_event({'message': '{} drinks a {}'.format(target.name, source_of_effect.owner.name),
                          'color': ConstColors.THROW_ITEM_COLOR})
        target.fighter.heal(power)
        return {'consume_item': True,
                'message': ConstTexts.WOUND_HEALED,
                "color": ConstColors.WOUND_HEALED}


# v0.0.20
def acide(user, source_of_effect, dict_results, events):
    # source of effect is an item_component for now.
    power = source_of_effect.power
    target = dict_results.get('requested')

    damage = randint(int(power / 2), int(power * 1.5))

    if target and target.fighter and user.fighter:
        events.add_event({'message': '{} throw a {} at {}'.format(user.name, source_of_effect.owner.name, target.name),
                          'color': ConstColors.THROW_ITEM_COLOR})
        user.fighter.do_damage(target, damage, events)
        return {'consume_item': True}
    else:
        return {'consume_item': False}
