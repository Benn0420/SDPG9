import arcade
from arcade.gui import UIManager, UIFlatButton
from cardgame import *
from constants import *


class PauseView(arcade.View):
    def __init__(self, solitaire_game_view, draw_mode="1", game_mode="N", vegas_cumulative=False, points=0):
        super().__init__()
        self.solitaire_game_view = solitaire_game_view
        self.draw_mode = draw_mode
        self.game_mode = game_mode
        self.vegas_cumulative = vegas_cumulative
        if self.vegas_cumulative:
            self.points = points
        else:
            self.points = 0
        self.ui_manager = None
        self.title_text = None

    def on_show(self):
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # background color and title
        arcade.set_background_color(arcade.color.AMAZON)
        self.title_text = arcade.Text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                                      arcade.color.WHITE, font_size=50, anchor_x="center")

        # resume button
        resume_button = UIFlatButton(BUTTON_X, BUTTON1_Y, BUTTON_W, BUTTON_H, text="Resume", style=solitaire_style)
        resume_button.on_click = self.on_resume_button_click
        self.ui_manager.add(resume_button)

        # restart button
        restart_button = UIFlatButton(BUTTON_X, BUTTON2_Y, BUTTON_W, BUTTON_H, text="Restart", style=solitaire_style)
        restart_button.on_click = self.on_restart_button_click
        self.ui_manager.add(restart_button)

        # quit button
        quit_button = UIFlatButton(BUTTON_X, BUTTON3_Y, BUTTON_W, BUTTON_H, text="Quit", style=solitaire_style)
        quit_button.on_click = self.on_quit_button_click
        self.ui_manager.add(quit_button)

    def on_draw(self):
        # draw the pause view
        arcade.start_render()
        self.title_text.draw()
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_resume_button_click(self, button):
        # resume the game
        self.window.show_view(self.solitaire_game_view)

    def on_restart_button_click(self, button):
        # restart the game with current rules
        from cardgame import SolitaireGameView
        solitaire_view = SolitaireGameView(
            draw_mode=self.solitaire_game_view.draw_mode,
            game_mode=self.solitaire_game_view.game_mode,
            vegas_cumulative=self.solitaire_game_view.vegas_cumulative,
            points = self.solitaire_game_view.points
        )
        solitaire_view.setup()
        self.window.show_view(solitaire_view)

    def on_quit_button_click(self, button):
        # return to main menu
        from mainMenu import MainMenuView
        self.window.show_view(MainMenuView())
