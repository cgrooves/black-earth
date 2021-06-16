"""
Hello-World example given from https://arcade.academy/examples/platform_tutorial/step_01.html
"""

# General import statements
import itertools
import queue

# Third-party library import statements
import arcade
import pymunk
from typing import Optional

# Local import statements
from tank import Tank, TankList
from weapons import Weapon
from game_states import GameState, InputState, BallisticSimState

from config import WindowConfig, GameConfig, PhysicsConfig, TankConfig

class BlackEarthGame(arcade.Window):
    """
    Main application class.
    """

    ## ---------------------------------------------------- ##
    # Overridden class functions
    ## ---------------------------------------------------- ##

    def __init__(self, width, height, title):
        """Constructor"""

        # Call the parent class and set up the window
        super().__init__(width, height, title)

        # Set up member variables
        self.weaponsQueue: Optional[arcade.SpriteList] = None
        self.tankSpriteList: Optional[arcade.SpriteList] = None
        self.tanksList: Optional[TankList] = None
        self.physicsEngine = Optional[arcade.PymunkPhysicsEngine]
        self.processing_firing_events = False
        self.weapons_queue = Optional[queue.Queue]

        self.activeState : Optional[GameState] = None
        self.ballisticSimState = BallisticSimState(self)
        self.inputState = InputState(self)

    def setup(self, num_tanks=2):
        """ Set up the game here. Call this function to restart the game.
        
        Allow the user to specify how many tanks to start the game
        with. Note that the way that we do this will DEFINITELY change
        in the future, this is just a fun way to be able to parameterize
        @param num_tanks Number of tanks to instantiate
        """

        self.activeState = self.inputState

        # Set up players
        self.create_tanks(num_tanks)

        # Create the ground (just a rectangle for now)
        self.create_environment()

        # Set up weapons queue and active weapons list
        self.setup_weapons(num_tanks)

        # Add the physics
        self.setup_physics_engine()
        self.setup_physics_collisions()

    def on_key_press(self, key, modifiers):
        """Handle key press events"""

        self.activeState.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        """Handle key release events"""

        # Handle window events first
        if key == arcade.key.ESCAPE:
            exit()

        self.activeState.on_key_release(key, modifiers)

    def on_update(self, delta_time):
        """ Update game state for game objects """

        # Make the active tank update
        self.activeState.on_update(delta_time)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        self.activeState.on_draw()

    ## ------------------------------------------------------------- ##
    ## Custom functions defined below
    ## ------------------------------------------------------------- ##

    def create_tanks(self, num_tanks):

        self.tankSpriteList = arcade.SpriteList()
        self.tanksList = TankList()

        # Populate a list based on number of tanks
        # The list will be useful for keeping track of all of the tanks, and
        # being able to do the same operation (such as "draw") on them all very
        # easily.
        for n in range(1,num_tanks + 1):
            new_tank = Tank(
                name = f"Player {n}",
                parent = self,
                position = pymunk.Vec2d(WindowConfig.WIDTH*n/(num_tanks+1), WindowConfig.HEIGHT/3),
                color = next(TankConfig.COLORS)
            )

            self.tanksList.append(new_tank)
            self.tankSpriteList.extend(new_tank.sprite_list)

        # Set the active player
        self.activeTank = self.tanksList.getNext()
    
    def create_environment(self):
        # Color the sky
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Create the ground
        self.ground = arcade.SpriteSolidColor(
            width=WindowConfig.WIDTH,
            height=WindowConfig.HEIGHT//3,
            color=arcade.color.DARK_SPRING_GREEN
        )
        self.ground.center_x = WindowConfig.WIDTH / 2
        self.ground.center_y = WindowConfig.HEIGHT / 6

    def setup_weapons(self, num_tanks: int):
        self.weaponsQueue = arcade.SpriteList()

        # Set up the firing queue
        if GameConfig.TURN_STYLE == GameConfig.TurnStyle.SEQUENTIAL:
            maxsize = 1
        elif GameConfig.TURN_STYLE == GameConfig.TurnStyle.SYNCHRONOUS:
            maxsize = num_tanks
        else:
            raise IOError(f"{GameConfig.TURN_STYLE} is not a valid turn style option!")

        self.weapons_queue = queue.Queue(maxsize=maxsize)
    
    def setup_physics_engine(self):
        self.physicsEngine = arcade.PymunkPhysicsEngine(
            gravity=(0, PhysicsConfig.GRAVITY),
            damping=PhysicsConfig.DAMPING
        )
    
    def setup_physics_collisions(self):

        # Add the ground
        self.physicsEngine.add_sprite(
            self.ground,
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            collision_type="ground"
        )

        # Add the tank
        self.physicsEngine.add_sprite_list(
            self.tanksList,
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            collision_type="tank"
        )

        # Add collision between tank weapon and ground
        def weapon_ground_handler(weapon_sprite, ground_sprite, _arbiter, _space, _data):
            """Called for weapon/ground collision"""
            weapon_sprite.detonate()
            weapon_sprite.remove_from_sprite_lists()

        # Add collision between tank weapon and tank
        def weapon_tank_handler(weapon_sprite, tank_sprite, _arbiter, _space, _data):
            """Called for weapon/tank collision"""
            weapon_sprite.detonate(tank_sprite)
            weapon_sprite.remove_from_sprite_lists()

        self.physicsEngine.add_collision_handler("weapon", "ground", post_handler=weapon_ground_handler)
        self.physicsEngine.add_collision_handler("weapon", "tank", post_handler=weapon_tank_handler)
    
    def draw_hud(self):
        # TODO: Encapsulate the HUD as a class
        # Render the activeTank's tank angle
        arcade.draw_text(
            text=f"Angle: {self.activeTank.turretAngleDeg}",
            start_x =10.0,
            start_y=0.95*WindowConfig.HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

        # Render the activeTank's power
        arcade.draw_text(
            text=f"Power: {self.activeTank.power}",
            start_x =140.0,
            start_y=0.95*WindowConfig.HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

        # Display the current player's name
        arcade.draw_text(
            text=f"Active: {self.activeTank.name}",
            start_x=WindowConfig.WIDTH/2-50,
            start_y=0.95*WindowConfig.HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

        # Display the current player's active weapon name
        arcade.draw_text(
            text=f"Weapon: {self.activeTank.activeWeapon.name}",
            start_x=WindowConfig.WIDTH/2-50,
            start_y=0.90*WindowConfig.HEIGHT,
            color=arcade.csscolor.WHITE_SMOKE
        )

    def add_active_weapon(self, weapon: Weapon):
        """Add a tank's activated (i.e. fired) weapon to the physics engine"""

        self.weaponsQueue.append(weapon)
        self.physicsEngine.add_sprite(weapon,
            mass=weapon.mass,
            damping=PhysicsConfig.DAMPING,
            friction=weapon.friction,
            collision_type="weapon")
        self.physicsEngine.apply_impulse(weapon, (weapon.power,0))

    def queue_fire_event(self, weapon: Weapon):
        """Queue a fire event to be processed by the game"""

        self.weapons_queue.put(weapon)

        if self.weapons_queue.full():
            self.processing_firing_events = True
            while not self.weapons_queue.empty():
                self.add_active_weapon(self.weapons_queue.get())
        
        return



def main():
    """ Main function for running the game """
    window = BlackEarthGame(
        width=WindowConfig.WIDTH,
        height=WindowConfig.HEIGHT,
        title=WindowConfig.TITLE
    )
    window.setup(num_tanks=GameConfig.NUM_TANKS)
    arcade.run()

# Put this here in case we want to run the game from
# some other file or function later, we can import the
# main() function without running this file as a script
if __name__ == "__main__":
    main()