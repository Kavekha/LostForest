from config.constants import ConstColors
from utils.death_functions import kill_monster


'''
Fighter class : combat system.
ideal : 
    Si on va dans une fonction "fighter", on envoie du x.fighter.
    Si on sort de la fonction "fighter", on envoie du x.owner 
'''

class Fighter:
    def __init__(self, hp, death_function=kill_monster):
        self.owner = None
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function

    def attack(self, target, events):
        # target is entity, not entity.fighter # TODO: Choisir si on envoie du entity.fighter ou entity
        damage = 1
        target.fighter.take_damage(self, damage, events)

        if damage > 0:
            events.add_event({'message': '{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), 'color': ConstColors.DAMAGING_ATTACK})
        else:
            events.add_event({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), 'color': ConstColors.NO_DAMAGE_ATTACK})

    def take_damage(self, attacker, amount, events):
        self.hp -= amount
        if self.hp <= 0:
            self.death_function(self.owner, attacker.owner, events)

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
