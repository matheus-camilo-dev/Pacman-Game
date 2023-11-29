import pygame

from constants import DirectionConstants, GameConstants

class Entity:
    def __init__(self, size : int , color, step_size,  rect : pygame.Rect):
        self.SIZE = (size, size)
        self.COLOR = color
        self.rect = rect
        self.STEP_SIZE = step_size
        self.display = True

        self.direction = DirectionConstants.STOP
        self.rect = rect
        self.collision = [
            False, 
            False, # LEFT
            False, # UP
            False, # RIGHT
            False  # DOWN
        ]
    
    def update_position(self, position,  gameConstants : GameConstants):   
        # Valid Moviment
        if self.direction == DirectionConstants.LEFT and not self.collision[DirectionConstants.LEFT]:
            position[0] -= self.STEP_SIZE
        elif self.direction == DirectionConstants.RIGHT and not self.collision[DirectionConstants.RIGHT]:
            position[0] += self.STEP_SIZE
        elif self.direction == DirectionConstants.UP and not self.collision[DirectionConstants.UP]:
            position[1] -= self.STEP_SIZE
        elif self.direction == DirectionConstants.DOWN and not self.collision[DirectionConstants.DOWN]:
            position[1] += self.STEP_SIZE
        
        self.collision = [
            False, 
            False, # LEFT
            False, # UP
            False, # RIGHT
            False  # DOWN
        ]
        
        # Position Out of Screen
        if self.rect.topleft[0] >=  gameConstants.WIDTH:
            position[0] = 0
        elif self.rect.topleft[0] < 0:
            position[0] = gameConstants.WIDTH - gameConstants.TILE_SIZE
        
        if self.rect.topleft[1] >=  gameConstants.HEIGHT:
            position[1] = 0
        elif self.rect.topleft[1] < 0:
            position[1] = gameConstants.HEIGHT - gameConstants.TILE_SIZE

        return position
