import pygame

class healthBar():
    def __init__(self, x, y, largura, altura, vida):
        vida_max = 100
        self.rect = pygame.rect.Rect(x, y, (largura * (10)), altura)
        self.rect_remain = pygame.rect.Rect(x, y, (20), altura)
    