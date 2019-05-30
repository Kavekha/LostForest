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
    def __init__(self, hp, might, vitality, death_function=kill_monster):
        self.owner = None
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function

        self.might = might
        self.vitality = vitality

    def attack(self, target, events):
        # target is entity, not entity.fighter # TODO: Choisir si on envoie du entity.fighter ou entity
        base_damage = randint(0, 2)
        damage = base_damage
        if self.might < base_damage:
            damage = self.might
        elif self.might >= (base_damage * 2):
            damage *= 2

        # get hit retourne les dmg modifiés par les effets se trouvant sur la Target.
        modified_damage = target.fighter.get_hit(self, damage, events)

        if modified_damage <= 0:
            events.add_event({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), 'color': ConstColors.NO_DAMAGE_ATTACK})
        else:
            # take_damage joue de potentiels effets dû à des dmg.
            target.fighter.take_damage(self, modified_damage, events)
            if target.fighter:
                # npc lost their fighter component on kill_function, but not the player
                if target.fighter.is_alive():
                    events.add_event({'message': '{0} attacks {1} for {2} hit points.'.format(
                        self.owner.name.capitalize(), target.name, str(modified_damage)),
                        'color': ConstColors.DAMAGING_ATTACK})

    def is_alive(self):
        if self.hp > 0:
            return True
        return False

    # get_hit : j ai ete touché, je vais prendre des degats.
    # Je peux les reduire si j ai de l'armure ou autre chose.
    def get_hit(self, attacker, damage, events):
        if damage > self.vitality:
            damage *= 2
        elif (damage * 2) < self.vitality:
            damage = int(damage / 2)
        return damage

    def take_damage(self, attacker, amount, events):
        self.hp -= amount
        if self.hp <= 0:
            # attacker is fighter
            attacker.kill(self, events)
            self.on_death(attacker, events)

    def on_death(self, attacker, events):
        self.death_function(self.owner, attacker.owner, events)

    def kill(self, killed, events):
        pass

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
