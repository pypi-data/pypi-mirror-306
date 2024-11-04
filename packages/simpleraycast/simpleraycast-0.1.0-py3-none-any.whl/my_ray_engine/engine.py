import pygame
import math

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FOV = math.pi / 3  # Field of view (60 degrees)
NUM_RAYS = 120     # Number of rays to cast
MAX_DEPTH = 800    # Maximum depth for the rays
SCALE = SCREEN_WIDTH // NUM_RAYS  # Scaling factor for rendering

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Map (1 represents a wall, 0 is an empty space)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
TILE_SIZE = 64  # Size of a tile (in pixels)

# Player settings
player_x = 100
player_y = 100
player_angle = 0
player_speed = 0.8
turn_speed = 0.03

# Initialize Pygame screen
screen = None

def init_screen():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def cast_rays():
    start_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * FOV / NUM_RAYS
        for depth in range(MAX_DEPTH):
            target_x = player_x + depth * math.cos(ray_angle)
            target_y = player_y + depth * math.sin(ray_angle)
            
            map_x = int(target_x // TILE_SIZE)
            map_y = int(target_y // TILE_SIZE)
            
            if map_x >= MAP_WIDTH or map_y >= MAP_HEIGHT or map_x < 0 or map_y < 0:
                break
            if MAP[map_x][map_y] == 1:
                depth *= math.cos(player_angle - ray_angle)
                wall_height = 20000 / (depth + 0.0001)
                color_intensity = 255 / (1 + depth * 0.01)
                color = (color_intensity, color_intensity, color_intensity)
                
                pygame.draw.rect(screen, color, (ray * SCALE, SCREEN_HEIGHT // 2 - wall_height // 2, SCALE, wall_height))
                break

def is_collision(x, y):
    buffer = 5
    map_x = int(x // TILE_SIZE)
    map_y = int(y // TILE_SIZE)
    if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
        return True
    if MAP[map_y][map_x] == 1:
        return True
    if MAP[int((y - buffer) // TILE_SIZE)][map_x] == 1 or MAP[int((y + buffer) // TILE_SIZE)][map_x] == 1:
        return True
    if MAP[map_y][int((x - buffer) // TILE_SIZE)] == 1 or MAP[map_y][int((x + buffer) // TILE_SIZE)] == 1:
        return True
    return False

def move_player():
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y

    if keys[pygame.K_w]:
        new_x += player_speed * math.cos(player_angle)
        new_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        new_x -= player_speed * math.cos(player_angle)
        new_y -= player_speed * math.sin(player_angle)

    if not is_collision(new_x, new_y):
        player_x, player_y = new_x, new_y

    if keys[pygame.K_a]:
        player_angle -= turn_speed
    if keys[pygame.K_d]:
        player_angle += turn_speed

def render_sprite(sprite_image, sprite_x, sprite_y):
    dx = sprite_x - player_x
    dy = sprite_y - player_y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle_to_sprite = math.atan2(dy, dx)
    angle_difference = angle_to_sprite - player_angle
    if angle_difference > math.pi:
        angle_difference -= 2 * math.pi
    if angle_difference < -math.pi:
        angle_difference += 2 * math.pi
    half_fov = FOV / 2
    if -half_fov < angle_difference < half_fov:
        screen_x = (SCREEN_WIDTH / 2) + (angle_difference * (SCREEN_WIDTH / FOV))
        sprite_size = int(5000 / (distance + 0.0001))
        scaled_sprite = pygame.transform.scale(sprite_image, (sprite_size, sprite_size))
        screen.blit(scaled_sprite, (screen_x - sprite_size // 2, SCREEN_HEIGHT // 2 - sprite_size // 2))

def run_game():
    global screen
    pygame.init()
    init_screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        move_player()
        cast_rays()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    run_game()
