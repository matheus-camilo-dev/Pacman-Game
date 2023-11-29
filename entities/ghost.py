import random
import pygame

from constants import *
from entities.entity import Entity

class Ghost(Entity):
    def __init__(self, size, color, step_size, rect):    
        super().__init__(size, color, step_size, rect)
        self.scape_ticks = 0
        self.normal_color = Colors.RED
        self.scape_color = Colors.PURPLE
        self.power_up_image_file = 'powerup'
        self.dead_image_file = 'dead'
        ghost_image_list = ['blue', 'orange', 'pink', 'red']
        self.image_file = random.choice(ghost_image_list)
        self.normal_image_file = self.image_file
        self.dead_time = 30
        self.is_dead = False

    def update_ghost_position(self, Game : GameConstants, wall_array_rect, player_rect : pygame.Rect, ghosts_rect_array) -> None:
        new_self_pos = pygame.Rect(self.rect.left, self.rect.top, self.SIZE[0], self.SIZE[1])
        
        if self.is_dead:
            self.image_file = self.dead_image_file
            self.dead_time -= 1 
            
            if self.dead_time <= 0:
                self.image_file = self.normal_image_file
                self.is_dead = False
                self.scape_ticks = 0
                self.dead_time = 30
            else:        
                return new_self_pos
        
        self.update_position(new_self_pos, Game)
        
        # Wall Collision and Other Ghosts Collision
        if new_self_pos.collidelist(wall_array_rect) >= 0 or new_self_pos.collidelist(ghosts_rect_array) >= 0:
            self.collision[self.direction] = True
        else:
            self.rect = new_self_pos

        # Generate Moviment
        self.generate_moviment(player_rect)

    
    def generate_moviment(self, rect : pygame.Rect) -> None:
        # Follow The Player
        if abs(self.rect.top - rect.top) > abs(self.rect.left - rect.left):
            if self.rect.top - rect.top > 0:
                self.direction = DirectionConstants.UP
            else:
                self.direction = DirectionConstants.DOWN
        else:
            if self.rect.left - rect.left > 0:
                self.direction = DirectionConstants.LEFT
            else:
                self.direction = DirectionConstants.RIGHT
        
        # Escape from the player
        if self.scape_ticks > 0:
            self.scape_ticks -= 1
            self.invert_direction()
            if self.scape_ticks < 20 and self.scape_ticks % 4 == 0:
                if self.image_file == self.power_up_image_file:
                    self.image_file = self.normal_image_file
                else:
                    self.image_file = self.power_up_image_file
            else:
                self.image_file = self.power_up_image_file
        else:
            self.image_file = self.normal_image_file


    def invert_direction(self) -> None:
        self.direction *= -1
