""" Sprite Sample Program """

import random
import arcade
from weapons import Weapon
import tank
from config import TurretConfig


# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that hold sprit lists.
        self.player_list = None
        self.bullet_list = None

        # Setup up player info
        self.tank_sprite = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite lists
        self.tank_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Setup the player
        
        # Turret image from kenney.nl
        self.turret_sprite = arcade.Sprite("./game/images/turret.png", SPRITE_SCALING_PLAYER)
        self.turret_sprite.center_x = 62
        self.turret_sprite.center_y = 59
        self.tank_list.append(self.turret_sprite)

        # Tank track image from kenney.nl
        self.track_sprite = arcade.Sprite("./game/images/tracks.png", SPRITE_SCALING_PLAYER)
        self.track_sprite.center_x = 50
        self.track_sprite.center_y = 40
        self.tank_list.append(self.track_sprite)

        # Tank body image from kenney.nl
        self.tank_sprite = arcade.Sprite("./game/images/body.png", SPRITE_SCALING_PLAYER)
        self.tank_sprite.center_x = 50
        self.tank_sprite.center_y = 50
        self.tank_list.append(self.tank_sprite)

    def on_draw(self):
        arcade.start_render()
        self.tank_list.draw()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()