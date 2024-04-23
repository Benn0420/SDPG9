import arcade
from arcade.gui import UIManager, UIFlatButton, UITextArea, UILabel
from cardgame import *
from constants import *


class MainMenuView(arcade.View):
    """ View to hold main Menu """

    def __init__(self):
        super().__init__()

        # title and buttons
        self.title_text = None
        self.ui_manager = None

        self.draw_mode = "1"
        self.game_mode = "N"
        self.vegas_cumulative = False
        self.checkbox_label = None
        self.show_instructions = False
        self.v_points = -52

    def on_show_view(self):

        self.ui_manager = UIManager()
        self.ui_manager.enable()

        arcade.set_background_color(arcade.color.AMAZON)

        # title
        self.title_text = arcade.Text("Solitaire SDG9", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,
                                      arcade.color.WHITE, font_size=50, anchor_x="center")
        # normal game mode
        normal_button = UIFlatButton(BUTTON_X, BUTTON1_Y, BUTTON_W, BUTTON_H, text="Normal", style=solitaire_style)
        normal_button.on_click = self.on_normal_button_click
        self.ui_manager.add(normal_button)
        # vegas game mode
        vegas_button = UIFlatButton(BUTTON_X, BUTTON2_Y, BUTTON_W, BUTTON_H, text="Vegas", style=solitaire_style)
        vegas_button.on_click = self.on_vegas_button_click
        self.ui_manager.add(vegas_button)
        # instructions display button
        instruction_button = UIFlatButton(BUTTON_X, BUTTON4_Y, BUTTON_W, BUTTON_H, text="Instructions",
                                          style=solitaire_style)
        instruction_button.on_click = self.on_instruction_button_click
        self.ui_manager.add(instruction_button)
        # cumulative and draw button call
        self.create_cumulative_choice()
        self.create_draw_buttons()

    def create_cumulative_choice(self):
        # vegas cumulative option
        self.checkbox_label = arcade.Text("Enable Cumulative?", BUTTON_X + 210, BUTTON2_Y + 40,
                                          (152, 204, 152), font_size=12)
        cumulative_button = UIFlatButton(BUTTON_X + 260, BUTTON2_Y + 5, 25, 25,
                                         text=self.get_cumulative_button_choice(), style=solitaire_style)
        cumulative_button.on_click = self.on_cumulative_button_click
        self.ui_manager.add(cumulative_button)

    def create_draw_buttons(self):
        # draw 1 or 3 toggle buttons
        draw1_button = UIFlatButton(BUTTON_X - 1, BUTTON3_Y, BUTTON_W / 2, BUTTON_H,
                                    text=self.get_draw1_button_text(), style=solitaire_style)
        draw1_button.on_click = self.on_draw1_button_click
        self.ui_manager.add(draw1_button)

        draw3_button = UIFlatButton(BUTTON_X + 101, BUTTON3_Y, BUTTON_W / 2, BUTTON_H,
                                    text=self.get_draw3_button_text(), style=solitaire_style)
        draw3_button.on_click = self.on_draw3_button_click
        self.ui_manager.add(draw3_button)

    def on_draw(self):
        """ drawing the view """
        self.clear()
        self.title_text.draw()
        self.checkbox_label.draw()
        # ui elements
        self.ui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.ui_manager.on_mouse_press(x, y, button, modifiers)

    def on_normal_button_click(self, button):
        # load game with normal setting
        self.game_mode = "N"
        self.draw_mode = "100"
        self.vegas_cumulative = False
        from cardgame import SolitaireGameView
        solitaire_view = SolitaireGameView(self.draw_mode, self.game_mode, self.vegas_cumulative)
        solitaire_view.setup()
        self.window.show_view(solitaire_view)

    def on_vegas_button_click(self, button):
        self.game_mode = "V"
        # load game with vegas setting
        from cardgame import SolitaireGameView
        solitaire_view = SolitaireGameView(self.draw_mode, self.game_mode, self.vegas_cumulative, self.v_points)
        solitaire_view.setup()
        self.window.show_view(solitaire_view)

    def on_cumulative_button_click(self, button):
        # toggle vegas cumulative choice (vegas only)
        if self.vegas_cumulative:
            self.vegas_cumulative = False
        else:
            self.vegas_cumulative = True
        self.update_vegas_cumulative_choice()

    def get_cumulative_button_choice(self):
        return "\U00002713" if self.vegas_cumulative is True else ""

    def update_vegas_cumulative_choice(self):
        # remove existing buttons
        self.ui_manager.remove("cumulative_button")
        # create and add updated buttons
        self.create_cumulative_choice()

    def on_draw1_button_click(self, button):
        self.draw_mode = "1"
        self.update_button_text()

    def on_draw3_button_click(self, button):
        self.draw_mode = "3"
        self.update_button_text()

    def get_draw1_button_text(self):
        return "Draw 1" if self.draw_mode == "1" else ""

    def get_draw3_button_text(self):
        return "Draw 3" if self.draw_mode == "3" else ""

    def update_button_text(self):
        # remove existing buttons
        self.ui_manager.remove("draw1_button")
        self.ui_manager.remove("draw3_button")
        # create and add updated buttons
        self.create_draw_buttons()

    def on_instruction_button_click(self, button):
        # return to main menu
        from instructions import InstructionsView
        self.window.show_view(InstructionsView())
