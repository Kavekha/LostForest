from menus.menu import Menu
from data_loaders.localization import Texts
from components.equippable import slot_to_text, get_equipment_in_slot


class InventoryMenu(Menu):
    def __init__(self, inventory):
        super().__init__(inventory)
        self.header = Texts.get_text('INVENTORY_HEADER')
        self.forced_width = 40
        self.update_options()

    def update_options(self):
        if len(self.source.items) == 0:
            self.header = (
                    Texts.get_text('INVENTORY_HEADER') + "\n" + Texts.get_text('INVENTORY_EMPTY')
            )
            self.display_options = []
            self._options = []
        else:
            self.display_options = []
            player = self.source.owner
            for item in self.source.items:
                if (
                    item.equippable
                    and player.equipment
                    and item
                    == get_equipment_in_slot(item.equippable.slot, player.equipment)
                ):
                    self.display_options.append(
                        "{} [{}]".format(item.name, slot_to_text(item.equippable.slot))
                    )
                else:
                    self.display_options.append(item.name)

            self._options = [item for item in self.source.items]

    def return_choice_result(self, string_choice):
        if self.source.owner.fighter.is_alive():
            success = self.source.use(string_choice)
            if success:
                self.update_options()


class DropMenu(InventoryMenu):
    def __init__(self, inventory):
        super().__init__(inventory)
        self.header = Texts.get_text('INVENTORY_HEADER')
        self.forced_width = 40
        self.update_options()

    def return_choice_result(self, string_choice):
        if self.source.owner.fighter.is_alive():
            success = self.source.drop(string_choice)
            if success:
                self.update_options()
