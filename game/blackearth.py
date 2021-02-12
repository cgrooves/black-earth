"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

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
        self.shapes = arcade.ShapeElementList()
        
        # Create the ground
        ground = arcade.create_rectangle_filled(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 6,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT / 3,
            color=arcade.color.DARK_SPRING_GREEN
        )
        self.shapes.append(ground)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        self.shapes.draw()


def main():
    """ Main method """
    window = BlackEarthGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()