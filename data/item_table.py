def get_item_table(map_type):
    tables = {
        'standard_map': {
            'healing potion': 10,
            'greater healing potion': 3
        },
        'forest_map': {
            'healing potion': 12,
            'greater healing potion': 1
        },
        'old_forest': {
            'healing potion': 15,
            'greater healing potion': 3
        },
        'thorns': {
            'healing potion': 20,
            'greater healing potion': 10
        }
    }
    try:
        return tables[map_type]
    except:
        return None
