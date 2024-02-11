import arcade

from Cards import Card
from constants import CARD_SUITS, CARD_VALUES, CARD_SCALE, START_X, BOTTOM_Y

# screen title and size

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "SOLITAIRE"


class SolitaireGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON)

        # list of cards to drag with mouse
        self.held_cards = None

        # drag from/snap back location
        self.held_cards_original_location = None

    def setup(self):
        """Set up the game"""

        # handle held cards:
        self.held_cards = []

        self.held_cards_original_location = []

        # list of all the cards
        self.card_list = arcade.SpriteList()

        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)

    def on_draw(self):
        """Render the screen"""
        # clear screen
        self.clear()

        # draw cards
        self.card_list.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """for mouse press"""

        # get list of cards clicked
        cards = arcade.get_sprites_at_point((x,y), self.card_list)

        # check if card has been clicked on
        if len(cards) > 0:
            # top of stack only
            primary_card = cards[-1]

            self.held_cards = [primary_card]
            # set position
            self.held_cards_original_location = [self.held_cards[0].position]
            # put it on top
            self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """for mouse release"""

        # no cards
        if len(self.held_cards) == 0:
            return

        # release cards
        self.held_cards = []


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """moving the mouse"""

        # move cards with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def pull_to_top(self, card: arcade.Sprite):
        """Pull the cards to the top of the rendering order"""

        # put the card you are selecting on top of rendering
        self.card_list.remove(card)
        self.card_list.append(card)


def main():
    """main function"""
    window = SolitaireGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
