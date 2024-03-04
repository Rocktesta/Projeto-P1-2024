import pygame


class Piso:  #classe do jogador
    def __init__(self, x, y, largura=2000, altura=10):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, largura, altura)
        