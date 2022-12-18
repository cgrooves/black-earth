import itertools
import arcade

# Config Constants

class WindowConfig:
    WIDTH = 1000
    HEIGHT = 650
    TITLE = "Black Earth"


class GameConfig:
    class TurnStyle:
        SEQUENTIAL = 1
        SYNCHRONOUS = 2

    NUM_TANKS = 4
    TURN_STYLE = TurnStyle.SEQUENTIAL

class PhysicsConfig:
    GRAVITY = -1500
    DAMPING = 1.0

class WeaponConfig:
    MASS = 0.08
    FRICTION = 0.6
    COLOR = arcade.color.GHOST_WHITE

class TankConfig:
    SIZE = 50

    COLORS = itertools.cycle([
        arcade.csscolor.RED,
        arcade.csscolor.BLUE,
        arcade.csscolor.GREEN,
        arcade.csscolor.YELLOW,
        arcade.csscolor.LAVENDER,
        arcade.csscolor.DEEP_PINK
    ])

class TurretConfig:
    LENGTH = 40
    WIDTH = 5
    OFFSET_Y = 5

    INC_STEP = 2

    ANGLE_MAX = 180
    ANGLE_MIN = 0
    STARTING_ANGLE_DEG = 45

    POWER_MAX = 100
    POWER_MIN = 0
    POWER_START = 50