import arcade

from constants import SCREEN_WIDTH

class BulletSprite(arcade.SpriteCircle):
    """Bullet sprite"""

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """Handle when the sprite is moved by the physics engine"""

        if self.center_x <= 0 or self.center_x >= SCREEN_WIDTH:
            self.remove_from_sprite_lists()
    
    def detonate(self):
        pass