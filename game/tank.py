# General import statements
import itertools

# Third-party library import statements
import arcade
import pymunk

import numpy

# Local imports
from weapons import weaponsList
from config import TankConfig, TurretConfig

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
        self.size = TankConfig.SIZE
        self.position = position
        self.color = color

        # Create the turret
        # TODO: make a Turret class later on to encapsulate this
        # Then creating the turret might look something more like
        # >> self.turret = TurretBasic()
        self.turretAngleDeg = TurretConfig.STARTING_ANGLE_DEG
        self.turretLength = TurretConfig.LENGTH
        self.power = TurretConfig.POWER_START
        
        self.turretSpeed = 0
        self.powerIncrement = 0
        
        self.turretTip = pymunk.Vec2d()

        # Create a cyclical view of the weapons list
        self.weaponsCycle = itertools.cycle(weaponsList)

        # Set the active weapon
        self.activeWeapon = next(self.weaponsCycle)

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
        self.turretTip.y = turretPosition.y + self.position.y + TurretConfig.WIDTH/2

        arcade.draw_line(
            start_x=self.position.x,
            start_y=self.position.y + TurretConfig.WIDTH/2,
            end_x=self.turretTip.x,
            end_y=self.turretTip.y,
            color=self.color,
            line_width=TurretConfig.WIDTH
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
            self.turretSpeed = TurretConfig.INC_STEP
        if key == arcade.key.RIGHT:
            self.turretSpeed = -TurretConfig.INC_STEP

        # Handle the power increment
        if key == arcade.key.UP:
            self.powerIncrement = TurretConfig.INC_STEP
        if key == arcade.key.DOWN:
            self.powerIncrement = -TurretConfig.INC_STEP

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
        
        if key == arcade.key.TAB:
            self.activeWeapon = next(self.weaponsCycle)

    def on_update(self):
        """
        Update the player state

        Update the turret angle (and bound it to a min and max).
        """
        # Increment the turret speed
        self.turretAngleDeg += self.turretSpeed
        # Bound the turret speed
        if self.turretAngleDeg > TurretConfig.ANGLE_MAX:
            self.turretAngleDeg = TurretConfig.ANGLE_MAX
        elif self.turretAngleDeg < TurretConfig.ANGLE_MIN:
            self.turretAngleDeg = TurretConfig.ANGLE_MIN
        
        # Increment the power
        self.power += self.powerIncrement
        # Bound the power
        if self.power > TurretConfig.POWER_MAX:
            self.power = TurretConfig.POWER_MAX
        elif self.power < TurretConfig.POWER_MIN:
            self.power = TurretConfig.POWER_MIN
    
    def processFireEvent(self):
        """Create the artillery round and pass it to the physics engine"""
        weapon = self.activeWeapon()
        weapon.angle = self.turretAngleDeg
        weapon.center_x = self.turretTip.x
        weapon.center_y = self.turretTip.y
        weapon.power = self.power
        self.parent.add_active_weapon(weapon)