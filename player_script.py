import pygame
#Script do player

class Player:  #classe do jogador
    def __init__(self, x, y, largura, altura):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, largura, altura)
        self.vida = 100
        self.municao = 30
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.pulo = False

    def movimento(self):
        round(self.velocidade_x)

        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        
