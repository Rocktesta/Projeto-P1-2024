import pygame
import os
import numpy
import player_script
from player_script import Bullet
import weapons
from weapons import Missil
from pygame.sprite import Group

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 500
        self.vivo = True
        self.speed = 5
        self.direcao = 1
        self.velocidade = 7
        self.vel_y = 0
        self.shoot_laser_cooldown = 0
        self.flip = True
        self.no_canto = False
        self.lista_animacoes = []
        self.frame_index = 0
        self.action = 0
        self.x = x
        self.y = y 
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run',  'Win']
        for animation in animation_types:
            lista_temp = []
            num_frames = len(os.listdir(f'Image\Sprites\\boss\{animation}'))
            for i in range(num_frames):
                img = pygame.image.load(f'Image\Sprites\\boss\{animation}\\boss_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3.5, img.get_height() * 3.5))
                lista_temp.append(img) 
            self.lista_animacoes.append(lista_temp)
        
        self.image = self.lista_animacoes[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.lista_animacoes[0][0])
        self.imagem_mask = self.mask.to_surface()
        self.imagem_mask.set_colorkey((0, 0, 0))
        self.rect.center = (x, y)

    def update(self):
        self.update_animacao()
        # update cooldown laser
        if self.shoot_laser_cooldown > 0:
            self.shoot_laser_cooldown -= 1

    def update_animacao(self):
        cooldown_animacao = 100
		#update da imagem dependendo do frame
        self.image = self.lista_animacoes[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > cooldown_animacao:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out the reset back to the start
        if self.frame_index >= len(self.lista_animacoes[self.action]):
            if self.action == 3:
                self.frame_index = len(self.lista_animacoes[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, nova_acao):
        # checa se a nova ação é deferente da ação anterior
        if nova_acao != self.action:
            self.action = nova_acao
            # update do cooldown da animação
            if self.action == 0:
                self.cooldown_animacao = 300 # cooldown da ação de Idle
            elif self.action == 1:
                self.cooldown_animacao = 100 # cooldown da ação de Run
            elif self.action == 2:
                self.cooldown_animacao = 100 # cooldown da ação de shoot_laser
            elif self.action == 3:
                self.cooldown_animacao = 100 # cooldown da ação de Death
            elif self.action == 4:
                self.cooldown_animacao = 100 # cooldown da ação de Win
            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def shoot_laser(self):
        if self.shoot_laser_cooldown == 0:
            self.shoot_laser_cooldown = 50 # cooldown do tiro
            laser_bullet = Bullet('bullet_laser', self.rect.centerx + (0.32 * self.rect.size[0] * self.direcao), self.rect.centery - 20, self.direcao, 10)
            inimigo_bullet_group.add(laser_bullet)

    def shoot_missil(self, player):
        missil1 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 20, 0.7)
        missil2 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 25, 0.5)
        missil3 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 30, 0.45)
        missil_group.add(missil1, missil2, missil3)

    def big_run(self, player):
        if self.no_canto == False:
            self.rect.x -= self.velocidade * self.direcao
            self.update_action(1) # ação de correr
            if self.rect.colliderect(player.rect):
                player.vida -= 0.2 # dano da corrida
            if self.rect.right >= 1280:
                print(self.rect.x)
                self.direcao = -1
                self.flip = True
                self.no_canto = True
            elif self.rect.left <= 0:
                print(self.rect.x)
                self.direcao = 1
                self.flip = False 
                self.no_canto = True  
        else:
            self.update_action(0) #ação de idle
            return
            

    def laser_beam(self):
        pass

    def ai(self, player):
        if self.vivo:
            # se o player estiver na tela a luta inicia
            if player.rect.x > 0:
                self.big_run(player) # corrida até o outro lado da tela
                if self.action == 0:
                    self.shoot_missil(player)

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


def bossfight():
    pass

# sprite groups
inimigo_bullet_group = player_script.inimigo_bullet_group
missil_group = weapons.missil_group