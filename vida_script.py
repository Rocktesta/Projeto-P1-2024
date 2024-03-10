import pygame
from random import randint

def nova_posicao_item(player):
        # gera uma posição aleatória para o item
        pos = [randint(400,1200), randint(400, 600)]
        while pos[0] == player.rect.x:
            pos = [randint(100,1200), randint(400, 600)]
        return pos

class HealthBar:
    def __init__(self, x, y, largura, altura, vida):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida_max = 100
        self.vida_atual = vida

    def update(self, nova_vida):
        self.vida_atual = nova_vida

    def draw(self, tela):
        #barra inteira vida max
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, self.largura, self.altura))
        
        # tamanho restante
        largura_restante = (self.vida_atual / self.vida_max) * self.largura
        
        # barra de vida atual
        pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, largura_restante, self.altura))

class Coxinha(pygame.sprite.Sprite):
    def __init__(self, player):  #inicializa o objeto jogador
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player)
        self.x = self.pos[0]
        self.y = self.pos[1]
        image = pygame.image.load('Image\itens\health_box.png')
        self.image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.vida = 10
        self.render = True

    def draw(self, tela):
        if self.render:
            tela.blit(self.image, self.rect)

    def update(self, player):
        vida = 0
        if self.rect.colliderect(player) == 1:
            vida += self.vida
            self.render = False
        return vida


        
