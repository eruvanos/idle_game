from arcade import load_texture
from arcade.gui import UIBoxLayout, UIAnchorLayout, UILabel

import idle_game.assets.resources
from idle_game.arcade_gui import UIImage
from idle_game.gamestate import current_game_state


class HeadBar(UIAnchorLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        top_layout = self.add(
            child=UIBoxLayout(vertical=False, space_between=10, size_hint=(1, 0)).with_padding(top=5, bottom=8),
            align_x=0,
            align_y=0,
            anchor_x="left",
            anchor_y="top",
        )
        top_layout.with_background(texture=idle_game.assets.button_brown_9patch())

        self.wood_label = UILabel(text=f"Wood: {current_game_state.wood}", align="center", )
        self.stone_label = UILabel(text=f"Stone: {current_game_state.stone}", align="center", )
        self.fruit_label = UILabel(text=f"Fruits: {current_game_state.fruits}", align="center", )
        self.gold_label = UILabel(text=f"Gold: {current_game_state.gold}", align="center", size_hint=(1, None), )

        # Children of top_layout should request maximal size and center content within them
        # (UIAnchorLayout does it by default)
        top_layout.add(UIAnchorLayout(children=[UIBoxLayout(  # to place multiple UIWidgets, we use UIBoxLayout
            children=[
                UIImage(
                    texture=load_texture(file_path=idle_game.assets.resources.WOOD),
                    width=25,
                    height=25,
                ),
                self.wood_label
            ],
            vertical=False,
        )]))
        top_layout.add(UIAnchorLayout(children=[UIBoxLayout(
            children=[
                UIImage(
                    texture=load_texture(file_path=idle_game.assets.resources.STONE),
                    width=25,
                    height=25,
                ),
                self.stone_label
            ],
            vertical=False,
        )]))

        top_layout.add(UIAnchorLayout(children=[UIBoxLayout(
            children=[
                # UIImage(
                #     texture=load_texture(file_name=idle_game.assets.resources.STONE),
                #     width=25,
                #     height=25,
                # ),
                self.fruit_label
            ],
            vertical=False,
        )]))

        top_layout.add(self.gold_label)

    def on_update(self, dt):
        self.wood_label.text = f"Wood: {current_game_state.wood}"
        self.stone_label.text = f"Stone: {current_game_state.stone}"
        self.fruit_label.text = f"Fruits: {current_game_state.fruits}"
        self.gold_label.text = f"Gold: {current_game_state.gold}"
