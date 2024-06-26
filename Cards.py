import arcade


class Card(arcade.Sprite):
    """Card sprite, card image"""

    def __init__(self, suit, value, scale=1):
        """card constructor"""

        self.suit = suit
        self.value = value

        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

