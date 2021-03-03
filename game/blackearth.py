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

class BlackEarthGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Set up player1
        self.player1 = Tank(
            Vec2d(SCREEN_WIDTH/3,SCREEN_HEIGHT/3),
            color=arcade.csscolor.DARK_RED
            )
        
        self.player2 = Tank(
            Vec2d(SCREEN_WIDTH*2/3, SCREEN_HEIGHT/3),
            color=arcade.csscolor.DARK_BLUE
        )
        self.player2.turretAngleDeg = 90 + 45

    def on_key_press(self, key, modifiers):
        # Pass through inputs to player1
        self.player1.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        # Handle window events first
        if key == arcade.key.ESCAPE:
            exit()

        # Pass through inputs to player1
        self.player1.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        # Update game state for game objects
        self.player1.on_update()
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

        # Render the player1
        self.player1.draw()
        self.player2.draw()

        # Render the player1's tank angle
        arcade.draw_text(
            text=f"Tank Angle: {self.player1.turretAngleDeg}",
            start_x =10.0,
            start_y=0.95*SCREEN_HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )
        self.shapes.draw()


def main():
    """ Main method """
    window = BlackEarthGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()