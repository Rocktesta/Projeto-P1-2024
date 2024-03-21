import pygame
from pygame import mixer
import os
import numpy
import player_script
from player_script import Bullet
import weapons
from weapons import Missil
from pygame.sprite import Group

mixer.init()
# carregando sons
som_missil = mixer.Sound('Audio\Tiros\Som_Missil_Inicio.wav')

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 400
        self.vivo = True
        self.speed = 5
        self.direcao = -1
        self.flip = True
        self.velocidade = 3
        self.vel_y = 0
        self.shoot_laser_cooldown = 0
        self.shoot_missil_cooldown = 0
        self.laser_beam_cooldown = 0
        self.valor_cooldown_shoot_laser = 80
        self.valor_cooldown_shoot_missil = 1000
        self.valor_cooldown_laser_beam = 2000
        self.lista_animacoes = []
        self.frame_index = 0
        self.action = 0
        self.x = x
        self.y = y 
        self.music = False
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Win', 'Death']
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

        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.campo_visao_longe = pygame.Rect(0, 0, 600, 70)
        self.campo_visao_longe.center = self.rect.center

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.velocidade
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.velocidade
            self.flip = False
            self.direction = 1
        #check collision with floor
        if self.rect.bottom + dy > 600: # chão settado para 600
            dy = 600 - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.update_animacao()
        self.check_vivo()
        # update cooldown
        if self.shoot_laser_cooldown > 0:
            self.shoot_laser_cooldown -= 1
        if self.shoot_missil_cooldown > 0:
            self.shoot_missil_cooldown -= 1
        if self.laser_beam_cooldown > 0:
            self.laser_beam_cooldown -= 1

    def update_animacao(self):
        cooldown_animacao = 100
		# update da imagem dependendo do frame
        self.image = self.lista_animacoes[self.action][self.frame_index]
		# check se já passou tempo suficiente desde o último update
        if pygame.time.get_ticks() - self.update_time > cooldown_animacao:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		# se a animação chegou no final ela reinicia
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
                self.cooldown_animacao = 100 # cooldown da ação de Win
            elif self.action == 3:
                self.cooldown_animacao = 100 # cooldown da ação de Death
            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def check_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.speed = 0
            self.vivo = False
            self.update_action(3)

    def shoot_laser(self):
        if self.shoot_laser_cooldown == 0:
            self.shoot_laser_cooldown = self.valor_cooldown_shoot_laser # cooldown do tiro
            laser_bullet = Bullet('bullet_laser', self.rect.centerx + (0.45 * self.rect.size[0] * self.direcao), self.rect.centery - 70, self.direcao, 10)
            inimigo_bullet_group.add(laser_bullet)

    def shoot_missil(self, player):
        if self.shoot_missil_cooldown == 0:
            self.shoot_missil_cooldown = self.valor_cooldown_shoot_missil
            missil1 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 20, 0.7)
            missil2 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 30, 0.5)
            missil3 = Missil((self.rect.x, self.rect.y + 30), (player.rect.x, player.rect.y), 40, 0.4)
            missil_group.add(missil1, missil2, missil3)
            som_missil.play()

    def laser_beam(self):
        if self.laser_beam_cooldown == 0:
            self.laser_beam_cooldown = self.valor_cooldown_laser_beam
            laser = weapons.Laser(self.rect.centerx - 100, self.rect.centery)
            laser_group.add(laser)

    '''def big_run(self, player):
        self.rect.x -= self.velocidade * self.direcao
        self.update_action(1) # ação de correr
        if self.rect.colliderect(player.rect):
            player.vida -= 0.2 # dano da corrida
        if self.rect.right >= 1280: # borda direita da tela em que está
            self.direcao = 1
            self.flip = True
            self.update_action(0) #ação de idle 
        elif self.rect.left <= 0:# borda esqyerda da tela em que está
            self.direcao = -1
            self.flip = False 
            self.update_action(0) #ação de idle''' 
        
    def ai(self, player, tela, tela_scroll):
        if self.vivo and player.vivo:
            if self.vida >= 100:
                self.valor_cooldown_shoot_laser = 60
                self.valor_cooldown_shoot_missil = 500
                self.valor_cooldown_laser_beam = 1000
            self.campo_visao_longe.center = (self.rect.centerx + 500 * self.direcao, self.rect.centery)
            if self.idling == False and numpy.random.randint(1, 150) == 1:
                self.update_action(0) # ação de idle
                self.idling = True
                self.idling_counter = 150
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False
                if self.campo_visao_longe.colliderect(player.rect):
                    self.music = True
                    escolher_ataque = numpy.random.randint(0, 3)
                    if escolher_ataque == 0:
                        self.shoot_laser()
                    elif escolher_ataque == 1:
                        self.shoot_missil(player)
                    elif escolher_ataque == 2:
                        self.laser_beam()
        

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# sprite groups
inimigo_bullet_group = player_script.inimigo_bullet_group
missil_group = weapons.missil_group
laser_group = weapons.laser_group