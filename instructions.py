import arcade
from arcade.gui import UIManager, UIFlatButton
from cardgame import *
from constants import *


class InstructionsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.instructions_title = None
        self.instructions_text = None
        self.instructions_background = None
        self.back_button = None

        self.ui_manager = None

    def on_show(self):
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        arcade.set_background_color(arcade.color.AMAZON)

        text = (
            "1. Choose between Normal or Vegas mode.\n\n"
            "2. Normal mode starts at 0, scores 10 points per foundation pile move and 50 for completing.\n\n"
            "3. Vegas mode starts at -52 points and scores 5 per foundation pile.\n\n"
            "4. Vegas mode has a cumulative scoring option and limits on stock pile draws (1 or 3).\n\n"
            "5. Cumulative option continues players points if they restart their game.\n\n"
            "6. Normal mode has no cumulative scoring option and a default draw limit of 100.\n\n"
            "7. Begin with a dealt table and your first move, the timer begins on the first click.\n\n"
            "8. Move cards by descending rank and alternating colors in the tableau piles.\n\n"
            "9. Build foundation piles from Ace to King following suit and ascending order.\n\n"
            "10. Draw from the stock pile with a simple click if needed.\n\n"
            "11. Keep playing until you clear the tableau, filling the foundations or can't make any more moves.\n\n"
            "12. Win by clearing all cards to foundations, lose if you can't move and there are cards left."
        )
        self.instructions_text = UILabel(
            text=text,
            x=SCREEN_WIDTH // 2 - 400,
            y=90,
            text_color=arcade.color.WHITE,
            width=800,
            height=500,
            font_size=14,
            align="center",
            multiline=True
        )
        self.ui_manager.add(self.instructions_text)

        # back display button
        back_button = UIFlatButton(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 50, text="\U0001F519",
                                   style=solitaire_style)
        back_button.on_click = self.on_back_button_click
        self.ui_manager.add(back_button)

    def on_draw(self):
        # draw the pause view
        arcade.start_render()
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_back_button_click(self, button):
        # return to main menu
        from mainMenu import MainMenuView
        self.window.show_view(MainMenuView())
