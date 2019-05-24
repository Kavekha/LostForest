import libtcodpy as libtcod


def menu(con, header, options, width, screen_width, screen_height):

    '''
    :param con: window where the menu is displayed
    :param header: text
    :param options: list with various options, like items in inventory.
    :param width: menu width
    :param screen_width:
    :param screen_height:
    :return:
    '''

    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    menu_window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(menu_window, libtcod.white)
    libtcod.console_print_rect_ex(menu_window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')

    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(menu_window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(menu_window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
    print('inventory blit done')