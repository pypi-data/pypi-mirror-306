import pygame
import math
import random


class NPC:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y

    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


class RaycastingEngine:

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    BLACK = (0, 0, 0)
    FOV = math.pi / 3  # Field of view
    SCALE = SCREEN_WIDTH // 120  # Scale of the projection

    NUM_RAYS = 120  # Number of rays to cast
    MAX_DEPTH = 800  # Maximum depth to render

    MAP = None

    MAP_WIDTH = None
    MAP_HEIGHT = None
    TILE_SIZE = 64  # Size of a tile (in pixels)

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.player_x = 100
        self.player_y = 100
        self.player_angle = 0
        self.player_speed = 0.5
        self.turn_speed = 0.01
        self.screen = None
        self.loaded_sprites = {}  # Dictionary to cache loaded sprites
        self.sprite_requests = []  # List to hold sprite rendering requests
        self.sprites = []
        self.message_queue = []  # Queue for storing messages
        self.text_to_display = []  # List to hold text elements to display
        self.current_message_index = 0
        self.hud_text = []
        self.npcs = []
        self.font = pygame.font.Font(None, 30)  # Default font size
        self.wall_texture = None

    def init_screen(self):
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)
        self.load_textures()

    def load_textures(self):
        self.wall_texture = pygame.image.load("wall_texture.png").convert()

    def set_map(self, map_data):
        self.MAP = map_data
        self.MAP_WIDTH = len(self.MAP[0])
        self.MAP_HEIGHT = len(self.MAP)

    def set_hud_text(self, text, position=(0, 0), font_size=24,
                     color=(255, 255, 255), centered=False):
        # Set text to display on the heads-up display (HUD).
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        if centered:
            position = (
                position[0] -
                text_surface.get_width() //
                2,
                position[1] -
                text_surface.get_height() //
                2)
        self.hud_text.append((text_surface, position))

    def render_hud(self):
        # Render the heads-up display (HUD) text on the screen.
        for text_surface, position in self.hud_text:
            self.screen.blit(text_surface, position)

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

                    # Calculate texture coordinates
                    texture_x = int(
                        (target_x %
                         self.TILE_SIZE) /
                        self.TILE_SIZE *
                        self.wall_texture.get_width())
                    texture_slice = self.wall_texture.subsurface(
                        texture_x, 0, 1, self.wall_texture.get_height())
                    texture_slice = pygame.transform.scale(
                        texture_slice, (self.SCALE, int(wall_height)))

                    # Draw the wall slice
                    self.screen.blit(
                        texture_slice,
                        (ray *
                         self.SCALE,
                         self.SCREEN_HEIGHT //
                         2 -
                         wall_height //
                         2))
                    break

    def is_collision(self, x, y):
        buffer = 5
        map_x = int(x // self.TILE_SIZE)
        map_y = int(y // self.TILE_SIZE)
        if map_x < 0 or map_x >= self.MAP_WIDTH or map_y < 0 or map_y >= self.MAP_HEIGHT:
            return True
        if self.MAP[map_y][map_x] == 1:
            return True
        if self.MAP[int((y - buffer) // self.TILE_SIZE)
                    ][map_x] == 1 or self.MAP[int((y + buffer) // self.TILE_SIZE)][map_x] == 1:
            return True
        if self.MAP[map_y][int((x - buffer) // self.TILE_SIZE)
                           ] == 1 or self.MAP[map_y][int((x + buffer) // self.TILE_SIZE)] == 1:
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
                self.loaded_sprites[sprite_path] = pygame.image.load(
                    sprite_path).convert_alpha()
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
            screen_x = (self.SCREEN_WIDTH / 2) + \
                (angle_difference * (self.SCREEN_WIDTH / self.FOV))
            sprite_size = int(5000 / (distance + 0.0001))
            scaled_sprite = pygame.transform.scale(
                sprite_image, (sprite_size, sprite_size))
            self.screen.blit(
                scaled_sprite,
                (screen_x -
                 sprite_size //
                 2,
                 self.SCREEN_HEIGHT //
                 2 -
                 sprite_size //
                 2))

    def set_text(self, text, position=(0, 0), font_size=24,
                 color=(255, 255, 255), centered=False):
        # Use the font initialized in __init__ for consistency
        lines = text.split('\n')  # Split text into lines
        total_height = 0  # To accumulate the total height of all lines

        # Create a list to hold text surfaces and calculate total height
        text_surfaces = []
        for line in lines:
            text_surface = self.font.render(line, True, color)
            text_surfaces.append(text_surface)
            total_height += text_surface.get_height() + 5  # 5 pixels spacing

            if text_surface.get_width() > self.SCREEN_WIDTH:
                print(f"Warning: Text exceeds screen width: {line}")

        if centered:
            # Calculate the starting y position to center the text vertically
            start_y = (self.SCREEN_HEIGHT - total_height) // 2
            # Center each line horizontally
            for i, text_surface in enumerate(text_surfaces):
                # Calculate the x position to center the line
                start_x = (self.SCREEN_WIDTH - text_surface.get_width()) // 2
                # Append the rendered text surface and its position
                self.text_to_display.append(
                    (text_surface, (start_x, start_y + i * (font_size + 5))))
        else:
            # If not centered, just position it based on the provided
            # coordinates
            for i, text_surface in enumerate(text_surfaces):
                self.text_to_display.append(
                    (text_surface, (position[0], position[1] + i * (font_size + 5))))

    def add_npc(self, npc_path, npc_x, npc_y):
        # Add a non-player character to the level.
        npc = NPC(npc_path, npc_x, npc_y)
        self.npcs.append(npc)

    def move_npcs(self):
        # Move all NPCs to new positions.
        for npc in self.npcs:
            npc.move()

    def render_npcs(self):
        # Render all NPCs on the screen.
        for npc in self.npcs:
            npc.render(self.screen)

    def render_texts(self):
        # Render all text elements on screen.
        for text_surface, position in self.text_to_display:
            self.screen.blit(text_surface, position)
        # self.text_to_display.clear()  # Clear text after rendering

    def set_external_text(self, text, position=(
            10, 10), font_size=24, color=(255, 255, 255), centered=False):
        # Sets text on the screen for the given raycasting engine instance.
        self.message_queue.append((text, position, font_size, color, centered))

    def display_current_message(self):
        # Check if there is a message to display.
        if self.current_message_index < len(self.message_queue):
            text, position, font_size, color, centered = self.message_queue[
                self.current_message_index]
            self.set_text(text, position, font_size, color, centered)
        else:
            # Clear texts when no messages remain.
            self.text_to_display.clear()

    def run_game(self):
        pygame.init()
        self.init_screen()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        # Move to the next message when ENTER is pressed
                        self.current_message_index += 1
                        self.text_to_display.clear()  # Clear previous text

            self.screen.fill(self.BLACK)
            self.move_player()
            self.cast_rays()

            # Queue each sprite in the level for rendering
            for sprite_path, x, y in self.sprites:
                self.render_sprite(sprite_path, x, y)

            self.process_sprites()  # Process all sprite rendering requests

            self.move_npcs()  # Move all non-player characters

            self.render_npcs()  # Render all non-player characters

            # Display the current message on the screen
            self.display_current_message()

            self.render_texts()  # Render all text elements on screen
            self.render_hud()  # Render the heads-up display (HUD) text on screen

            pygame.display.flip()  # Update the full display Surface to the screen

        pygame.quit()


# Usage example
if __name__ == "__main__":
    engine = RaycastingEngine()
    engine.init_screen()
    engine.set_text("Health: 100", (200, 120))
    engine.set_text("Money: 50", (200, 140))
    engine.render_texts()
    engine.run_game()
