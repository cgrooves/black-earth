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

        # Set up players
        self.tanksList = []
        self.activeTank = None
        self.activeTankId = 0

        # TODO: read this in from a config file, or pass in a mapping
        # of players and tanks or something of that sort
        self.tanksList.append(
            Tank(
                Vec2d(SCREEN_WIDTH/3,SCREEN_HEIGHT/3),
                color=arcade.csscolor.DARK_RED
            )
        )
        
        self.tanksList.append(
            Tank(
                Vec2d(SCREEN_WIDTH*2/3, SCREEN_HEIGHT/3),
                color=arcade.csscolor.DARK_BLUE
            )
        )

        # Set the active player
        self.activeTank = self.tanksList[self.activeTankId]

        # Set up other shapes to draw
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

    def on_key_press(self, key, modifiers):
        # Pass through inputs to activeTank
        self.activeTank.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        # Handle window events first
        if key == arcade.key.ESCAPE:
            exit()

        # Pass through inputs to activeTank
        self.activeTank.on_key_release(key, modifiers)

        # Handle space bar
        # I'm putting this code here, after passing the key press and key release
        # onto the active tank, so that the tank can do its own events with the
        # spacebar before we "pass the control"
        if key == arcade.key.SPACE:
            # Wrap around the list if needed
            if self.activeTankId < (len(self.tanksList) - 1):
                self.activeTankId += 1
            else:
                self.activeTankId = 0 # set to beginning if over the edge
            # Actually set the active tank
            self.activeTank = self.tanksList[self.activeTankId]

    def on_update(self, delta_time):
        """ Update game state for game objects """
        self.activeTank.on_update()

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        # Code to draw the screen goes here

        # Render the players
        for player in self.tanksList:
            player.draw()

        # Render the activeTank's tank angle
        arcade.draw_text(
            text=f"Tank Angle: {self.activeTank.turretAngleDeg}",
            start_x =10.0,
            start_y=0.95*SCREEN_HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

        # Draw other shapes
        self.shapes.draw()


def main():
    """ Main method """
    window = BlackEarthGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()