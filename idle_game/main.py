"""
Example shows how to use UIAnchorWidget to position widgets on screen.
Dummy widgets indicate hovered, pressed and clicked.
"""

import arcade

from idle_game.view.resources import Resources


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "UI Gallery", resizable=True)

        self.show_view(Resources())


if __name__ == '__main__':
    window = MainWindow()
    arcade.run()
