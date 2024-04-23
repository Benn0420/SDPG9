import arcade
from arcade.gui import UIManager, UIFlatButton
from cardgame import *
from constants import *


class VictoryView(arcade.View):
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
        self.stats_text = None
        self.stats_text_vegas = None
        self.final_points = solitaire_game_view.get_final_points()
        self.final_time = solitaire_game_view.get_final_time()

        # adjusting time display and strings
        minutes, seconds = divmod(self.final_time, 60)
        self.time_str = f"{int(minutes)}:{int(seconds):02d}"
        self.point_str = str(self.final_points)

    def on_show(self):
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # background color and title
        arcade.set_background_color(arcade.color.AMAZON)
        self.title_text = arcade.Text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                                      arcade.color.WHITE, font_size=50, anchor_x="center")
        stats_text_lines = [
            "You completed the game with:",
            f"{self.point_str} points",
            f"in a time of {self.time_str}",
        ]
        stats_text = "\n".join(stats_text_lines)
        # players score and time
        self.stats_text = arcade.Text(stats_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.75,
                                      arcade.color.WHITE, font_size=15, anchor_x="center")

        stats_text_lines_vegas = [
            "You've ran out of draws,",
            f"you have {self.point_str} points",
            f"keep going or cash in?",
        ]
        stats_text_vegas = "\n".join(stats_text_lines_vegas)
        # players score and time
        self.stats_text_vegas = arcade.Text(stats_text_vegas, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.75,
                                      arcade.color.WHITE, font_size=15, anchor_x="center")

        if self.vegas_cumulative:
            self.vegas_buttons()
        else:
            self.standard_buttons()

    def standard_buttons(self):
        # restart button
        restart_button = UIFlatButton(BUTTON_X, BUTTON2_Y, BUTTON_W, BUTTON_H, text="Restart", style=solitaire_style)
        restart_button.on_click = self.on_restart_button_click
        self.ui_manager.add(restart_button)

        # menu button
        menu_button = UIFlatButton(BUTTON_X, BUTTON3_Y, BUTTON_W, BUTTON_H, text="Main Menu", style=solitaire_style)
        menu_button.on_click = self.on_menu_button_click
        self.ui_manager.add(menu_button)

    def vegas_buttons(self):
        # continue button
        continue_button = UIFlatButton(BUTTON_X, BUTTON2_Y, BUTTON_W, BUTTON_H, text="Keep Going", style=solitaire_style)
        continue_button.on_click = self.on_restart_button_click
        self.ui_manager.add(continue_button)

        # cashin button
        cashin_button = UIFlatButton(BUTTON_X, BUTTON3_Y, BUTTON_W, BUTTON_H, text="Cash In!", style=solitaire_style)
        cashin_button.on_click = self.on_menu_button_click
        self.ui_manager.add(cashin_button)

    def on_draw(self):
        # draw the victory view
        arcade.start_render()
        self.title_text.draw()
        if self.vegas_cumulative:
            self.stats_text_vegas.draw()
        else:
            self.stats_text.draw()
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_restart_button_click(self, button):
        # restart the game with current rules
        from cardgame import SolitaireGameView
        solitaire_view = SolitaireGameView(
            draw_mode=self.solitaire_game_view.draw_mode,
            game_mode=self.solitaire_game_view.game_mode,
            vegas_cumulative=self.solitaire_game_view.vegas_cumulative,
            points=self.solitaire_game_view.points
        )
        solitaire_view.setup()
        self.window.show_view(solitaire_view)

    def on_menu_button_click(self, button):
        # return to main menu
        from mainMenu import MainMenuView
        self.window.show_view(MainMenuView())
