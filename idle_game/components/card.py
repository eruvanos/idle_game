from arcade import Texture
from arcade.gui import UIAnchorLayout, Property, UILabel, UITextureButton, UIOnClickEvent

import idle_game.assets
from idle_game.arcade_gui import UIImage, UIProgressBar


class Card(UIAnchorLayout):
    active = Property(False)

    def __init__(self,
                 *,
                 texture: Texture,
                 data=None,
                 cast_time=5,
                 **kwargs
                 ):
        super().__init__(
            width=100,
            height=150,
            size_hint=(None, None),
            **kwargs
        )

        self.data = data
        self.with_background(texture=idle_game.assets.panel_9patch())
        self.with_padding(5, 5, 5, 5)

        self.add(
            align_y=0,
            anchor_y="top",
            child=UIImage(
                texture=texture,
                size_hint=(1, 1),
                size_hint_max=(80, 80)
            ).with_border(color=(162, 140, 125)),
        )

        self.progress = self.add(
            align_y=-85,
            anchor_y="top",
            child=UIProgressBar(
                max_value=cast_time,
                width=80,
                height=10,
                back_texture=idle_game.assets.button_brown_9patch(),
                full_texture=idle_game.assets.enhance(idle_game.assets.BUTTON_BROWN, 0.8),
            ))

        self.add(
            align_y=-97,
            anchor_y="top",
            child=UILabel(
                text=f"Takes {cast_time}s",
                align="center",
                height=12,
                font_size=9,
                text_color=(95, 64, 40),
                size_hint=(1, None),
            ),
        )

        self.button = self.add(
            align_y=0,
            anchor_y="bottom",
            child=UITextureButton(
                width=80,
                height=25,
                text="start",
                texture=idle_game.assets.button_brown_9patch(),
                texture_hovered=idle_game.assets.button_brown_9patch(enhanced=1.2),
                texture_pressed=idle_game.assets.button_brown_9patch(enhanced=0.8),
            ))

        @self.button.event
        def on_click(event: UIOnClickEvent):
            if self.active:
                self.deactivate()
            else:
                self.activate()

        self.register_event_type("on_finish")
        self.register_event_type("on_card_activated")

    def on_update(self, dt):
        if self.active:
            self.progress.value += dt

            if self.progress.value > self.progress.max_value:
                self.progress.value = 0

                self.dispatch_event("on_finish", self)

    def activate(self):
        self.active = True
        self.button.text = "stop"

        if self.active:  # card got activated
            self.dispatch_event("on_card_activated", self)

    def deactivate(self):
        self.active = False
        self.button.text = "start"
        self.progress.value = 0

    def on_card_activated(self, source):
        pass

    def on_finish(self, source):
        pass
