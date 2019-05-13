'''
Fighter class : combat system.
'''


class Fighter:
    def __init__(self, hp):
        self.owner = None
        self.max_hp = hp
        self.hp = hp

    def attack(self, target, events):
        damage = 1
        target.fighter.take_damage(damage, events)

        if damage > 0:
            events.add_event({'message': '{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage))})
        else:
            events.add_event({'message': '{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name)})

    def take_damage(self, amount, events):
        self.hp -= amount
        if self.hp <= 0:
            events.add_event({'dead': self.owner})
