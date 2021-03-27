import arcade

from constants import SCREEN_WIDTH

class Bullet(arcade.SpriteCircle):
    """Bullet"""

    def get_name(self):
        return "Bullet"

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """Handle when the sprite is moved by the physics engine
        
        When the sprite goes off-screen to the left or right, I
        want it to disappear and cease to exist.
        """

        if self.center_x <= 0 or self.center_x >= SCREEN_WIDTH:
            self.remove_from_sprite_lists()
    
    def detonate(self):
        pass

class Missile(Bullet):
    """Missile class"""

    def get_name(self):
        return "Missile"
    
    def detonate(self):
        print("BIGGER BOOM!")
