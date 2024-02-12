import arcade

from Cards import Card
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                       CARD_SUITS, CARD_VALUES, CARD_SCALE, START_X,
                       BOTTOM_Y, MAT_WIDTH, MAT_HEIGHT, X_SPACING, MIDDLE_Y, TOP_Y)


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

        # mats
        self.pile_mat_list = None

    def setup(self):
        """Set up the game"""

        # handle held cards:
        self.held_cards = []

        self.held_cards_original_location = []

        # Create mats
        # sprite list of mats
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color=arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color=arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # tableau
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color=arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # foundations
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, color=arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

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

        # draw the mats
        self.pile_mat_list.draw()

        # draw cards
        self.card_list.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """for mouse press"""

        # get list of cards clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

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

        # if close to more than one pile, snap to closest
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # check for contact
        if arcade.check_for_collision(self.held_cards[0], pile):

            # move dropped card(s) to pile
            for i, dropped_card in enumerate(self.held_cards):
                dropped_card.position = pile.center_x, pile.center_y

            # cards snapped, don't reset
            reset_position = False

        # return cards to original position if snap is invalid
        if reset_position:
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_location[pile_index]

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
