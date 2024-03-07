import pygame
class Coxinha:
    def __init__(self, x, y, largura, altura):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, 25, 25)
        self.vida = 10
        self.largura = largura
        self.altura = altura
        
    def draw(self, tela):
        pygame.draw.rect(tela, (255, 255, 255), (self.rect.x, self.rect.y, self.largura, self.altura))

        
