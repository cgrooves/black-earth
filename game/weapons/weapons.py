import arcade

from constants import SCREEN_WIDTH

class Bullet(arcade.SpriteCircle):
    """Bullet"""

    name = "Bullet"

    def __init__(self):
        super().__init__(radius=5, color=arcade.color.GHOST_WHITE)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """Handle when the sprite is moved by the physics engine
        
        When the sprite goes off-screen to the left or right, I
        want it to disappear and cease to exist.
        """

        if self.center_x <= 0 or self.center_x >= SCREEN_WIDTH:
            self.remove_from_sprite_lists()
    
    def detonate(self):
        print("little boom")

class Missile(Bullet):
    """Missile class"""

    name = "Missile"
    
    def detonate(self):
        print("BIGGER BOOM!")