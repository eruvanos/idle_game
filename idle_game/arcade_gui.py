from typing import Union

from arcade import Texture
from arcade.gui import UIWidget, Surface, Property, NinePatchTexture, bind, UIAnchorLayout, UIBoxLayout, UIFlatButton, \
    UIOnClickEvent, UIOnActionEvent, UITextureButton

import idle_game.assets.resources


class UIImage(UIWidget):
    def __init__(
        self,
        *,
        texture: Texture,
        **kwargs,
    ):
        self.texture = texture

        super().__init__(**kwargs)

    def do_render(self, surface: Surface):
        self.prepare_render(surface)
        surface.draw_texture(
            x=0,
            y=0,
            width=self.width,
            height=self.height,
            tex=self.texture
        )


class UIProgressBar(UIWidget):
    value = Property(0)

    def __init__(
        self,
        *,
        value: int = 0,
        max_value: int = 100,
        back_texture: Union[Texture, NinePatchTexture],
        full_texture: Union[Texture, NinePatchTexture],
        width=100,
        height=20,
        **kwargs,
    ):
        self.value = value
        self.max_value = max_value
        self._full_texture = full_texture

        super().__init__(
            width=width,
            height=height,
            **kwargs
        )
        PADDING = 3
        self.with_padding(PADDING, PADDING, PADDING, PADDING)
        self.with_background(texture=back_texture)

        bind(self, "value", self.trigger_render)

    def do_render(self, surface: Surface):
        self.prepare_render(surface)

        percentage = int(self.value * (self.content_width / self.max_value))
        surface.draw_texture(0, 0, percentage, self.content_height, self._full_texture)


class UISideBar(UIAnchorLayout):
    # UIAnchorLayout used as baseclass so it can be added to UIManager and will position actual content (UIBoxLayout).
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs
        )

        self._buttons = UIBoxLayout(space_between=5, size_hint=(0, 1))
        self._buttons.with_border(color=(80, 73, 23))
        self._buttons.with_background(color=(196, 154, 108))
        self._buttons.with_padding(all=5, top=10)

        self.add(self._buttons, anchor_x="left", anchor_y="top", align_x=0, align_y=-30)

        self.register_event_type("on_action")

    def add_button(self, text: str, action: str):
        button = self._buttons.add(UITextureButton(
            width=100,
            height=30,
            text=text,
            texture=idle_game.assets.button_brown_9patch(),
            texture_hovered=idle_game.assets.button_brown_9patch(enhanced=1.2),
            texture_pressed=idle_game.assets.button_brown_9patch(enhanced=0.8),
        ))

        @button.event()
        def on_click(event: UIOnClickEvent):
            self.dispatch_event("on_action", UIOnActionEvent(event.source, action))
