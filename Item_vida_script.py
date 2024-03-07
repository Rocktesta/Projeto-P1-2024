import pygame
class Coxinha:
    def __init__(self, x, y, largura, altura):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, 25, 25)
        self.vida = 10
        self.largura = largura
        self.altura = altura
        self.render = True
        
    def draw(self, tela):
        if self.render:
            pygame.draw.rect(tela, (255, 255, 255), (self.rect.x, self.rect.y, self.largura, self.altura))

    def update(self, player):
        vida = 0
        if self.rect.colliderect(player) == 1:
            vida += self.vida
            self.render = False
        return vida


        
