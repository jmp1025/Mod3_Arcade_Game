import arcade
import random

# img original dimensions: 128 x 128
# new dimensions maintain aspect ratio
IMG_WIDTH = 28
IMG_HEIGHT = 28

SOUND = arcade.load_sound(":resources:sounds/coin2.wav")


class Coin:
    """
    used for creating coin objects
    """

    def __init__(self, s_width, s_height):
        super().__init__()
        #  x and y coordinates are chosen randomly
        #  width and height are controlled by variable main.py
        self.x = random.uniform(0, s_width)  # x axis coordinate
        self.y = random.uniform(0, s_height)  # y axis coordinate

        self.radius = 15  # used for collision detection

    def draw(self):
        """
        draws a coin to the screen
        """
        img = ":resources:images/items/coinGold.png"
        texture = arcade.load_texture(img)
        arcade.draw_texture_rectangle(self.x, self.y, IMG_WIDTH,
                                      IMG_HEIGHT, texture, 0, 255)

    def sound(self):
        """
        plays a coin sound when called
        """
        arcade.play_sound(SOUND)

    def collect(self):
        """
        used for increasing collection value
        """
        return 1
