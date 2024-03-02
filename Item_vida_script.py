import pygame
class Coxinha:
    def __init__(self, x, y):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, 25, 25)
        self.vida = 10

