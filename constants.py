"""Game constants"""
import arcade
from arcade.gui import UIFlatButton

# screen title and size
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
SCREEN_TITLE = "SOLITAIRE"

PAUSE_X = SCREEN_WIDTH - 100
PAUSE_Y = SCREEN_HEIGHT - 50

POINTS_X = SCREEN_WIDTH - 300
POINTS_Y = 100

TIMER_X = SCREEN_WIDTH - 300
TIMER_Y = 50

BUTTON_X = SCREEN_WIDTH / 2 - 100
BUTTON1_Y = SCREEN_HEIGHT / 2 - 25
BUTTON2_Y = SCREEN_HEIGHT / 2 - 100
BUTTON3_Y = SCREEN_HEIGHT / 2 - 175
BUTTON4_Y = SCREEN_HEIGHT / 2 - 250
BUTTON_W = 200
BUTTON_H = 50

CARD_SCALE = 0.6

CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

MAT_PERCENT_OVERSIZE = 1.2
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Pile constants, may change later
PILE_COUNT = 13
STOCK = 0
TALON = 1

TABLEAU_1 = 2
TABLEAU_2 = 3
TABLEAU_3 = 4
TABLEAU_4 = 5
TABLEAU_5 = 6
TABLEAU_6 = 7
TABLEAU_7 = 8

FOUNDATION_1 = 9
FOUNDATION_2 = 10
FOUNDATION_3 = 11
FOUNDATION_4 = 12

# Button style
solitaire_style = {
            "normal": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.AMAZON,  # Change font color to contrast with light green background
                bg=(152, 204, 152),  # Soft light green color
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            ),
            "hover": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.AMAZON,  # Change font color to contrast with light green background
                bg=(144, 238, 144),  # Light green color on hover
                border=(120, 180, 120),  # Lighter green border color
                border_width=2,
            ),
            "press": UIFlatButton.UIStyle(
                font_size=14,
                font_name=("Arial", "Calibri"),
                font_color=arcade.color.AMAZON,  # Change font color to contrast with light green background
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
