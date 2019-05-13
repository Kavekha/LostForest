def get_monster_table(map_type):
    tables = {
        'standard_map': {
            'monsters_list': ['Ougloth', 'Living root']
        }
    }
    try:
        return tables[map_type]
    except:
        return None