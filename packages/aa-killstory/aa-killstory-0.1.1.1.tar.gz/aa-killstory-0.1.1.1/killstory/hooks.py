from allianceauth.hooks import hooks
from allianceauth.hooks.menu import MenuItemHook
from allianceauth.hooks.urls import URLHook
from django.urls import path, include

@hooks.register('menu_item_hook')
def register_killstory_menu():
    return MenuItemHook(
        'Killstory',
        'fas fa-skull-crossbones',
        'aa_killstory:index',
        1000
    )

@hooks.register('url_hook')
def register_killstory_urls():
    return URLHook(
        'aa_killstory',
        'killstory'
    )
