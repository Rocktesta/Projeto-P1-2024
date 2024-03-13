import pygame
import os
from player_script import Bullet
from random import randint
from pygame.sprite import Group

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.speed = 5
        self.direcao = 1
        self.velocidade = 5
        self.vel_y = 0
        self.shoot_laser_cooldown = 0
        self.flip = True
        self.lista_animacoes = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Win']
        for animation in animation_types:
            lista_temp = []
            num_frames = len(os.listdir(f'Image\Sprites\\boss\{animation}'))
            for i in range(num_frames):
                img = pygame.image.load(f'Image\Sprites\\boss\{animation}\\boss_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4))
                lista_temp.append(img) 
            self.lista_animacoes.append(lista_temp)
        
        self.image = self.lista_animacoes[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.perseguindo = False
        self.move_counter = 0
        self.linha_de_fogo = pygame.Rect(0, 0, 600, 40)
        self.campo_visao = pygame.Rect(0, 0, 700, 40)
        self.idling = False
        self.idling_counter = 0

    def update(self):
        self.update_animacao()
        # update cooldown laser
        if self.shoot_laser_cooldown > 0:
            self.shoot_laser_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset as variáveis de movimento
        if self.vivo:
            tela_scroll = 0
            dx = 0
            dy = 0
            # checando se o player se move para a direita ou esquerda
            if moving_left:
                dx = -self.velocidade
                self.flip = True
                self.direcao = -1
            if moving_right:
                dx = +self.velocidade
                self.flip = False
                self.direcao = 1
            # ação da gravidade
            if self.vel_y > 10: # velocidade máxima
                self.vel_y
            dy += self.vel_y
            # checando colisão com o chão
            if self.rect.bottom + dy > 700:
                dy = 700 - self.rect.bottom
                self.no_ar = False
            # updade da posição do rect do player
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.right > 1280 - 200 or self.rect.left < 200:
                self.rect.x -= dx
                tela_scroll = -dx
            return tela_scroll
        else:
            return 0

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
                self.cooldown_animacao = 100 # cooldown da ação de Jump
            elif self.action == 3:
                self.cooldown_animacao = 100 # cooldown da ação de Death
            elif self.action == 4:
                self.cooldown_animacao = 100 # cooldown da ação de Win
            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def shoot_laser(self):
        if self.shoot_laser_cooldown == 0:
            self.shoot_laser_cooldown = 60
            laser_bullet = Bullet('bullet_laser', self.rect.centerx + (0.32 * self.rect.size[0] * self.direcao), self.rect.centery - 20, self.direcao, 7)
            

    def shoot_missil(self):
        pass
    
    def laser_beam(self):
        pass

    def big_run(self):
        pass 

    def ai(self, player):
        if self.vivo and player.vivo:
            self.linha_de_fogo.center = (self.rect.centerx + 200 * self.direcao, self.rect.centery) # posição do campo de visão
            self.campo_visao.center = (self.rect.centerx + 200 * self.direcao, self.rect.centery) # posição do campo de visão extendido
            # fazendo o inimigo ficar parado
            if self.idling == False and randint(1, 200) == 1:
                self.update_action(0) # ação de idle
                self.idling = True
                self.idling_counter = 50
            # check se o inimigo está perto de um player
            if self.campo_visao.colliderect(player.rect):
                # se o jogador entrar no campo de visão o inimigo o persegue
                self.perseguindo = True
            else:
                self.perseguindo = False
            if self.linha_de_fogo.colliderect(player.rect) and self.perseguindo:
                # parar de se mover e encarar o player
                self.update_action(0) # ação de idle
                self.shoot_laser()
                self.perseguindo = True
            elif self.perseguindo:
                # se o jogador sair da linha de tiro ou entrar no campo de visão o inimigo o persegue até sair do campo de visão
                self.update_action(1)  # Ação de correr
                self.move(self.direcao == -1, self.direcao == 1)
            else:
                self.perseguindo = False
                if self.idling == False:
                    # movendo o inimigo
                    if self.direcao == 1:
                        ai_movendo_direita = True
                    else:
                        ai_movendo_direita = False
                    ai_movendo_esquerda = not ai_movendo_direita
                    self.move(ai_movendo_esquerda, ai_movendo_direita)
                    self.update_action(1) # ação de correr
                    self.move_counter += 1
                    # update visão do inimigo quando ele se move
                    self.linha_de_fogo.center = (self.rect.centerx + 200 * self.direcao, self.rect.centery) # posição do campo de visão
                    self.campo_visao.center = (self.rect.centerx + 200 * self.direcao, self.rect.centery) # posição do campo de visão extendido
                    # mudando a direção
                    if self.move_counter > 50:
                        self.direcao *= -1
                        self.move_counter *= -1
                else: 
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


def bossfight():
    pass