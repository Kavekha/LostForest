# http://rogueliketutorials.com/tutorials/tcod/part-12/


def from_dungeon_level(table, dungeon_level):
    print('reverse table : ', reversed(table))
    for (value, level) in reversed(table):
        print('for : value, level', value, level)
        if dungeon_level >= level:
            return value
    return 0


max_monster = [[2, 1], [3, 4], [5, 6]]
level = 3

print(from_dungeon_level(max_monster, level))