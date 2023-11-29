import pygame
from entities.entity import Entity

from constants import GameConstants, DirectionConstants

class Player(Entity):
    def __init__(self, size, color, step_size, rect, image_file):    
        super().__init__(size, color, step_size, rect)
        self.lifes = 3
        self.score = 0
        self.image_file = image_file
        self.base_image = pygame.transform.scale(pygame.image.load(image_file), (self.SIZE[0], self.SIZE[1]))
        self.image = self.base_image
            

    def update_player_position(self, Game : GameConstants, wall_array_rect) -> pygame.Rect:
        old_self_pos = pygame.Rect(self.rect.left, self.rect.top, self.SIZE[0], self.SIZE[1])
        new_self_pos = self.update_position(old_self_pos, Game) 
        
        # Rotate Player Image
        if self.direction == DirectionConstants.LEFT: 
            self.image = pygame.transform.rotate(self.base_image, 180)
        elif self.direction == DirectionConstants.RIGHT:
            self.image = self.base_image
        elif self.direction == DirectionConstants.UP:
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif self.direction == DirectionConstants.DOWN:
            self.image = pygame.transform.rotate(self.base_image, 270)
  
        # Wall Collision
        if new_self_pos.collidelist(wall_array_rect) >= 0:
            self.collision[self.direction] = True
        else:
            self.rect = new_self_pos
            
        return new_self_pos
