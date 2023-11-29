import sys
import time as timer
from time import sleep

import pygame

from entities.player import Player
from entities.ghost import Ghost

from constants import (
    GameConstants, DirectionConstants, GameStatus, WallConstants, 
    MapsElements as mp, Colors, player_closes_game, player_loses_the_game, player_win_game)
from maps import GameMap

# Pygame Inits
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Prepare Constants
game_map = GameMap
Game = GameConstants(game_map.TILE_PROPORTION)
Wall = WallConstants(Game.TILE_SIZE)
Direction = DirectionConstants()

# Configure Game
screen = pygame.display.set_mode((Game.WIDTH, 660))
game = pygame.Surface((Game.WIDTH, Game.HEIGHT))
pygame.display.set_caption("Pacman")
time = pygame.time.Clock()

# Configure Font
game_font = pygame.font.SysFont('Comic Sans MS', 30)

# Configure Music
music = pygame.mixer.Sound('sounds/sound_intro.mp3')

def get_elements_from_map(game_map):
    wall_array_rect, ghosts, fruits_rects, special_fruits_rects = [], [], [], []
    for line in range(0, len(game_map)):
        for column in range(0, len(game_map[line])):
            default_x, default_y = column * Wall.WALL_SIZE[0], line * Wall.WALL_SIZE[1]
            if game_map[line][column] == mp.WALL:
                wall_array_rect.append(
                    pygame.Rect(
                        default_x, 
                        default_y, 
                        Wall.WALL_SIZE[0], Wall.WALL_SIZE[1]
                    )
                )
            if game_map[line][column] == mp.PACMAN:
                player = Player(
                    Game.TILE_SIZE, 
                    Colors.YELLOW, 
                    Game.TILE_SIZE, 
                    pygame.Rect(default_x, default_y, Game.TILE_SIZE, Game.TILE_SIZE),
                    'assets/player_images/default.png'
                )
            if game_map[line][column] == mp.GHOST:
                ghosts.append(
                    Ghost(
                        Game.TILE_SIZE, 
                        Colors.RED, 
                        10, 
                        pygame.Rect(
                            default_x, 
                            default_y, 
                            Game.TILE_SIZE, Game.TILE_SIZE)
                        
                        )
                )
            if game_map[line][column] == mp.VOID:
                fruits_rects.append(
                    pygame.Rect(
                        default_x + (Game.TILE_SIZE // 4), 
                        default_y + (Game.TILE_SIZE // 4), 
                        Game.TILE_SIZE // 2, Game.TILE_SIZE // 2)
                )
            if game_map[line][column] == mp.ESPECIAL_FRUIT:
                special_fruits_rects.append(
                    pygame.Rect(
                        default_x + (Game.TILE_SIZE // 8), 
                        default_y + (Game.TILE_SIZE // 8), 
                        Game.TILE_SIZE // 1.3, Game.TILE_SIZE // 1.3)
                )
    return wall_array_rect, player, ghosts, fruits_rects, special_fruits_rects

def game_menu() -> None:
    music.play(-1)
    music.set_volume(0.1)
    
    while True:
        screen.fill(Colors.BLACK)
        text_width, text_height = game_font.size('Pacman')
        text_surface = game_font.render('Pacman', False, Colors.YELLOW)
        screen.blit(text_surface, ((Game.WIDTH - text_width) // 2, (Game.HEIGHT - text_height) // 2))
        text_width, text_height = game_font.size('Pressione Qualquer tecla para iniciar!')
        text_surface = game_font.render('Pressione Qualquer tecla para iniciar!', False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width) // 2, (Game.HEIGHT - text_height) // 2 + text_height))
        for event in pygame.event.get():
            # Player Event
            if event.type == pygame.KEYDOWN:
                music.stop()
                return None
            
            # Quit Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()

def game_win(finish_time : float, points : int, high_score : int) -> None:
    
    while True:        
        text_width1, text_height1 = game_font.size('Parabéns!')
        text_width2, text_height2 = game_font.size('Você Ganhou!')
        text_width3, text_height3 = game_font.size(f'Tempo: {finish_time:.2f}s')
        text_width4, text_height4 = game_font.size(f'Pontos: {points}')
        text_width5, text_height5 = game_font.size(f'Recorde: {high_score}')
        text_width7, text_height7 = game_font.size("Pressione 'r' para reiniciar o jogo!")
        
        
        screen.fill(Colors.BLACK)
        text_surface = game_font.render('Parabéns!', False, Colors.YELLOW)
        screen.blit(text_surface, ((Game.WIDTH - text_width1) // 2, (Game.HEIGHT - text_height1 * 5) // 2))
        text_surface = game_font.render('Você Ganhou!!', False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width2) // 2, (Game.HEIGHT - text_height2 * 5) // 2 + text_height1))
        text_surface = game_font.render(f'Tempo: {finish_time:.2f}s', False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width3) // 2, (Game.HEIGHT - text_height3 * 5) // 2 + text_height2*2))
        text_surface = game_font.render(f'Pontos: {points}', False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width4) // 2, (Game.HEIGHT - text_height4 * 5) // 2 + text_height3*3))
        text_surface = game_font.render(f'Recorde: {high_score}', False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width5) // 2, (Game.HEIGHT - text_height5  * 5) // 2 + text_height4*4))
        text_surface = game_font.render("Pressione 'r' para reiniciar o jogo!", False, Colors.WHITE)
        screen.blit(text_surface, ((Game.WIDTH - text_width7) // 2, (Game.HEIGHT - text_height7  * 5) // 2 + text_height4*5))
        
        if high_score < points:
            text_width6, text_height6 = game_font.size('Novo Recorde!')
            text_surface = game_font.render('Novo Recorde!', False, Colors.YELLOW)
            screen.blit(text_surface, ((Game.WIDTH - text_width6) // 2, (Game.HEIGHT - text_height6 * 5) // 2 + text_height5*6))
            high_score = points
    
        for event in pygame.event.get():
            # Player Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return high_score, GameStatus.STARTED
            
            # Quit Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

def game_run(old_player_lifes = None, old_player_points = None, old_game_timer = None,
             old_fruits_rects = None, old_special_fruits_rects = None):

    # Select Map
    map_pos = game_map.MAPS[0]

    # Get elements pos from map    
    wall_array_rect, player, ghosts, fruits_rects, special_fruits_rects = get_elements_from_map(map_pos)
    start_timer = timer.time()

    # Verify saved Data
    if old_player_lifes is not None:
        player.lifes = old_player_lifes
    if old_player_points is not None:
        player.score = old_player_points
    if old_player_points is not None:
        start_timer = old_game_timer
    if old_fruits_rects is not None:
        fruits_rects = old_fruits_rects
    if old_special_fruits_rects is not None:
        special_fruits_rects = old_special_fruits_rects
    
    
    while True:
        # FPS
        time.tick(Game.FPS)
        
        # Screen Blit
        screen.fill(Colors.WHITE)
        game.fill(Game.BACKGROUND_COLOR)
        
        actual_time = timer.time()
        
        # Text
        text_surface = game_font.render(f'Vidas: {player.lifes}', False, Colors.BLACK)
        screen.blit(text_surface, (0, 0))
        text_width, _ = game_font.size(f'Pontos: {player.score}')
        text_surface = game_font.render(f'Pontos: {player.score}', False, Colors.BLACK)
        screen.blit(text_surface, (Game.WIDTH - text_width, 0))
        text_surface = game_font.render(f'Timer: {actual_time - start_timer:.2f}s', False, Colors.BLACK)
        screen.blit(text_surface, (200, 0))

        # TODO: Implement one for to all draw for performance
        # Draw Fruits
        for fruit_rect in fruits_rects:
            pygame.draw.circle(game, Colors.WHITE, fruit_rect.center, fruit_rect.width // 4)
            
        # Draw Special Fruits
        for special_fruit_rect in special_fruits_rects:
            pygame.draw.circle(game, Colors.WHITE, special_fruit_rect.center, special_fruit_rect.width // 3)
        
        # Blit Ghosts
        for ghost in ghosts:
            game.blit(pygame.transform.scale(pygame.image.load(f'assets/ghost_images/{ghost.image_file}.png'), (Game.TILE_SIZE, Game.TILE_SIZE)), ghost.rect)
        
        # Blit Player
        game.blit(player.image, player.rect)
        
        # Draw Walls
        for wall_rect in wall_array_rect:
            pygame.draw.rect(game, Wall.WALL_COLOR, wall_rect)

        game.blit(player.image, player.rect)

        # Game Surface Blit
        screen.blit(game, (0, 60))

        # Events
        for event in pygame.event.get():
            # Player Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    player.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    player.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    player.direction = Direction.DOWN
                if event.key == pygame.K_r:
                    return player.lifes, player.score, actual_time - start_timer, fruits_rects, special_fruits_rects, GameStatus.STARTED
            
            # Quit Event
            if event.type == pygame.QUIT:
                return player.lifes, player.score, actual_time - start_timer, fruits_rects, special_fruits_rects, GameStatus.STOPPED
            
        # Update Player Position
        # fruit_rect_list = [fruit.rect for fruit in fruits]
        #ghosts_rect_array = [ghost.rect for ghost in ghosts]
        for i,ghost in enumerate(ghosts):    
            if player.rect.colliderect(ghost.rect):
                if ghost.scape_ticks > 0:
                    player.score += 15
                    ghost.is_dead = True
                else:
                    player.lifes -= 1
                    return player.lifes, player.score, actual_time - start_timer, fruits_rects, special_fruits_rects, GameStatus.RESTARTED
        new_player_pos = player.update_player_position(Game, wall_array_rect)
        
        # Fruit Collision
        if len(fruits_rects) <= 100:
            return player.lifes, player.score, actual_time - start_timer, fruits_rects, special_fruits_rects, GameStatus.WIN
        
        for i, fruit_rect in enumerate(fruits_rects):
            if fruit_rect.colliderect(player.rect):
                player.score += 1
                fruits_rects.pop(i)
        
        # Special Fruit Collision
        player_got_special_fruit = False
        for i, special_fruit_rect in enumerate(special_fruits_rects):
            if special_fruit_rect.colliderect(player.rect):
                player.score += 10
                player_got_special_fruit = True
                special_fruits_rects.pop(i)

        # Update Ghost Position
        for ghost in ghosts:
            if player_got_special_fruit:
                ghost.scape_ticks = 100
            ghost_rect_array = [ghost2.rect for ghost2 in ghosts if ghost.rect != ghost2.rect]
            ghost.update_ghost_position(Game, wall_array_rect, player.rect, ghost_rect_array)

        # Update Display    
        pygame.display.update()

def game_over() -> GameStatus:
    screen.fill(Colors.BLACK)
    text_width, text_height = game_font.size('Game Over!')
    text_surface = game_font.render('Game Over!', False, Colors.YELLOW)
    screen.blit(text_surface, ((Game.WIDTH - text_width) // 2, (Game.HEIGHT - text_height) // 2))
    text_width, text_height = game_font.size("Pressione 'r' tecla para reiniciar!")
    text_surface = game_font.render("Pressione 'r' tecla para reiniciar!", False, Colors.WHITE)
    screen.blit(text_surface, ((Game.WIDTH - text_width) // 2, (Game.HEIGHT - text_height) // 2 + text_height))
    pygame.display.update()
    
    while True:    
        for event in pygame.event.get():
            # Player Event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:                
                    return GameStatus.STARTED
            
            # Quit Event
            if event.type == pygame.QUIT:
                return GameStatus.STOPPED

def start_variables():
    return None, None, None, None, None, GameStatus.STARTED

def main():
    high_score = 0
    start = True
    [
        player_lifes, player_points, game_time, 
        fruits_rects, special_fruits_rects, 
        game_status
    ] = start_variables()
    while True:
        if start:
            game_menu()
            start = False
        [
            player_lifes, player_points, game_time,
            fruits_rects, special_fruits_rects, 
            game_status
        ] = game_run(player_lifes, player_points, game_time, fruits_rects, special_fruits_rects)
        if player_loses_the_game(player_lifes):
            game_status = game_over()
            if game_status == GameStatus.STARTED:
                start = True
                [
                    player_lifes, player_points, game_time,
                    fruits_rects, special_fruits_rects, 
                    game_status
                ] = start_variables()
                continue
            else:
                break
        if player_closes_game(game_status):
            break
        if player_win_game(game_status):
            high_score, game_status = game_win(game_time, player_points, high_score)
            start = True
            [
                player_lifes, player_points, game_time,
                fruits_rects, special_fruits_rects, 
                game_status
            ] = start_variables()
    
    pygame.quit()
    sys.exit()

    
if __name__ == '__main__':
    main()
