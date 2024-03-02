import pygame
vector = pygame.math.Vector2

class Camera:
    def __init__(self):
        self.offset = vector(0, 0)
        self.velocidade_x = 0.1
        self.velocidade_y = 0.1
        self.posicao_x = 0
        self.posicao_y = 0
    def scroll(self):
        keys = pygame.key.get_pressed()
        # Camera movement
        if keys[pygame.K_q]:
            self.posicao_x += self.velocidade_x
        if keys[pygame.K_e]:
            self.posicao_x -= self.velocidade_x
        if keys[pygame.K_f]:
            self.posicao_y += self.velocidade_y
        if keys[pygame.K_v]:
            self.posicao_y -= self.velocidade_y