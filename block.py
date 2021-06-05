import arcade


class Block:
    """
    simple object used for hiding things behind
    """

    def __init__(self, x, y, w, h):
        super().__init__()
        # attributes for cooridnate location
        self.x = x  # x axis coordinate
        self.y = y  # y axis coordinate

        self.width = w  # controlled by variable in game.py
        self.height = h  # controlled by variable in game.py
        self.radius = 50  # used for collision detection

    def draw(self):
        """
        draws a black square to the screen
        """
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     arcade.color.BLACK)
