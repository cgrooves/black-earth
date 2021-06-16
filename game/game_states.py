import arcade

class GameState:

    def __init__(self, game) -> None:
        super().__init__()
        self._game = game
    
    def setup(self):
        pass
    
    def on_update(self, delta_time):
        self._game.tanksList.on_update(delta_time)

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_draw(self):
        # Common things that we always draw
        self._game.tankSpriteList.draw()
        self._game.draw_hud()
        self._game.ground.draw()


class InputState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)
    
    def on_key_press(self, key, modifiers):
        
        # Pass through to active tank
        self._game.activeTank.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        # Pass through to active tank
        self._game.activeTank.on_key_release(key, modifiers)

        # If fire key, then set to BallisticSimState
        if key == arcade.key.SPACE:
            self._game.activeState = self._game.ballisticSimState


class BallisticSimState(GameState):

    def __init__(self, game) -> None:
        super().__init__(game)

    def on_update(self, delta_time):
        super().on_update(delta_time)

        # Handle transition to next state
        if len(self._game.weaponsQueue) == 0:
            self._game.activeTank = self._game.tanksList.getNext()
            self._game.activeState = self._game.inputState
        
        # Update bullet physics
        self._game.physicsEngine.step(delta_time=delta_time)
    
    def on_draw(self):

        # Draw all normally + weapons
        super().on_draw()
        self._game.weaponsQueue.draw()