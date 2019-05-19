def get_item_table(map_type):
    tables = {
        'standard_map': {
            'items_list': ['healing potion']
        }
    }
    try:
        return tables[map_type]
    except:
        return None
