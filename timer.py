import arcade


class Timer:
    """
    countdown timer for game challenge
    """

    def __init__(self):
        super().__init__()
        self.total_time = 30.0
        self.minutes = 0
        self.seconds = 0
        self.alive = True

    def calc_minutes(self):
        """
        calculates when to change minutes 1 - 60
        """
        minutes = int(self.total_time) // 60
        return minutes

    def calc_seconds(self):
        """
        calculates when to change seconds 1 - 60
        """
        seconds = int(self.total_time) % 60
        return seconds

    def countdown(self, time):
        """
        countdown will stop at 00:00
        """
        if self.total_time > 0.0:
            self.total_time -= time
        else:
            self.alive = False

    def draw(self, h):
        """
        draws the coundown to the top left corner of the screen
        """
        output = f"Time: {self.calc_minutes():02d}:{self.calc_seconds():02d}"
        arcade.draw_text(output, 10, h - 30, arcade.color.RED, 20)
