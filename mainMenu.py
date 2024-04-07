import arcade
from arcade.gui import UIManager, UIFlatButton
from cardgame import *
from constants import *


class MainMenuView(arcade.View):
    """ View to hold main Menu """

    def __init__(self):
        super().__init__()

        # instructions
        self.instructions_text = None
        self.ui_manager = None

    def on_show_view(self):

        self.ui_manager = UIManager()
        self.ui_manager.enable()

        arcade.set_background_color(arcade.color.AMAZON)

        solitaire_style = {
            "normal": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.BLACK,  # Change font color to contrast with light green background
                bg=(152, 204, 152),  # Soft light green color
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            ),
            "hover": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.BLACK,  # Change font color to contrast with light green background
                bg=(144, 238, 144),  # Light green color on hover
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            ),
            "press": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.BLACK,  # Change font color to contrast with light green background
                bg=(124, 252, 124),  # Even lighter green color when pressed
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            ),
            "disabled": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.LIGHT_GRAY,  # Light gray font color for disabled state
                bg=(152, 204, 152),  # Soft light green color
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            )
        }

        # text objects for instructions
        self.instructions_text = arcade.Text("Solitaire SDG9", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                                             arcade.color.WHITE, font_size=50, anchor_x="center")

        button_width = 200
        button_height = 50

        normal_button = UIFlatButton(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 25,
                                     button_width, button_height, text="Normal", style=solitaire_style)
        normal_button.on_click = self.on_normal_button_click
        self.ui_manager.add(normal_button)

        vegas_button = UIFlatButton(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100,
                                    button_width, button_height, text="Vegas", style=solitaire_style)
        vegas_button.on_click = self.on_vegas_button_click
        self.ui_manager.add(vegas_button)

        draw1_button = UIFlatButton(SCREEN_WIDTH / 2 - 101, SCREEN_HEIGHT / 2 - 175,
                                    button_width / 2, button_height, text="Draw 1", style=solitaire_style)
        draw1_button.on_click = self.on_draw1_button_click
        self.ui_manager.add(draw1_button)

        draw3_button = UIFlatButton(SCREEN_WIDTH / 2 + 1, SCREEN_HEIGHT / 2 - 175,
                                    button_width / 2, button_height, text="Draw 3", style=solitaire_style)
        draw3_button.on_click = self.on_draw3_button_click
        self.ui_manager.add(draw3_button)

    def on_draw(self):
        """ drawing the view """
        self.clear()

        # draw instructions
        self.instructions_text.draw()
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):

        self.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_normal_button_click(self, button):
        solitaire_view = SolitaireGameView()
        solitaire_view.setup()
        self.window.show_view(solitaire_view)

    def on_vegas_button_click(self, button):
        print("Vegas button clicked")

    def on_draw1_button_click(self, button):
        print("Draw 1 button clicked")

    def on_draw3_button_click(self, button):
        print("Draw 3 button clicked")
