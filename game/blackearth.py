"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""
from itertools import cycle

import arcade
from pymunk import Vec2d

from tank import Tank, TANK_COLORS

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Black Earth"

class BlackEarthGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """Constructor"""

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self, num_tanks=2):
        """ Set up the game here. Call this function to restart the game.
        
        Allow the user to specify how many tanks to start the game
        with. Note that the way that we do this will DEFINITELY change
        in the future, this is just a fun way to be able to parameterize


        @param num_tanks Number of tanks to instantiate
        """

        # Set up players

        # Populate a list based on number of tanks
        # The list will be useful for keeping track of all of the tanks, and
        # being able to do the same operation (such a "draw") on them all very
        # easily.
        self.tanksList = []
        for n in range(1,num_tanks + 1):
            tank = Tank(
                name=f"Player {n}",
                position = Vec2d(SCREEN_WIDTH*n/(num_tanks+1), SCREEN_HEIGHT/3),
                color=next(TANK_COLORS)
            )

            self.tanksList.append(tank)

        # Create a circular Iterator for the tank list
        # An Iterator is something different from a list, though certainly you can
        # "iterate" through things like lists and tuples and even dictionaries.
        # In other words, lists and tuples and dictionaries can themselves be termed
        # "Iterators". I still want a list of tanks, but I also want something that
        # points to that list, but I can use to cycle through them endlessly. I know
        # that I want this, because I know that I just want to be able to keep going
        # to whatever Tank's turn is next. Next, next, next. Me calling "next" shouldn't
        # alter the list of tanks; I can have two "views" of the same data: the list
        # view, and the endless cycle view.
        self.tanksCycle = cycle(self.tanksList)

        # Set the active player
        self.activeTank = next(self.tanksCycle)

        # Set up other shapes to draw (just the ground for now)
        self.shapes = arcade.ShapeElementList()

        # Create the ground (just a rectangle for now)
        ground = arcade.create_rectangle_filled(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 6,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT / 3,
            color=arcade.color.DARK_SPRING_GREEN
        )
        self.shapes.append(ground)
    
    def on_key_press(self, key, modifiers):
        """Handle key press events"""

        # Pass through inputs to activeTank

        # Instead of having the Window object handle all of the logic for
        # updating the Tank's turret, we can use the fact that the Tank is
        # a class, and can define its own behaviors (e.g. functions, or methods),
        # that we can then use. So the idea here is to pass the key event on to
        # the Tank, and let it update itself. That way, if somebody really
        # wants to know exactly what the Tank is doing with key presses, they can
        # go look. Otherwise, if they just want to know the general flow of the
        # game, they can look here and say "oh look, the Tank handles keyboard events".
        # This is an example of the idea of "encapsulation", an important principle
        # in programming. Encapsulation states that we should try to group similar
        # data and behaviors and put them into a box, with only useful interfaces
        # exposed. Think of a car: we encapsulate the workings of the engine and
        # the starter and just give people a key to turn. Then, if they want to know
        # more, or things aren't working, they can pop the hood and look in.
        self.activeTank.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        """Handle key release events"""

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
            # Actually set the active tank
            self.activeTank = next(self.tanksCycle)

    def on_update(self, delta_time):
        """ Update game state for game objects """

        # Make the active tank update
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
        
        # Display the current player's name
        arcade.draw_text(
            text=f"Active: {self.activeTank.name}",
            start_x=SCREEN_WIDTH/2-50,
            start_y=0.95*SCREEN_HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

        # Draw other shapes
        self.shapes.draw()


def main():
    """ Main method """
    window = BlackEarthGame()
    window.setup(num_tanks=4)
    arcade.run()


if __name__ == "__main__":
    main()