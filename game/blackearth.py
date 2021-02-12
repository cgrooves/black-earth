"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""
import arcade
from pymunk import Vec2d

from tank import Tank

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Black Earth"


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

        # Set up player
        self.player = Tank(
            Vec2d(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),
            color=arcade.csscolor.DARK_RED
            )

    def on_key_press(self, key, modifiers):
        # Pass through inputs to player
        self.player.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        # Handle window events first
        if key == arcade.key.ESCAPE:
            exit()

        # Pass through inputs to player
        self.player.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        # Update game state for game objects
        self.player.on_update()

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        # Render the player
        self.player.draw()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()