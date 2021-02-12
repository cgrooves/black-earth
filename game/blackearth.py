"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""
import arcade
from pymunk import Vec2d

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"


class Tank:

    def __init__(self, color: arcade.color):
        self.size = 50
        self.position = Vec2d(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.color = color
        self.turretAngleDeg = 90
        self.turretLength = 50
    
    def changeTurretAngle(self, amount):

        self.turretAngleDeg += amount
        if self.turretAngleDeg > 180:
            self.turretAngleDeg = 180
        elif self.turretAngleDeg < 0:
            self.turretAngleDeg = 0

    def draw(self):
        arcade.draw_arc_filled(
            center_x=self.position.x,
            center_y=self.position.y,
            width=self.size,
            height=self.size,
            color=self.color,
            start_angle=0.0,
            end_angle=180
        )

        # Calculate turret end point
        turretPosition = Vec2d(self.turretLength, 0)
        turretPosition.rotate_degrees(self.turretAngleDeg)

        arcade.draw_line(
            start_x=self.position.x,
            start_y=self.position.y,
            end_x=turretPosition.x + self.position.x,
            end_y=turretPosition.y + self.position.y,
            color=self.color,
            line_width=2.0
        )


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player = Tank(arcade.csscolor.DARK_RED)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        # Create the player
        self.player.draw()

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.LEFT:
            self.player.changeTurretAngle(-1)
        elif key == arcade.key.RIGHT:
            self.player.changeTurretAngle(1)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()