import arcade

# screen title and size

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "SOLITAIRE"


class SolitaireGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """Set up the game"""
        pass

    def on_draw(self):
        """Render the screen"""
        self.clear()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """for mouse press"""
        pass

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """for mouse release"""
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """moving the mouse"""
        pass


def main():
    """main function"""
    window = SolitaireGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
