import pygame
#Scrpits para as armas

altura = 10
largura = 20

class Municao:
    def __init__(self, x, y): # incializa objeto municao com quantidade = 10
        self.rect = pygame.Rect(x, y,  40, 12)
        self.qnt = 10

class Pistol: #pistola
    def __init__(self, x, y, altura, largura):
        self.rect = pygame.Rect(x, y, 20, 10)

    def update_position(self, x, y):
        # Atualiza a posição da pistola para acompanhar o jogador
        self.rect.x = x + 35  # Ajuste conforme necessário para a posição da pistola em relação ao jogador
        self.rect.y = y + 5  # Ajuste conforme necessário para a posição da pistola em relação ao jogador
