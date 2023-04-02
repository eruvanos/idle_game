from typing import Dict, Any

from arcade.gui import Property, DictProperty


class GameState:
    stone = Property(0)
    wood = Property(0)
    fruits = Property(0)
    gold = Property(0)

    crop_field: Dict[tuple, Any] = DictProperty()


# TODO fix this :D
current_game_state = GameState()
