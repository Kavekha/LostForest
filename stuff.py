def check_save(game):
    print('game is ', game)
    print('game.events ', game.events)
    print('game.fov_algorithm', game.fov_algorithm)
    print('game.fov_recompute', game.fov_recompute)
    print('game.map', game.map)
    print('game.player', game.player)
    print('game.game_state', game.game_state)
    print('game.previous_game_state', game.previous_game_state)
    print('------')
    print('', game.map.map_type)
    print('', game.map.colors)
    print('', game.map.width)
    print('', game.map.height)
    print('', game.map.room_max_size)
    print('', game.map.room_min_size)
    print('', game.map.max_rooms)
    print('', game.map.max_monsters_room)
    print('', game.map.max_items_room)
    print('', game.map.tiles)
    print('', game.map.fov_map)
    print('', game.map.rooms)
    print('', game.map.entities)
    print('', game.map.spawner)
    print('------------')
    '''
    count = 0
    block_sight = 0
    blocked = 0
    explored = 0
    nothing = 0
    for x in game.map.tiles:
        for tile in x:
            #print('attributes are : ', tile.blocked, tile.block_sight, tile.explored)
            if tile.block_sight:
                print('tile block sight')
                block_sight += 1
            if tile.blocked:
                print('tile blocked')
                blocked += 1
            if tile.explored:
                print('tile explored')
                explored += 1
            if not tile.block_sight and not tile.blocked and not tile.explored:
                print('nothing')
                nothing += 1
            count += 1
        print('count is ', count)
        print('block sight is ', block_sight)
        print('blocked is ', blocked)
        print('explored is ', explored)
        print('nothing is ', nothing)'''
    print('----------')
    player = game.player
    print('player ', player.x, player.y, player.char, player.color, player.name, player.render_order)
    if player.fighter:
        print('player fighter')
    if player.inventory:
        print('player inventory')
    print('fov light and block ', player.fov_radius, player.light_walls, player.blocks)
    print(player.fighter.hp)
    print(player.fighter.max_hp)
    print('------------------')
    for entity in game.map.entities:
        if entity.fighter:
            print('entity ', entity.name, entity.fighter.hp)
