import pygame
import numpy
import math
import os
from pygame.sprite import Group

#Scrpits para as armas e balas
def nova_posicao_item(player, tela_scroll):
        # gera uma posição aanguloatória para o item
        pos = [numpy.random.randint(400,1200) + tela_scroll, numpy.random.randint(300, 500) + tela_scroll]
        while pos[0] == player.rect.x:
            pos = [numpy.random.randint(100,1200), numpy.random.randint(400, 600)]
        return pos

class Shotgun(pygame.sprite.Sprite):
    def __init__(self, player, tela_scroll=0, sprite="Weapons\Shotgun_sprite.png", cooldown=1, escala=3):
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player, tela_scroll)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * escala, self.sprite.get_height() * escala))
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        self.cooldown = cooldown
        self.equipada = False
        self.player = player

    @staticmethod
    def gerar_shotgun(player, tela_scroll=0):
        shotgun_group = pygame.sprite.Group()
        if numpy.random.randint(1, 5) == 1:
            shotgun = Shotgun(player, tela_scroll) 
            shotgun_group.add(shotgun)
        return shotgun_group

    def draw(self, tela):
        if self.equipada == False:
            tela.blit(self.sprite, (self.rect.x , self.y))

    def update(self, player):
        if self.rect.colliderect(player) and not player.shotgun_equip:
            player.shotgun_equip = True
            self.kill()

    '''def draw_blast(self, tela, player):
        cooldown_animacao = 50  

        if pygame.time.get_ticks() - self.update_time > cooldown_animacao:
            self.update_time = pygame.time.get_ticks()  
            print('atualizando quadro')
            self.frame_index += 1
            if self.frame_index >= self.num_frames:
                self.frame_index = 0

            print('desenhando quadro')
            tela.blit(self.blast_list[self.frame_index], (self.player.rect.x + (200 * player.direcao) , self.player.rect.centery - 200))'''
    
            
class ShotgunBlast(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] 
        for n in range(len(os.listdir(f'Weapons')) - 1):
            img = pygame.image.load(f'Weapons\Shotgun_blast{n}.png')
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self):
        velocidade_blast = 4
        self.contador += 1
        if self.contador >= velocidade_blast and self.frame_index < len(self.images) - 1:
            self.contador = 0
            self.frame_index += 1
            self.image = self.images[self.frame_index]
        # animação completa reset frame index
        if self.frame_index >= len(self.images) - 1 and self.contador >= velocidade_blast:
            self.kill()

class Missil(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, altura, gravidade):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image\\bullet\\bullet_laser.png')
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.speed = 10 # velocidade do míssil
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.distance_to_target = math.sqrt((target_pos[0] - start_pos[0]) ** 2 + (target_pos[1] - start_pos[1]) ** 2)
        self.dx = (target_pos[0] - start_pos[0]) / self.distance_to_target
        self.dy = (target_pos[1] - start_pos[1]) / self.distance_to_target
        self.angle = math.atan2(-self.dy, self.dx)
        self.gravidade = gravidade
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle) - altura

    def update(self, player):
        self.rect.x += self.vx
        self.vy += self.gravidade
        self.rect.y += self.vy
        # Verifique se o míssil atingiu o jogador
        if self.rect.colliderect(player.rect):
            #player.vida -= 30 # dano do míssil
            self.kill()

# Sprite Grups       
weapons_group = pygame.sprite.Group()
shotgun_blast_group = pygame.sprite.Group() 
missil_group = pygame.sprite.Group()