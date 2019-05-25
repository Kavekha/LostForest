# http://rogueliketutorials.com/tutorials/tcod/part-12/

from random import randint


def random_choice_index(chances):
    print('index chances : ', chances)
    random_chance = randint(1, sum(chances))
    print('random chance is : ', random_chance)

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            print('return choice ', choice)
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    print('choice dict: ', choice_dict)
    choices = list(choice_dict.keys())
    print('choice list : ', choices)
    chances = list(choice_dict.values())
    print('chances list : ', chances)

    index_choices = random_choice_index(chances)
    print('return from random choice from dict : ', choices[index_choices])


monster_chances = {'orc': 80, 'troll': 20}
print(monster_chances)
monster_choice = random_choice_from_dict(monster_chances)
