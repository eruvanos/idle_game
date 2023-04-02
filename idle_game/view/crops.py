from typing import Optional

import arcade
from arcade import load_texture, Texture
from arcade.gui import UIManager, UIAnchorLayout, UIGridLayout, UIWidget, UIInteractiveWidget, UIOnClickEvent

from idle_game.assets.index import crop_field_10x10_png, crop_crop_carrot_0_png, \
    crop_crop_carrot_1_png, crop_crop_carrot_2_png, crop_crop_carrot_3_png
from idle_game.components.headbar.headbar import HeadBar
from idle_game.sidebar import GlobalSideBar


class CropField(UIInteractiveWidget):

    def __init__(self, texture: Optional[Texture] = None, **kwargs):
        super().__init__(**kwargs)

        if texture:
            self.with_background(texture=texture)

        self._progress = 0
        self._grow = False

    def on_update(self, dt):
        if self.hovered:
            self.with_border(width=1, color=arcade.color.LIGHT_GRAY)
        else:
            self.with_border(width=0)
            self.trigger_full_render()

        if self._grow:
            self._progress += dt

            if self._progress == 0:
                self.with_background(texture=load_texture(crop_crop_carrot_0_png))
            if self._progress > 0:
                self.with_background(texture=load_texture(crop_crop_carrot_1_png))
            if self._progress > 2:
                self.with_background(texture=load_texture(crop_crop_carrot_2_png))
            if self._progress > 5:
                self.with_background(texture=load_texture(crop_crop_carrot_3_png))

    def on_click(self, event: UIOnClickEvent):
        self.with_background(texture=load_texture(crop_crop_carrot_0_png))

        self._progress = 0
        self._grow = True


class Crops(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((120, 191, 92))

        self.manager = UIManager()
        self.manager.add(GlobalSideBar())
        self.manager.add(HeadBar())

        anchor = self.manager.add(UIAnchorLayout())
        anchor.with_padding(left=120)

        # View Content

        field_size = 12
        cell_size = 30

        grid = UIGridLayout(
            column_count=field_size,
            row_count=field_size,
            horizontal_spacing=5,
            vertical_spacing=5,
            size_hint=(0, 0)
        )
        grid.with_background(texture=load_texture(crop_field_10x10_png))

        for x in range(1, field_size - 1):
            for y in range(1, field_size - 1):
                grid.add(
                    child=CropField(
                        width=cell_size,
                        height=cell_size,
                    ),
                    col_num=x,
                    row_num=y
                )

        # we skip outer row and columns to match with background image
        for x in range(field_size):
            grid.add(
                child=UIWidget(
                    width=cell_size,
                    height=cell_size,
                    ),
                col_num=x,
                row_num=0
            )

        for y in range(field_size):
            grid.add(
                child=CropField(
                    width=cell_size,
                    height=cell_size,
                ),
                col_num=field_size - 1,
                row_num=y
            )

        # grid_size = (field_size + 2) * cell_size
        # min_width, min_height = grid.size_hint_min
        # grid.resize(width=min_width, height=min_height)

        anchor.add(grid)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()
