import arcade
from timer import Timer
from player import Player
from coin import Coin
from block import Block

"""
in game views
"""
GAME_START = 1
GAME_PLAY = 2
GAME_OVER = 3
GAME_WIN = 4

BLOCK_SIDE = 50  # block square dimension


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.game = GAME_START
        self.width = width  # controlled by variable in main.py
        self.height = height  # controlled by variable in main.py

        # list of 3 coins
        self.coins = [Coin(width, height),
                      Coin(width, height),
                      Coin(width, height)]

        # list of black blocks
        # will always cover entire screen
        self.blocks = []
        for row in range(int(self.height/BLOCK_SIDE)):
            for column in range(int(self.width/BLOCK_SIDE)):
                x = column * BLOCK_SIDE + (BLOCK_SIDE/2)
                y = row * BLOCK_SIDE + (BLOCK_SIDE/2)
                block = Block(x, y, BLOCK_SIDE, BLOCK_SIDE)
                self.blocks.append(block)

        self.player = Player()
        self.held_keys = set()
        self.timer = Timer()
        self.score = 0

    def new_game(self):
        """
        repopulate objects and lists if player wants to play again
        """
        self.timer = Timer()
        self.player = Player()
        self.coins = [Coin(self.width, self.height),
                      Coin(self.width, self.height),
                      Coin(self.width, self.height)]
        self.blocks = []
        for row in range(int(self.height/BLOCK_SIDE)):
            for column in range(int(self.width/BLOCK_SIDE)):
                x = column * BLOCK_SIDE + (BLOCK_SIDE/2)
                y = row * BLOCK_SIDE + (BLOCK_SIDE/2)
                block = Block(x, y, BLOCK_SIDE, BLOCK_SIDE)
                self.blocks.append(block)
        self.score = 0
        self.game = GAME_PLAY

    def draw_begin(self):
        """
        draw a start screen before game play
        """
        arcade.draw_text("Find 3 Coins!", 0,
                         self.height//1.8, arcade.color.BLACK, 24,
                         self.width, "center")
        arcade.draw_text("Press \"Enter\" To Play \n\nPress \"Q\" To Quit", 0,
                         self.height//2.6, arcade.color.BLACK, 18,
                         self.width, "center")
        arcade.draw_text("Use the Up, Down, Left and Right arrow keys for"
                         " controls", 0, self.height//3.4, arcade.color.BLACK,
                         18, self.width, "center")

    def draw_end(self, status):
        """
        end screen dependent on win or lose status
        """
        if status == GAME_WIN:
            arcade.draw_text("You Won!", 0,
                             self.height//1.8, arcade.color.BLACK, 24,
                             self.width, "center")
            arcade.draw_text("Press \"Enter\" To Play Again"
                             "\n\nPress \"Q\" To Quit", 0, self.height//2.6,
                             arcade.color.BLACK, 18, self.width, "center")

        elif status == GAME_OVER:
            arcade.draw_text("Oh No!  You Lost", 0,
                             self.height//1.8, arcade.color.BLACK, 24,
                             self.width, "center")
            arcade.draw_text("Press \"Enter\" To Play Again"
                             "\n\nPress \"Q\" To Quit",
                             0, self.height//2.6, arcade.color.BLACK, 18,
                             self.width, "center")

    def on_draw(self):
        """
        Use this function to draw everything to the screen.
        """

        # Start the render. This must happen before any drawing
        # commands. We do NOT need an stop render command.
        arcade.start_render()

        arcade.set_background_color(arcade.color.SAND)

        # the game views will decide what is drawn
        if self.game == GAME_START:
            self.draw_begin()
        elif not self.timer.alive:
            self.game = GAME_OVER
            self.draw_end(self.game)
        elif not self.coins:
            self.game = GAME_WIN
            self.draw_end(self.game)
        elif self.game == GAME_PLAY:
            self.player.draw()
            for coin in self.coins:
                coin.draw()
            for block in self.blocks:
                block.draw()
            self.timer.draw(self.height)
            score = f"Coins: {self.score}/3"
            arcade.draw_text(score, self.width - 110, self.height - 30,
                             arcade.color.RED, 20)

    def on_update(self, delta_time):
        """
        Use this function to update in game changes to screen
        """
        self.check_keys()
        if self.game == GAME_PLAY:
            self.timer.countdown(delta_time)
            self.check_collisions()

    def check_collisions(self):
        """
        Use this function to check for collisions with the player image
        """
        # checks collisions with coins
        for coin in self.coins:
            if self.player.alive and coin.alive:
                too_close = self.player.radius + coin.radius
                if (abs(self.player.x - coin.x) < too_close and
                        abs(self.player.y - coin.y) < too_close):
                    coin.sound()
                    self.score += coin.collect()  # updates collection
                    self.coins.remove(coin)  # removes the coin upon collision

        # checks for collisions with the black blocks
        for block in self.blocks:
            if self.player.alive and block.alive:
                too_close = self.player.radius + block.radius
                if (abs(self.player.x - block.x) < too_close and
                        abs(self.player.y - block.y) < too_close):
                    self.blocks.remove(block)  # removes block upon collision

    def check_keys(self):
        """
        Use this function to setup key controls for keys that are held down.
        """
        if arcade.key.UP in self.held_keys:
            self.player.move_up(self.height)

        if arcade.key.DOWN in self.held_keys:
            self.player.move_down()

        if arcade.key.LEFT in self.held_keys:
            self.player.move_left()

        if arcade.key.RIGHT in self.held_keys:
            self.player.move_right(self.width)

    def on_key_press(self, key: int, modifiers: int):
        """
        Use this function to setup key control that won't be held down
        """
        self.held_keys.add(key)

        # statement for game view conrols
        if key == arcade.key.ENTER and self.game == GAME_START:
            self.game = GAME_PLAY
        elif key == arcade.key.ENTER and self.game == GAME_OVER:
            self.new_game()
        elif key == arcade.key.ENTER and self.game == GAME_WIN:
            self.new_game()

        #  pressing Q will end the game and close the window
        if key == arcade.key.Q:
            quit()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
