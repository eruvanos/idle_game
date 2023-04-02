from typing import List

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILayout, UILabel, UIWidget

import idle_game.assets.resources
from idle_game.components.card import Card
from idle_game.gamestate import current_game_state
from idle_game.sidebar import GlobalSideBar
from idle_game.components.headbar.headbar import HeadBar
from idle_game.transition import Transition, EaseFunctions


class ToastKillTransition(Transition):
    """
    Removes a widget from its parent after some time
    """

    def __init__(self, duration: float):
        super().__init__(start=0, end=0, attribute=None, duration=duration)

    def update(self, subject: UIWidget, dt):
        self._elapsed += dt

        if self.finished:
            subject.parent.remove(subject)


class Toast(UILabel):
    """
    Temporarily text shown to the user.

    :param text: Text to show
    :param timeout: Text will vanish after x seconds
    :param kwargs: UILabel constructor kwargs
    """

    def __init__(self, text: str, timeout=2.0, **kwargs):
        super().__init__(text=text, **kwargs)
        self._transitions: List[Transition] = []

        self.add_transition(ToastKillTransition(timeout))

    def on_update(self, dt):

        # Update transitions 
        for transition in self._transitions[:]:
            transition.update(self, dt)

            if transition.finished:
                self._transitions.remove(transition)

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    @property
    def opacity(self):
        return self.label._label.opacity

    @opacity.setter
    def opacity(self, value):
        self.label._label.opacity = value
        self.trigger_full_render()

    @property
    def center_y(self):
        return super().center_y

    @center_y.setter
    def center_y(self, value):
        self.rect = self.rect.align_center_y(value)


class ToastManager(UILayout):
    def __init__(self, **kwargs):
        super().__init__(
            size_hint=(1, 1),
            **kwargs
        )

    def notify(self, text: str, timeout=2):
        toast = self.add(Toast(text=text, timeout=timeout))

        center_x = self.content_width // 2
        toast.rect = toast.rect.align_center_x(center_x)

        # move Toast up by x pixel
        toast.add_transition(Transition(
            start=10,
            end=30,
            duration=1.0,
            attribute="center_y",
            ease_function=EaseFunctions.linear,
        ))

        # blend in
        # flickers, skip for now 🤷
        # toast.add_transition(Transition(
        #     start=50,
        #     end=255,
        #     duration=0.2,
        #     attribute="opacity",
        #     ease_function=EaseFunctions.linear,
        # ))

        # blend out
        toast.add_transition(Transition(
            start=255,
            end=0,
            duration=0.5,
            delay=1.5,
            attribute="opacity",
            ease_function=EaseFunctions.linear,
        ))


class Resources(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.manager = UIManager()
        self.manager.add(GlobalSideBar())
        self.manager.add(HeadBar())

        toast_manager = ToastManager()

        anchor = self.manager.add(UIAnchorLayout())
        self.cards = anchor.add(UIBoxLayout(vertical=False, space_between=10),
                                align_x=120,
                                align_y=-50,
                                anchor_x="left",
                                anchor_y="top")

        # WOOD
        tree_card = self.cards.add(Card(texture=idle_game.assets.NORMAL_TREE, cast_time=2))

        @tree_card.event()
        def on_finish(source):
            current_game_state.wood += 1
            toast_manager.notify("+1 Wood")

        # STONE
        stone_card = self.cards.add(Card(texture=idle_game.assets.STONE))

        @stone_card.event()
        def on_finish(source):
            current_game_state.stone += 1
            toast_manager.notify("+1 Stone")

        # FRUITS
        fruit_card = self.cards.add(Card(texture=idle_game.assets.PEAR_TREE))

        @fruit_card.event()
        def on_finish(source):
            current_game_state.fruits += 1
            toast_manager.notify("+1 Fruit")

        self.cards = [
            tree_card,
            stone_card,
            fruit_card,
        ]

        for card in self.cards:
            card.on_card_activated = self._on_card_activated

        self.manager.add(toast_manager)

    def _on_card_activated(self, card: Card):
        for c in self.cards:
            if card != c:
                c.deactivate()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()
