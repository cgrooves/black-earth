"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

class Ground():

    def __init__(self, parent: arcade.Window):
        """
        Class encapsulating the ground
        """
        self.parent = parent
    
    def render(self):
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6,
            SCREEN_WIDTH, SCREEN_HEIGHT / 3,
            arcade.color.DARK_SPRING_GREEN
        )


class BlackEarthGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.ground = Ground(self)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        self.ground.render()


def main():
    """ Main method """
    window = BlackEarthGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()