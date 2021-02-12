
import arcade
from pymunk import Vec2d

TANK_SIZE = 50
TANK_TURRET_LENGTH = 50
TANK_STARTING_ANGLE_DEG = 45
TURRET_ANGLE_MAX = 180
TURRET_ANGLE_MIN = 0
TURRET_WIDTH = 5
TURRET_OFFSET_Y = 5
TURRET_SPEED = 2

class Tank:
    """
    Class encapsulating a player Tank
    """

    def __init__(self, x: float, y: float, color: arcade.color):
        """
        Construct the tank with a position and color
        """
        self.size = TANK_SIZE
        self.position = Vec2d(x,y)
        self.color = color
        self.turretAngleDeg = TANK_STARTING_ANGLE_DEG
        self.turretLength = TANK_TURRET_LENGTH
        self.moveTurret = 0

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
        turretPosition = Vec2d(self.turretLength, 0)
        turretPosition.rotate_degrees(self.turretAngleDeg)
        arcade.draw_line(
            start_x=self.position.x,
            start_y=self.position.y,
            end_x=turretPosition.x + self.position.x,
            end_y=turretPosition.y + self.position.y,
            color=self.color,
            line_width=TURRET_WIDTH
        )
    
    def on_key_press(self, key, modifiers):
        """
        Handle key presses.
        
        If a key is pressed, we'll set a turret movement
        speed. We can't just move the turret, because otherwise the turret will
        only move each and every time that we press a key (meaning, we have to
        press, release, press, release, just to move twice). Instead, we'll change
        the turret's movement speed based on which keys are pressed.
        """
        if key == arcade.key.LEFT:
            self.moveTurret += TURRET_SPEED
        if key == arcade.key.RIGHT:
            self.moveTurret -= TURRET_SPEED

    def on_key_release(self, key, modifiers):
        """
        Handle key releases.

        Decrement the turret speed
        """
        if key == arcade.key.LEFT:
            self.moveTurret -= TURRET_SPEED
        if key == arcade.key.RIGHT:
            self.moveTurret += TURRET_SPEED

    def on_update(self):
        """
        Update the player state

        Update the turret angle (and bound it).
        """
        if self.moveTurret != 0:
            self.turretAngleDeg += self.moveTurret
        if self.turretAngleDeg > TURRET_ANGLE_MAX:
            self.turretAngleDeg = TURRET_ANGLE_MAX
        elif self.turretAngleDeg < TURRET_ANGLE_MIN:
            self.turretAngleDeg = TURRET_ANGLE_MIN