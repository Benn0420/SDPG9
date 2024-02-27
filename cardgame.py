import arcade
import random
from Cards import Card
from constants import *


# (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
#                        CARD_SUITS, CARD_VALUES, CARD_SCALE, START_X,
#                        BOTTOM_Y, MAT_WIDTH, MAT_HEIGHT, X_SPACING, MIDDLE_Y, TOP_Y)

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

        # piles
        self.piles = None

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

        # Shuffle cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Create piles
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Put all cards in the stock
        for card in self.card_list:
            self.piles[STOCK].append(card)

        # pull from stock and deal into tableau
        for pile_no in range(TABLEAU_1, TABLEAU_7 + 1):
            for j in range(pile_no - TABLEAU_1 + 1):
                # pop each card from the stock
                card = self.piles[STOCK].pop()
                # add the card to the pile we are on
                self.piles[pile_no].append(card)
                # position
                card.position = self.pile_mat_list[pile_no].position
                # draw on top
                self.pull_to_top(card)

        # flip over tableau cards
        for i in range(TABLEAU_1, TABLEAU_7 + 1):
            self.piles[i][-1].face_up()

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

            # what pile is the card in?
            pile_index = self.get_pile_of_card(primary_card)

            if primary_card.is_face_down:
                primary_card.face_up()
            else:
                # get card being clicked
                self.held_cards = [primary_card]
                # set position
                self.held_cards_original_location = [self.held_cards[0].position]
                # put it on top
                self.pull_to_top(self.held_cards[0])

                # handle stack of cards
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card = self.piles[pile_index][i]
                    self.held_cards.append(card)
                    self.held_cards_original_location.append(card.position)
                    self.pull_to_top(card)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """for mouse release"""

        # no cards
        if len(self.held_cards) == 0:
            return

        # if close to more than one pile, snap to closest
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # check for contact
        if arcade.check_for_collision(self.held_cards[0], pile):
            # which pile?
            pile_index = self.pile_mat_list.index(pile)
            print(pile_index)

            # dropped in the same pile
            if pile_index == self.get_pile_of_card(self.held_cards[0]):
                print("index = pile, pass")
                pass

            elif TABLEAU_1 <= pile_index <= TABLEAU_7:
                # check if empty
                if len(self.piles[pile_index]) == 0:
                    # no cards in tableau pile
                    if self.held_cards[0].value == "K":
                        print("no cards in pile")
                        for i, dropped_card in enumerate(self.held_cards):
                            # Move cards to proper position
                            dropped_card.position = pile.center_x, \
                                pile.center_y - CARD_VERTICAL_OFFSET * i

                        # assign card to correct pile list
                        for card in self.held_cards:
                            self.move_card_to_pile(card, pile_index)
                        reset_position = False
                    else:
                        print("Invalid move: Table piles must start with a King")

                else:
                    # pile is not empty, read top card
                    top_card = self.piles[pile_index][-1]
                    # check for alternating colors
                    if self.is_alternating_color(top_card, self.held_cards[0]):
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = top_card.center_x, \
                                top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                        # assign card to correct pile list
                        for card in self.held_cards:
                            self.move_card_to_pile(card, pile_index)
                        reset_position = False
                    else:
                        print("Invalid move: Cards must be alternating in color")

            # if trying to add to foundation, only one card can be added at a time
            elif FOUNDATION_1 <= pile_index <= FOUNDATION_4 and len(self.held_cards) == 1:
                # if empty, only allow an ace
                if len(self.piles[pile_index]) == 0:
                    if self.held_cards[0].value == "A":
                        self.held_cards[0].position = pile.position
                        self.move_card_to_pile(self.held_cards[0], pile_index)
                        reset_position = False
                    else:
                        print("Can only start foundation with Ace")
                else:
                    # check if card being adding follows the foundation rules
                    top_card = self.piles[pile_index][-1]
                    if self.held_cards[0].suit == top_card.suit:
                        if CARD_VALUES.index(self.held_cards[0].value) - CARD_VALUES.index(top_card.value) == 1:
                            self.held_cards[0].position = pile.position
                            self.move_card_to_pile(self.held_cards[0], pile_index)
                            reset_position = False
                    else:
                        print("Invalid move for foundation pile")

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

    def get_pile_of_card(self, card):
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def remove_card_from_pile(self, card):
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def move_card_to_pile(self, card, pile_index):
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    @staticmethod
    def is_alternating_color(card1, card2):
        red_suits = ["Hearts", "Diamonds"]
        black_suits = ["Spades", "Clubs"]

        # checks if one card is red and the other is black
        if (card1.suit in red_suits and card2.suit in black_suits) or \
                (card1.suit in black_suits and card2.suit in red_suits):
            return True
        else:
            return False


def main():
    """main function"""
    window = SolitaireGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
