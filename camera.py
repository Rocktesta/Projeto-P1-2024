import pygame
vector = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vector(0, 0)
        self.offset_float = vector(self.player.rect.center)  # Initialize to player's center
        self.DISPLAY_L = 1280
        self.DISPLAY_A = 720
        self.CONST = vector(-self.DISPLAY_L / 2 + self.DISPLAY_A / 2, -self.player.rect.y + self.DISPLAY_A / 2)

    def scroll(self):
        self.offset_float.x += ((self.player.rect.centerx - self.offset_float.x) + self.CONST.x)
        self.offset_float.y += ((self.player.rect.centery - self.offset_float.y) + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
        self.cam_view = pygame.Rect(self.offset.x, self.offset.y, self.DISPLAY_L, self.DISPLAY_A)
