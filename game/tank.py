# General import statements
import itertools

# Third-party library import statements
import arcade
import pymunk
import numpy

# Local imports
from weapons import weaponsList
from config import TankConfig, TurretConfig

class TankList(arcade.SpriteList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._index = 0

    def getNext(self):
        if len(self.sprite_list) == 0:
            return None
        elif self._index == len(self.sprite_list):
            self._index = 0
        
        item = self.sprite_list[self._index]
        self._index += 1
        return item

class Tank(arcade.Sprite):
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
        self.size = TankConfig.SIZE
        super().__init__(scale=self.size)

        self.name = name
        self.parent = parent
        # Offset the y position
        self.center_x = position.x
        self.center_y = position.y + 20
        self.color = color
        self.health = 100

        self.append_texture(arcade.load_texture("./game/images/body.png", flipped_horizontally=False))
        self.append_texture(arcade.load_texture("./game/images/body.png", flipped_horizontally=True))
        self.set_texture(TankConfig.RIGHT_TEXT_ID)
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
        self.turret_sprite = arcade.Sprite("./game/images/turret.png", self.size)
        self.sprite_list.append(self.turret_sprite)
        self.turret_sprite.color = color

        self.track_sprite = arcade.Sprite(filename="./game/images/tracks.png", scale=self.size)
        self.track_sprite.color = color
        self.sprite_list.append(self.track_sprite)

        self.sprite_list.append(self)

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
        if modifiers & arcade.key.MOD_CTRL:
            turretInc = TurretConfig.MINOR_INC_STEP
        else:
            turretInc = TurretConfig.MAJOR_INC_STEP

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

        if key == arcade.key.H:
            self.power = TurretConfig.POWER_MAX
        if key == arcade.key.L:
            self.power = TurretConfig.POWER_MIN
        if key == arcade.key.M:
            self.power = (TurretConfig.POWER_MAX - TurretConfig.POWER_MIN) // 2

    def on_update(self, delta_time):
        """
        Update the player state

        Update the turret angle (and bound it to a min and max).
        """
        # Handle health
        if self.health <= 0:
            print(f"{self.name} hath died!")
            self.death()

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
            self.set_texture(TankConfig.LEFT_TEXT_ID)
        if self.turretAngleDeg < 90 and self.flipped:
            self.flipped = False
            self.set_texture(TankConfig.RIGHT_TEXT_ID)

        # Increment the power
        self.power += self.powerIncrement

        # Bound the power
        if self.power > TurretConfig.POWER_MAX:
            self.power = TurretConfig.POWER_MAX
        elif self.power < TurretConfig.POWER_MIN:
            self.power = TurretConfig.POWER_MIN

        # Position Sprites
        self.track_sprite.center_x = self.center_x
        self.track_sprite.center_y = self.center_y - 15

        # Rotate turret
        self.turret_sprite.angle = self.turretAngleDeg
        self.turret_sprite.center_x = self.center_x + 9*numpy.cos(numpy.deg2rad(self.turretAngleDeg))
        self.turret_sprite.center_y = self.center_y + 9*numpy.sin(numpy.deg2rad(self.turretAngleDeg)) + 9

        # Set the turret tip
        self.turretTip.x = self.turret_sprite.center_x + 17*numpy.cos(numpy.deg2rad(self.turretAngleDeg))
        self.turretTip.y = self.turret_sprite.center_y + 17*numpy.sin(numpy.deg2rad(self.turretAngleDeg))
    
    def processFireEvent(self):
        """Create the artillery round and pass it to the physics engine"""
        weapon = self.activeWeapon()
        weapon.angle = self.turretAngleDeg
        weapon.center_x = self.turretTip.x
        weapon.center_y = self.turretTip.y
        weapon.power = self.power
        self.parent.queue_fire_event(weapon)
    
    def death(self):
        self.track_sprite.kill()
        self.turret_sprite.kill()
        self.kill()