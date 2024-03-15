import pygame
import numpy


def nova_posicao_item(player, tela_scroll):
        # gera uma posição aleatória para o item
        pos = [numpy.random.randint(400,1200) + tela_scroll, numpy.random.randint(300, 400) + tela_scroll]
        while pos[0] == player.rect.x:
            pos = [numpy.random.randint(100,1200), numpy.random.randint(400, 600)]
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
    def __init__(self, player, tela_scroll=0):  #inicializa o objeto jogador
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player, tela_scroll)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.images = player.coxinha
        self.rect = self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vida = 10
        self.render = True
        self.cooldown_animacao = 100
        self.update_tempo = 0
        self.frame_index = 0

    @staticmethod
    def gerar_coxinhas(player, tela_scroll=0):
        coxinhas_group = pygame.sprite.Group()
        if numpy.random.randint(1, 7) == 1:
            quantidade_coxinhas = numpy.random.randint(1, 3)
            for _ in range(quantidade_coxinhas):
                coxinha = Coxinha(player, tela_scroll) 
                coxinhas_group.add(coxinha)
        return coxinhas_group
    
    def draw(self, tela):
        if self.render:
            sprite = self.images[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 14:
                self.frame_index = 0
            tela.blit(sprite, (self.rect.x - 50, self.rect.y - 40))

    def update(self, player):
        vida = 0
        if self.rect.colliderect(player.rect) == 1:
            if player.vida < player.max_vida:
                vida += self.vida
                self.render = False
        return vida


        