import arcade
import random
from mainMenu import *
from Cards import Card
from constants import *
from firework import *
from pauseMenu import *
from victory import *
from arcade.gui import UIManager, UIFlatButton


# (SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
#                        CARD_SUITS, CARD_VALUES, CARD_SCALE, START_X,
#                        BOTTOM_Y, MAT_WIDTH, MAT_HEIGHT, X_SPACING, MIDDLE_Y, TOP_Y)


class SolitaireGameView(arcade.View):
    """Main application class."""

    def __init__(self, draw_mode="1", game_mode="N", vegas_cumulative=False, points=0):
        super().__init__()
        self.draw_mode = draw_mode
        self.game_mode = game_mode
        self.vegas_cumulative = vegas_cumulative

        self.card_list = None
        self.ui_manager = None

        arcade.set_background_color(arcade.color.AMAZON)

        # list of cards to drag with mouse
        self.held_cards = None

        # drag from/snap back location
        self.held_cards_original_location = None

        # mats
        self.pile_mat_list = None

        # piles
        self.piles = None

        # stockpile run through counter
        self.shuffling = False
        self.shuffle_through = 0
        self.shuffled_through = False
        self.shuffle_limit = self.draw_mode
        self.tracked_card_value = 0
        self.tracked_card_suit = None

        # scoring
        if self.game_mode == "V":
            self.points = -52
        if self.game_mode == "N":
            self.points = 0
        if self.vegas_cumulative:
            self.points = points

        self.points_text = None

        # timing
        self.game_underway = False
        self.total_time = 0.0
        self.timer_text = None

        # game finished
        self.finished_foundations = 0
        self.game_finished = False

        # game won
        self.fireworks_list = []
        self.is_fireworks_active = False
        self.number_of_fireworks = 0

    def setup(self):
        """Set up the game"""

        # pause button
        self.ui_manager = UIManager()
        self.ui_manager.enable()
        pause_button = UIFlatButton(PAUSE_X, PAUSE_Y, 75, 30, text="PAUSE", style=solitaire_style)
        pause_button.on_click = self.on_pause_button_click
        self.ui_manager.add(pause_button)

        # text object for point scoring
        self.points_text = arcade.Text(f"Points: {self.points}", POINTS_X, POINTS_Y,
                                       arcade.csscolor.LIGHT_GREEN, 40, bold=True)

        # text object for timer
        self.timer_text = arcade.Text("Time: 00:00", TIMER_X, TIMER_Y,
                                      arcade.csscolor.LIGHT_GREEN, 40, bold=True)

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

        # draw points
        self.points_text.draw()

        # draw timer
        self.timer_text.draw()

        # draw pause button
        self.ui_manager.draw()

        # draw fireworks if they're active
        if self.is_fireworks_active:
            for firework in self.fireworks_list:
                firework.draw()

    def on_update(self, delta_time):
        # if the gameplay screen has been clicked
        if self.game_underway:
            self.total_time += delta_time
            # update timer text
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            self.timer_text.text = f"Time: {minutes:02d}:{seconds:02d}"
        # if fireworks are active
        if self.is_fireworks_active:
            for firework in self.fireworks_list:
                firework.update(delta_time)
                if firework.is_exploded:
                    self.fireworks_list.remove(firework)
            # if fireworks have all exploded
            if len(self.fireworks_list) == 0:
                self.is_fireworks_active = False
                self.game_over()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """for mouse press"""

        self.game_underway = True

        # get list of cards clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # check if card has been clicked on
        if len(cards) > 0:
            # top of stack only
            primary_card = cards[-1]
            # what pile is the card in?
            pile_index = self.get_pile_of_card(primary_card)

            if self.shuffled_through:
                self.tracked_card_value = 0
                self.tracked_card_suit = None
                self.shuffling = False
                self.shuffled_through = False

            # if it's the stockpile
            if pile_index == STOCK:
                if self.shuffling:
                    # if stockpile has been shuffled through
                    if primary_card.value == self.tracked_card_value and primary_card.suit == self.tracked_card_suit:
                        self.shuffle_through += 1
                        # if shuffle limit has been reached
                        if str(self.shuffle_through) == self.shuffle_limit:
                            # TESTING PURPOSES ONLY
                            # self.game_winner()
                            self.game_over()
                        self.shuffled_through = True
                if primary_card.is_face_down:
                    # flip the card face up
                    primary_card.face_up()

                # see if there is a card in the talon pile
                if self.piles[TALON]:
                    # card in talon pile goes to the bottom of the stock
                    card_in_talon = self.piles[TALON].pop(0)
                    if not self.shuffling:
                        self.shuffling = True
                        self.tracked_card_value = card_in_talon.value
                        self.tracked_card_suit = card_in_talon.suit
                    card_in_talon.face_down()
                    self.move_card_to_pile(card_in_talon, 0)
                    self.push_to_back(card_in_talon)
                    card_in_talon.position = self.pile_mat_list[STOCK].position
                # move the card to the talon pile
                primary_card.position = self.pile_mat_list[TALON].position
                self.move_card_to_pile(primary_card, TALON)
            # if it's any other pile
            else:
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
                pass

            elif TABLEAU_1 <= pile_index <= TABLEAU_7:
                # check if empty
                if len(self.piles[pile_index]) == 0:
                    # check if it's a King
                    if self.held_cards[0].value == "K":
                        # Move cards to proper position
                        for i, dropped_card in enumerate(self.held_cards):
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
                    print("held card value" + str(CARD_VALUES.index(self.held_cards[0].value)))
                    print("top card value" + str(CARD_VALUES.index(top_card.value)))
                    if CARD_VALUES.index(self.held_cards[0].value) - CARD_VALUES.index(top_card.value) == -1:
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
                    else:
                        print("Invalid move: Cards must be descending in order")

            # if trying to add to foundation, only one card can be added at a time
            elif FOUNDATION_1 <= pile_index <= FOUNDATION_4 and len(self.held_cards) == 1:
                # if empty, only allow an ace
                if len(self.piles[pile_index]) == 0:
                    if self.held_cards[0].value == "A":
                        self.held_cards[0].position = pile.position
                        self.move_card_to_pile(self.held_cards[0], pile_index)
                        if self.game_mode == "V":
                            self.increase_points(5)
                        if self.game_mode == "N":
                            self.increase_points(10)
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
                            if self.game_mode == "V":
                                self.increase_points(5)
                            if self.game_mode == "N":
                                self.increase_points(10)
                            reset_position = False
                            # check if card completes foundation stacking
                            if self.held_cards[0].value == "K":
                                self.finished_foundations += 1
                                if self.game_mode == "N":
                                    self.increase_points(50)
                                # call game winner function if all foundations finished
                                if self.finished_foundations == 4:
                                    self.game_underway = False
                                    self.game_winner()
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

    def push_to_back(self, card: arcade.Sprite):
        """Push the cards to the bottom of the rendering order"""

        # put the card you are selecting to the bottom of rendering
        self.card_list.remove(card)
        self.card_list.insert(0, card)

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

    def increase_points(self, amount):
        self.points += amount
        self.points_text.text = f"Points: {self.points}"

    def on_pause_button_click(self, button):
        pause_view = PauseView(self, self.draw_mode, self.game_mode, self.vegas_cumulative, self.points)
        self.window.show_view(pause_view)

    def game_winner(self):
        self.game_underway = False
        self.game_finished = True
        self.trigger_fireworks()

    def trigger_fireworks(self):
        # set number of fireworks
        self.number_of_fireworks = self.points + 250
        # initializing fireworks for celebration
        self.fireworks_list = []
        for _ in range(self.number_of_fireworks):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
            firework = Firework(x, y, color)
            self.fireworks_list.append(firework)
        # setting fireworks to active
        self.is_fireworks_active = True

    def get_final_points(self):
        return self.points

    def get_final_time(self):
        return self.total_time

    def game_over(self):
        self.game_underway = False
        self.game_finished = True
        victory_view = VictoryView(self, self.draw_mode, self.game_mode, self.vegas_cumulative, self.points)
        self.window.show_view(victory_view)


def main():
    """main function"""

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    from mainMenu import MainMenuView
    start_view = MainMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
