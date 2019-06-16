from random import randint


# Receive a dict with 'object':weight.
# Make it in two lists and send it to a function that roll the object chosen according to wheight.
def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    choice_index = random_choice_index(chances)

    return choices[choice_index]


# list of object weights.
# Rand from 1 to sum of all weight.
# Add all chances until rand < weight sum up until now.
def random_choice_index(chances):
    random_chance = randint(0, sum(chances) - 1)
    running_sum = 0
    choice = 0
    for weight in chances:
        running_sum += weight

        if random_chance <= running_sum:
            return choice
        choice += 1
    else:
        return choice
