from allianceauth.hooks import hooks
from allianceauth.hooks.menu import MenuItemHook

@hooks.register('menu_item_hook')
def register_menu():
    return MenuItemHook(
        'AA Killstory',
        'fas fa-skull-crossbones',
        'aa_killstory:index',
        1000
    )
