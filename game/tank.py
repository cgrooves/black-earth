# General import statements
import itertools

# Third-party library import statements
import arcade
import pymunk

import numpy

# Local imports
import bullet

# Make some global variables with general Tank constants

# Note: In general, global variables are very much discouraged, and we
# should put a TODO: here for us to remove these and put them into, say,
# a config file or some higher-level function to delegate, but for now
# they work, and we'll roll with it.
TANK_SIZE = 50
TANK_TURRET_LENGTH = 40
TURRET_ANGLE_MAX = 180
TURRET_ANGLE_MIN = 0
TURRET_WIDTH = 5
TURRET_OFFSET_Y = 5

TANK_STARTING_ANGLE_DEG = 45
TURRET_SPEED_STEP = 2

TURRET_POWER_MAX = 100
TURRET_POWER_MIN = 0

# Make an endless iterable of colors to use with Tanks.
# Note: this may or may not survive; we'll probably think
# of a better way to do this in the future.
TANK_COLORS = itertools.cycle([
    arcade.csscolor.RED,
    arcade.csscolor.BLUE,
    arcade.csscolor.GREEN,
    arcade.csscolor.YELLOW,
    arcade.csscolor.LAVENDER,
    arcade.csscolor.DEEP_PINK
])

class Tank:
    """
    Class encapsulating a player Tank

    Contains data and methods for defining and controlling a
    tank.
    """

    def __init__(
        self, name: str,
        parent: arcade.Window,
        position: pymunk.Vec2d,
        color: arcade.color
        ):
        """
        Construct the tank with a name, position and color
        """
        self.name = name
        self.parent = parent
        self.size = TANK_SIZE
        self.position = position
        self.color = color
        self.turretAngleDeg = TANK_STARTING_ANGLE_DEG
        self.turretLength = TANK_TURRET_LENGTH
        self.turretSpeed = 0
        self.powerIncrement = 0
        self.power = 50
        self.turretTip = pymunk.Vec2d()

    def draw(self):
        """
        Render the tank body and turret
        """
        # Draw tank body
        arcade.draw_arc_filled(
            center_x=self.position.x,
            center_y=self.position.y,
            width=self.size,
            height=self.size,
            color=self.color,
            start_angle=0.0,
            end_angle=180
        )
        # Draw turret
        # Calculate turret end point
        turretPosition = pymunk.Vec2d(self.turretLength, 0)
        turretPosition.rotate_degrees(self.turretAngleDeg)
        self.turretTip.x = turretPosition.x + self.position.x
        self.turretTip.y = turretPosition.y + self.position.y + TURRET_WIDTH/2

        arcade.draw_line(
            start_x=self.position.x,
            start_y=self.position.y + TURRET_WIDTH/2,
            end_x=self.turretTip.x,
            end_y=self.turretTip.y,
            color=self.color,
            line_width=TURRET_WIDTH
        )
    
    def on_key_press(self, key, modifiers):
        """
        Handle key presses.
        
        If a key is pressed, we'll set a turret movement
        speed. We can't just move the turret, because otherwise the turret will
        only move each and every time that we press a key (meaning, we have to
        press, release, press, release, just to move two degrees). Instead, we'll change
        the turret's movement speed based on which keys are pressed.
        """
        if key == arcade.key.LEFT:
            self.turretSpeed = TURRET_SPEED_STEP
        if key == arcade.key.RIGHT:
            self.turretSpeed = -TURRET_SPEED_STEP

        # Handle the power increment
        if key == arcade.key.UP:
            self.powerIncrement = TURRET_SPEED_STEP
        if key == arcade.key.DOWN:
            self.powerIncrement = -TURRET_SPEED_STEP

    def on_key_release(self, key, modifiers):
        """
        Handle key releases.

        Decrement the turret speed. The equivalent of saying "When!" when
        your dad is pouring juice.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.turretSpeed = 0

        if key == arcade.key.SPACE:
            self.turretSpeed = 0
            self.powerIncrement = 0
            self.processFireEvent()
        
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.powerIncrement = 0

    def on_update(self):
        """
        Update the player state

        Update the turret angle (and bound it to a min and max).
        """
        # Increment the turret speed
        self.turretAngleDeg += self.turretSpeed
        # Bound the turret speed
        if self.turretAngleDeg > TURRET_ANGLE_MAX:
            self.turretAngleDeg = TURRET_ANGLE_MAX
        elif self.turretAngleDeg < TURRET_ANGLE_MIN:
            self.turretAngleDeg = TURRET_ANGLE_MIN
        
        # Increment the power
        self.power += self.powerIncrement
        # Bound the power
        if self.power > TURRET_POWER_MAX:
            self.power = TURRET_POWER_MAX
        elif self.power < TURRET_POWER_MIN:
            self.power = TURRET_POWER_MIN
    
    def processFireEvent(self):
        """Create the artillery round and pass it to the physics engine"""
        tank_round = bullet.BulletSprite(5, arcade.color.GHOST_WHITE)
        tank_round.angle = self.turretAngleDeg
        tank_round.center_x = self.turretTip.x
        tank_round.center_y = self.turretTip.y
        self.parent.add_bullet(tank_round, self.power)