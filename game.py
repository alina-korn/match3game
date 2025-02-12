import pygame
import random

# Настройки экрана
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 8
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 60

# Цвета плиток
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match-3 Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Класс для плитки
class Tile:
    def __init__(self, x, y, color):
        self.color = color
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.x, self.y = x, y

# Генерация игрового поля
board = [[Tile(x, y, random.choice(COLORS)) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
selected_tile = None
score = 0

def draw_board():
    screen.fill(WHITE)
    for row in board:
        for tile in row:
            pygame.draw.rect(screen, tile.color, tile.rect)
            pygame.draw.rect(screen, BLACK, tile.rect, 3)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def swap_tiles(tile1, tile2):
    board[tile1.y][tile1.x], board[tile2.y][tile2.x] = board[tile2.y][tile2.x], board[tile1.y][tile1.x]
    tile1.x, tile2.x = tile2.x, tile1.x
    tile1.y, tile2.y = tile2.y, tile1.y
    tile1.rect.topleft = (tile1.x * TILE_SIZE, tile1.y * TILE_SIZE)
    tile2.rect.topleft = (tile2.x * TILE_SIZE, tile2.y * TILE_SIZE)

def check_matches():
    matches = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if board[y][x].color == board[y][x + 1].color == board[y][x + 2].color:
                matches.extend([(x, y), (x + 1, y), (x + 2, y)])
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if board[y][x].color == board[y + 1][x].color == board[y + 2][x].color:
                matches.extend([(x, y), (x, y + 1), (x, y + 2)])
    return list(set(matches))

def remove_matches(matches):
    global score
    for x, y in matches:
        board[y][x] = None
        score += 10

def apply_gravity():
    for x in range(GRID_SIZE):
        empty_y = None
        for y in reversed(range(GRID_SIZE)):
            if board[y][x] is None:
                if empty_y is None:
                    empty_y = y
            elif empty_y is not None:
                board[empty_y][x] = board[y][x]
                board[empty_y][x].y = empty_y
                board[empty_y][x].rect.topleft = (x * TILE_SIZE, empty_y * TILE_SIZE)
                board[y][x] = None
                empty_y -= 1
        for y in range(GRID_SIZE):
            if board[y][x] is None:
                board[y][x] = Tile(x, y, random.choice(COLORS))

def game_loop():
    global selected_tile
    running = True
    while running:
        draw_board()
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
                if selected_tile is None:
                    selected_tile = board[y][x]
                else:
                    if abs(selected_tile.x - x) + abs(selected_tile.y - y) == 1:
                        swap_tiles(selected_tile, board[y][x])
                        matches = check_matches()
                        if matches:
                            remove_matches(matches)
                            apply_gravity()
                        else:
                            swap_tiles(selected_tile, board[y][x])  # Откат хода, если нет совпадений
                    selected_tile = None
    pygame.quit()

if __name__ == "__main__":
    game_loop()