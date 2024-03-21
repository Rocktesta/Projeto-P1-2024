import pygame
from pygame import mixer
import numpy

mixer.init()
# carregando sons
comendo_coxinha0 = mixer.Sound('Audio\Coxinha\comendo_mine.wav')
comendo_coxinha1 = mixer.Sound('Audio\Coxinha\comendo_delicious.wav')
comendo_coxinha2 = mixer.Sound('Audio\Coxinha\comendo_mine_delicious.wav')

def nova_posicao_item(player, tela_scroll):
        # gera uma posição aleatória para o item
        pos = [numpy.random.randint(400,1200) + tela_scroll, numpy.random.randint(300, 400) + tela_scroll]
        while pos[0] == player.rect.x:
            pos = [numpy.random.randint(100,1200), numpy.random.randint(400, 600)]
        return pos

class HealthBar:    # classe da barra de vida do player
    def __init__(self, x, y, largura, altura, vida):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida_max = 100
        self.vida_atual = vida

    def update(self, nova_vida): 
        self.vida_atual = nova_vida

    def draw(self, tela):   # variacao de tamanho da barra verde em relacao a vermelha
        #barra inteira vida max
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, self.largura, self.altura))
        
        # tamanho restante
        largura_restante = (self.vida_atual / self.vida_max) * self.largura
        
        # barra de vida atual
        pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, largura_restante, self.altura))

class Coxinha(pygame.sprite.Sprite):    # classe coxinha, objeto de vida
    def __init__(self, player, tela_scroll=0):  #inicializa o objeto jogador
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player, tela_scroll)   # utilizado pelo staticmethod, para spawns
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.images = player.coxinha
        self.rect = self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.rect.x = self.x
        self.rect.y = self.y
        self.vida = 15
        self.render = True
        self.cooldown_animacao = 100
        self.update_tempo = 0
        self.frame_index = 0

    @staticmethod   # spawn aleatorio com base na pos do player
    def gerar_coxinhas(player, tela_scroll=0):
        coxinhas_group = pygame.sprite.Group()
        if numpy.random.randint(1, 4) == 1: # n aleatorio de 1 a 4 (chance de spawn)
            quantidade_coxinhas = numpy.random.randint(1, 3) # quantidade de spawn
            for _ in range(quantidade_coxinhas):    # para a quantidade a spawnar
                coxinha = Coxinha(player, tela_scroll) 
                coxinhas_group.add(coxinha)
        return coxinhas_group
    
    def draw(self, tela):   # render das coxinhas
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

    def update(self, player):   # se colliderect com player, add vida (afeta a barra, player.vida += vida)
        vida = 0
        if self.rect.colliderect(player.rect) == 1:
            if player.vida < player.max_vida:
                n_som = numpy.random.randint(0,3)
                if n_som == 0:
                    comendo_coxinha0.play()
                elif n_som == 1:
                    comendo_coxinha1.play()
                else:
                    comendo_coxinha2.play()
                vida += self.vida
                self.render = False
        return vida


        