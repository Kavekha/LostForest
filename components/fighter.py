from config.constants import ConstColors
from utils.death_functions import kill_monster
from random import randint


'''
Fighter class : combat system.
ideal : 
    Si on va dans une fonction "fighter", on envoie du x.fighter.
    Si on sort de la fonction "fighter", on envoie du x.owner 
'''


class Fighter:
    def __init__(self, hp, might, vitality, death_function=kill_monster, xp_value=0, base_dmg=(0, 2)):
        self.owner = None
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function
        self.xp_value = xp_value

        self.might = might
        self.vitality = vitality
        self.base_damage = base_dmg

    def attack(self, target, events):
        # target is entity, not entity.fighter # TODO: Choisir si on envoie du entity.fighter ou entity
        min_dam, max_dam = self.base_damage
        base_damage = randint(min_dam, max_dam)
        might_bonus = randint(0, self.might)
        damage = might_bonus + base_damage

        if self.might >= (damage * 2):
            damage *= 2

        # get hit retourne les dmg modifiés par les effets se trouvant sur la Target.
        modified_damage = target.fighter.get_hit(self, damage, events)

        if modified_damage <= 0:
            events.add_event({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), 'color': ConstColors.NO_DAMAGE_ATTACK})
        else:
            events.add_event({'message': '{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(modified_damage)),
                'color': ConstColors.DAMAGING_ATTACK})

            # take_damage joue de potentiels effets dû à des dmg.
            target.fighter.take_damage(self, modified_damage, events)

    def is_alive(self):
        if self.hp > 0:
            return True
        return False

    # get_hit : j ai ete touché, je vais prendre des degats.
    # Je peux les reduire si j ai de l'armure ou autre chose.
    def get_hit(self, attacker, damage, events):
        damage_reduction = randint(0, self.vitality)
        modified_damage = max(0, (damage - damage_reduction))

        if modified_damage > self.vitality:
            modified_damage *= 2
        elif (modified_damage * 2) < self.vitality:
            modified_damage = int(modified_damage / 2)

        return modified_damage

    def take_damage(self, attacker, amount, events):
        self.hp -= amount
        if self.hp <= 0:
            # attacker is fighter
            self.on_death(attacker, events)
            attacker.kill(self, events)

    def on_death(self, attacker, events):
        self.death_function(self.owner, attacker.owner, events)

    def kill(self, killed, events):
        if self.owner.level and killed.xp_value:
            self.owner.level.add_xp(killed.xp_value, events)

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
