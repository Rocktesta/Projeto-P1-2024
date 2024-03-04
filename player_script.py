import pygame
#Script do player

class Player:  #classe do jogador
    def __init__(self, x, y, largura, altura, sprite):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, largura, altura)
        self.vida = 90
        self.municao = 30
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.pulo = False
        self.sprite = sprite

    def movimento(self):
        tela_scroll = 0
        round(self.velocidade_x)
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        if self.rect.right > 1280 - 200 or self.rect.left < 200:
            self.rect.x -= self.velocidade_x
            tela_scroll = -self.velocidade_x
        return tela_scroll

             

        
