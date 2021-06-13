# General import statements
import itertools

# Third-party library import statements
import arcade
import pymunk
import numpy

# Local imports
from weapons import weaponsList
from config import TankConfig, TurretConfig

# Defining scaling factor of tank sprites.
SPRITE_SCALING_PLAYER = 0.5
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
        self.flipped = False
        self.turretLength = TurretConfig.LENGTH
        self.power = TurretConfig.POWER_START
        
        self.turretSpeed = 0
        self.powerIncrement = 0
        
        self.turretTip = pymunk.Vec2d()

        # Create a cyclical view of the weapons list
        self.weaponsCycle = itertools.cycle(weaponsList)

        # Set the active weapon
        self.activeWeapon = next(self.weaponsCycle)

        # Tank Sprite List
        self.sprite_list = arcade.SpriteList()

        # Load tank sprites
        self.turret_sprite = arcade.Sprite("./game/images/turret.png", SPRITE_SCALING_PLAYER)
        self.sprite_list.append(self.turret_sprite)

        self.body_texture_right = arcade.load_texture("./game/images/body.png", flipped_horizontally=False)
        self.body_texture_left  = arcade.load_texture("./game/images/body.png", flipped_horizontally=True)
        self.body_sprite = arcade.Sprite(scale=SPRITE_SCALING_PLAYER)
        self.body_sprite.texture = self.body_texture_right
        self.sprite_list.append(self.body_sprite)

        self.track_sprite = arcade.Sprite(filename="./game/images/tracks.png", scale=SPRITE_SCALING_PLAYER)
        self.sprite_list.append(self.track_sprite)

    def draw(self):
        """
        Render the tank body and turret
        """

        self.sprite_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Handle key presses.
        
        If a key is pressed, we'll set a turret movement
        speed. We can't just move the turret, because otherwise the turret will
        only move each and every time that we press a key (meaning, we have to
        press, release, press, release, just to move two degrees). Instead, we'll change
        the turret's movement speed based on which keys are pressed.
        """
        turretInc = TurretConfig.INC_STEP
        if modifiers & arcade.key.MOD_CTRL:
            turretInc = TurretConfig.INC_STEP // 2

        if key == arcade.key.LEFT:
            self.turretSpeed = turretInc
        if key == arcade.key.RIGHT:
            self.turretSpeed = -turretInc

        # Handle the power increment
        if key == arcade.key.UP:
            self.powerIncrement = turretInc
        if key == arcade.key.DOWN:
            self.powerIncrement = -turretInc

    def on_key_release(self, key, modifiers):
        """
        Handle key releases.

        Decrement the turret speed. The equivalent of saying "When!" when
        your dad is pouring juice.
        """
        if modifiers & arcade.key.MOD_CTRL:
            self.turretSpeed *= 2

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

        # Flip turret
        if self.turretAngleDeg > 90 and not self.flipped:
            self.flipped = True
            self.body_sprite.texture = self.body_texture_left
        if self.turretAngleDeg < 90 and self.flipped:
            self.flipped = False
            self.body_sprite.texture = self.body_texture_right

        # Increment the power
        self.power += self.powerIncrement

        # Bound the power
        if self.power > TurretConfig.POWER_MAX:
            self.power = TurretConfig.POWER_MAX
        elif self.power < TurretConfig.POWER_MIN:
            self.power = TurretConfig.POWER_MIN

        # Position Sprites
        self.body_sprite.center_x = self.position.x
        self.body_sprite.center_y = self.position.y + 11
        self.track_sprite.center_x = self.position.x
        self.track_sprite.center_y = self.position.y + 2

        # Rotate turret
        self.turret_sprite.angle = self.turretAngleDeg
        self.turret_sprite.center_x = self.position.x + 9*numpy.cos(numpy.deg2rad(self.turretAngleDeg))
        self.turret_sprite.center_y = self.position.y + 9*numpy.sin(numpy.deg2rad(self.turretAngleDeg)) + 20
    
    def processFireEvent(self):
        """Create the artillery round and pass it to the physics engine"""
        weapon = self.activeWeapon()
        weapon.angle = self.turretAngleDeg
        weapon.center_x = self.turretTip.x
        weapon.center_y = self.turretTip.y
        weapon.power = self.power
        self.parent.queue_fire_event(weapon)