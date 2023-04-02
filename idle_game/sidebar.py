from arcade import get_window
from arcade.gui import UIOnActionEvent

from idle_game import view
from idle_game.arcade_gui import UISideBar


class GlobalSideBar(UISideBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        views = {
            "Resources": view.Resources,
            "Crops": view.Crops,

        }

        for key in views.keys():
            self.add_button(key, key)

        @self.event()
        def on_action(event: UIOnActionEvent):
            window = get_window()

            view_factory = views.get(event.action)
            if view_factory:
                window.show_view(view_factory())
            else:
                print("unknown command")
