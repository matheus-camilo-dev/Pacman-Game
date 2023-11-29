class GameConstants:
    def __init__(self, tile_prorportion):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.TILE_SIZE = self.WIDTH * tile_prorportion
        self.FPS = 5
        self.BACKGROUND_COLOR = Colors.BLACK

class GameStatus:
    STARTED = 0     # A new Game is started
    RESTARTED = 1   # Player loses life
    LOSE = 2        # Player loses the game
    STOPPED = 3     # Player quit 
    WIN = 4         # Player win the game


class DirectionConstants:
    STOP = 0
    LEFT = -1
    UP = -2
    RIGHT = 1
    DOWN = 2


class WallConstants:
    def __init__(self, tileSize):
        self.WALL_SIZE = (tileSize, tileSize)
        self.WALL_COLOR = Colors.GREEN


class MapsElements:
    VOID = 0
    WALL = 1
    PACMAN = 2
    GHOST = 3
    FRUIT = 4
    ESPECIAL_FRUIT = 5


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128,0,128)


def player_loses_the_game(player_lifes : int) -> bool:
    return player_lifes == 0


def player_closes_game(game_status : GameStatus) -> bool:
    return game_status == GameStatus.STOPPED


def player_loses_life(game_status : GameStatus) -> bool:
    return game_status == GameStatus.RESTARTED


def player_restart_the_game(game_status : GameStatus) -> bool:
    return game_status == GameStatus.STARTED


def player_win_game(game_status : GameStatus) -> bool:
    return game_status == GameStatus.WIN
