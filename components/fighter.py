from random import randint

from config import color_config, game_config
from utils.death_functions import kill_monster
from data_loaders.localization import Texts


"""
Fighter class : combat system.
ideal : 
    Si on va dans une fonction "fighter", on envoie du x.fighter.
    Si on sort de la fonction "fighter", on envoie du x.owner 
"""


class Fighter:
    def __init__(self,
                 hp=1,
                 might=0,
                 vitality=0,
                 dexterity=0,
                 death_function=kill_monster,
                 xp_value=0,
                 base_dmg=(0, 2),
                 ):

        self.base_might = might
        self.base_vitality = vitality
        self.base_dexterity = dexterity
        self.base_damage = base_dmg

        self.owner = None
        self.base_max_hp = hp
        self.hp = self.max_hp
        self.death_function = death_function
        self.xp_value = xp_value

    @property
    def might(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.might_bonus
        else:
            bonus = 0
        return self.base_might + bonus

    @property
    def dexterity(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dexterity_bonus
        else:
            bonus = 0
        return self.base_dexterity + bonus

    @property
    def physical_power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.physical_power_bonus
        else:
            bonus = 0

        return self.might + bonus

    @property
    def physical_resistance(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.armor_bonus
        else:
            bonus = 0

        return self.vitality + bonus

    @property
    def vitality(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.vitality_bonus
        else:
            bonus = 0
        return self.base_vitality + bonus

    @property
    def damage(self):
        damage = None
        if self.owner and self.owner.equipment:
            damage = self.owner.equipment.weapon_damage
        if not damage:
            damage = self.base_damage

        return damage

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    def attack(self, target, events):
        # target is entity, not entity.fighter # TODO: Choisir si on envoie du entity.fighter ou entity
        # try to hit
        hit_success = self.try_to_hit(target.fighter, events)

        if hit_success:
            self.on_hit(target, events)
        else:
            self.on_miss(target, events)

    def on_hit(self, target, events):
        # follow a hit_success from try_to_hit
        damage = self.damage_formula()

        self.do_damage(target, damage, events)

    def damage_formula(self):
        min_dam, max_dam = self.damage
        final_damage = randint(min_dam, max_dam)

        final_damage *= self.physical_power
        final_damage *= game_config.FINAL_DAMAGE_MODIFIER

        return int(final_damage + 1)

    def on_miss(self, target, events):
        events.add_event(
            {
                "message": Texts.get_text('CHAR_ATTACKS_OTHER_MISS').format(
                    self.owner.name.capitalize(), target.name
                ),
                "color": color_config.NO_DAMAGE_ATTACK,
            }
        )

    def try_to_hit(self, target, events):
        '''return True if success, False if miss'''
        base = game_config.BASE_HIT_CHANCE
        modifier = (self.dexterity - target.dexterity) * game_config.MODIFIER_HIT_CHANCE
        to_hit = base + modifier

        # min hit chance?
        if to_hit < game_config.MIN_HIT_CHANCE:
            to_hit = game_config.MIN_HIT_CHANCE
        elif to_hit > game_config.MAX_HIT_CHANCE:
            to_hit = game_config.MAX_HIT_CHANCE

        # rand hit
        rand = randint(0, game_config.TO_HIT_ROLL)
        if rand <= to_hit:
            return True
        return False

    def do_damage(self, target, damage, events):
        # get hit retourne les dmg modifiés par les effets se trouvant sur la Target.
        modified_damage = target.fighter.get_hit(self, damage, events)

        if modified_damage <= 0:
            events.add_event(
                {
                    "message": Texts.get_text('CHAR_ATTACKS_OTHER_NO_DAMAGE').format(
                        self.owner.name.capitalize(), target.name
                    ),
                    "color": color_config.NO_DAMAGE_ATTACK,
                }
            )
        else:
            events.add_event(
                {
                    "message": Texts.get_text('CHAR_ATTACKS_OTHER_WITH_DAMAGE').format(
                        self.owner.name.capitalize(), target.name, str(modified_damage)
                    ),
                    "color": color_config.DAMAGING_ATTACK,
                }
            )

            # take_damage joue de potentiels effets dû à des dmg.
            target.fighter.take_damage(self, modified_damage, events)

    def is_alive(self):
        if self.hp > 0:
            return True
        return False

    # get_hit : j ai ete touché, je vais prendre des degats.
    # Je peux les reduire si j ai de l'armure ou autre chose.
    def get_hit(self, attacker, damage, events):
        damage_reduction = randint(0, self.physical_resistance)
        modified_damage = max(0, (damage - damage_reduction))

        return modified_damage

    def take_damage(self, attacker, amount, events):
        self.hp -= int(amount)
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
