import pygame
import math

class RaycastingEngine:
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

    def __init__(self):
        self.player_x = 100
        self.player_y = 100
        self.player_angle = 0
        self.player_speed = 0.8
        self.turn_speed = 0.03
        self.screen = None
        self.loaded_sprites = {}  # Dictionary to cache loaded sprites
        self.sprite_requests = []  # List to hold sprite rendering requests
        self.sprites = []

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def add_sprite(self, sprite_path, x, y):
        # Add a sprite with a specific position.
        self.sprites.append((sprite_path, x, y))

    def cast_rays(self):
        start_angle = self.player_angle - self.FOV / 2
        for ray in range(self.NUM_RAYS):
            ray_angle = start_angle + ray * self.FOV / self.NUM_RAYS
            for depth in range(self.MAX_DEPTH):
                target_x = self.player_x + depth * math.cos(ray_angle)
                target_y = self.player_y + depth * math.sin(ray_angle)
                
                map_x = int(target_x // self.TILE_SIZE)
                map_y = int(target_y // self.TILE_SIZE)
                
                if map_x >= self.MAP_WIDTH or map_y >= self.MAP_HEIGHT or map_x < 0 or map_y < 0:
                    break
                if self.MAP[map_y][map_x] == 1:
                    depth *= math.cos(self.player_angle - ray_angle)
                    wall_height = 20000 / (depth + 0.0001)
                    color_intensity = 255 / (1 + depth * 0.01)
                    color = (color_intensity, color_intensity, color_intensity)
                    
                    pygame.draw.rect(self.screen, color, (ray * self.SCALE, self.SCREEN_HEIGHT // 2 - wall_height // 2, self.SCALE, wall_height))
                    break

    def is_collision(self, x, y):
        buffer = 5
        map_x = int(x // self.TILE_SIZE)
        map_y = int(y // self.TILE_SIZE)
        if map_x < 0 or map_x >= self.MAP_WIDTH or map_y < 0 or map_y >= self.MAP_HEIGHT:
            return True
        if self.MAP[map_y][map_x] == 1:
            return True
        if self.MAP[int((y - buffer) // self.TILE_SIZE)][map_x] == 1 or self.MAP[int((y + buffer) // self.TILE_SIZE)][map_x] == 1:
            return True
        if self.MAP[map_y][int((x - buffer) // self.TILE_SIZE)] == 1 or self.MAP[map_y][int((x + buffer) // self.TILE_SIZE)] == 1:
            return True
        return False

    def move_player(self):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.player_x, self.player_y

        if keys[pygame.K_w]:
            new_x += self.player_speed * math.cos(self.player_angle)
            new_y += self.player_speed * math.sin(self.player_angle)
        if keys[pygame.K_s]:
            new_x -= self.player_speed * math.cos(self.player_angle)
            new_y -= self.player_speed * math.sin(self.player_angle)

        if not self.is_collision(new_x, new_y):
            self.player_x, self.player_y = new_x, new_y

        if keys[pygame.K_a]:
            self.player_angle -= self.turn_speed
        if keys[pygame.K_d]:
            self.player_angle += self.turn_speed

    def load_sprite(self, sprite_path):
        if sprite_path not in self.loaded_sprites:
            try:
                self.loaded_sprites[sprite_path] = pygame.image.load(sprite_path).convert_alpha()
            except pygame.error as e:
                print(f"Failed to load sprite: {e}")
        return self.loaded_sprites[sprite_path]

    def render_sprite(self, sprite_path, sprite_x, sprite_y):
        # Add a sprite to the render queue.
        self.sprite_requests.append((sprite_path, sprite_x, sprite_y))

    def process_sprites(self):
        # Process all queued sprite rendering requests.
        for sprite_path, sprite_x, sprite_y in self.sprite_requests:
            self.render_single_sprite(sprite_path, sprite_x, sprite_y)
        self.sprite_requests.clear()  # Clear requests after processing

    def render_single_sprite(self, sprite_path, sprite_x, sprite_y):
        sprite_image = self.load_sprite(sprite_path)
        
        dx = sprite_x - self.player_x
        dy = sprite_y - self.player_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        angle_to_sprite = math.atan2(dy, dx)
        angle_difference = angle_to_sprite - self.player_angle
        if angle_difference > math.pi:
            angle_difference -= 2 * math.pi
        if angle_difference < -math.pi:
            angle_difference += 2 * math.pi
        half_fov = self.FOV / 2
        if -half_fov < angle_difference < half_fov:
            screen_x = (self.SCREEN_WIDTH / 2) + (angle_difference * (self.SCREEN_WIDTH / self.FOV))
            sprite_size = int(5000 / (distance + 0.0001))
            scaled_sprite = pygame.transform.scale(sprite_image, (sprite_size, sprite_size))
            self.screen.blit(scaled_sprite, (screen_x - sprite_size // 2, self.SCREEN_HEIGHT // 2 - sprite_size // 2))

    def run_game(self):
        pygame.init()
        self.init_screen()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.BLACK)
            self.move_player()
            self.cast_rays()
            # Queue each sprite in the level for rendering
            for sprite_path, x, y in self.sprites:
                self.render_sprite(sprite_path, x, y)

            self.process_sprites()  # Process all sprite rendering requests

            pygame.display.flip()

        pygame.quit()

# Usage example
if __name__ == "__main__":
    rc = RaycastingEngine()
    rc.run_game()
