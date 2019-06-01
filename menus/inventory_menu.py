from menus.menu import Menu
from config.constants import ConstTexts


class InventoryMenu(Menu):
    def __init__(self, inventory):
        super().__init__(inventory)
        self.header = ConstTexts.INVENTORY_HEADER

        self.update_options()

    def update_options(self):
        if len(self.source.items) == 0:
            self.header = ConstTexts.INVENTORY_HEADER + '\n' + ConstTexts.INVENTORY_EMPTY
            self.display_options = []
            self._options = []
        else:
            self.display_options = [item.name for item in self.source.items]
            self._options = [item for item in self.source.items]

    def return_choice_result(self, string_choice):
        if self.source.owner.fighter.is_alive():
            success = self.source.use(string_choice)
            if success:
                self.update_options()
