import pygame
vector = pygame.math.Vector2

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vector(0, 0)
        self.velocidade_x = 5
        self.velocidade_y = 5
        self.posicao_x = 0
        self.posicao_y = 0
    def scroll(self):
        keys = pygame.key.get_pressed()
        # Camera movement
        if keys[pygame.K_LEFT]:
            self.posicao_x += self.velocidade_x
        if keys[pygame.K_RIGHT]:
            self.posicao_x -= self.velocidade_x
        if keys[pygame.K_UP]:
            self.posicao_y += self.velocidade_y
        if keys[pygame.K_DOWN]:
            self.posicao_y -= self.velocidade_y