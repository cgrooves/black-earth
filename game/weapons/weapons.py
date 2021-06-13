import arcade

from config import WindowConfig, WeaponConfig

class Weapon(arcade.SpriteCircle):
    """Weapon base class
    
    All other classes should inherit from this class and override
    at least the `name` and `detonate` function
    """

    name = "Weapon"
    mass = WeaponConfig.MASS
    friction = WeaponConfig.FRICTION

    def __init__(self):
        super().__init__(radius=5, color=WeaponConfig.COLOR)

        self.power = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """Handle when the sprite is moved by the physics engine
        
        When the sprite goes off-screen to the left or right, I
        want it to disappear and cease to exist.
        """

        if self.center_x <= 0 or self.center_x >= WindowConfig.WIDTH:
            self.remove_from_sprite_lists()
    
    def detonate(self, tank=None):
        pass


class BabyMissile(Weapon):
    """Baby Missile class"""

    name = "Baby Missile"

    def detonate(self, tank=None):
        print("little boom")

        if tank is not None:
            tank.health -= 50


class Missile(Weapon):
    """Missile class"""

    name = "Missile"
    
    def detonate(self, tank=None):
        print("BIGGER BOOM!")

        if tank is not None:
            tank.health -= 100