import pygame

class Municao:
    def __init__(self, x, y): # incializa objeto municao com quantidade = 10
        self.rect = pygame.Rect(x, y,  40, 12)
        self.qnt = 10