import arcade
from game import MyGame


# window dimensions
# MUST be in multiples of 50
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700


def main():
    """
    simple function to run MyGame()
    """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.draw_begin()
    arcade.run()


if __name__ == "__main__":
    main()
