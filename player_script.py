import pygame
import os
from random import randint
from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, velocidade, gravidade, escala=10, vida=90, cooldown_animacao=100):
        pygame.sprite.Sprite.__init__(self)
        self.escala = escala
        self.gravidade = gravidade
        self.vivo = True
        self.char_type = char_type
        self.velocidade = velocidade
        self.shoot_cooldown = 0 
        self.cooldown_animacao = cooldown_animacao # tempo de update da animação
        self.vida = vida
        self.max_vida = self.vida
        self.velocidade_y = 0
        self.direcao = 1
        self.jump = False
        self.no_ar = True
        self.flip = False
        self.lista_animacoes = []
        self.frame_index = 0
        # 0 = Idle | 1 = Run | 2 = Jump | 3 = Death
        self.action = 0
        self.update_tempo = pygame.time.get_ticks()
        animacao_types = ['Idle', 'Run', 'Jump', 'Death']
        for animacao in animacao_types:
            # reset da lista temporária de imagens
            temp_list = []
            # contar o número de arquivos na pasta
            num_frames = len(os.listdir(f'imagens\Sprites\{self.char_type}\{animacao}'))
            for i in range(num_frames):
                img_player = pygame.image.load(f'imagens\Sprites\{self.char_type}\{animacao}\{self.char_type}{i}.png').convert_alpha()
                img_player = pygame.transform.scale(img_player, (img_player.get_width() * 5, img_player.get_height() * 6))
                temp_list.append(img_player)
            self.lista_animacoes.append(temp_list)
        self.img_player = self.lista_animacoes[self.action][self.frame_index]
        self.rect = self.img_player.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animacao()
        self.check_vivo()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, mooving_left, mooving_right):
        # reset as variáveis de movimento
        if self.vivo:
            tela_scroll = 0
            dx = 0
            dy = 0
            # checando se o player se move para a direita ou esquerda
            if mooving_left:
                dx = -self.velocidade
                self.flip = True
                self.direcao = -1
            if mooving_right:
                dx = +self.velocidade
                self.flip = False
                self.direcao = 1
            # Pulo
            if self.jump == True and self.no_ar == False:
                self.velocidade_y = -15 # altura do pulo
                self.jump = False
                self.no_ar = True
            self.velocidade_y += self.gravidade
            # ação da gravidade
            if self.velocidade_y > 10: # velocidade máxima
                self.velocidade_y
            dy += self.velocidade_y
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


    def shoot(self, alvo, bullet_type):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 40
            bullet = Bullet(bullet_type, self.rect.centerx + (0.32 * self.rect.size[0] * self.direcao), self.rect.centery - 20, self.direcao, 10)
            if alvo == 'inimigo': 
                player_bullet_group.add(bullet)
            else:
                inimigo_bullet_group.add(bullet)

    def update_animacao(self):
        # update da imagem dependendo do frame
        self.img_player = self.lista_animacoes[self.action][self.frame_index]
        # check se passou tempo suficiente desde o último update
        if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
            self.update_tempo = pygame.time.get_ticks()
            self.frame_index += 1
        # se a animação chegar no final ela reinicia
        if self.frame_index >= len(self.lista_animacoes[self.action]):
            if self.action == 3:
                self.frame_index = len(self.lista_animacoes[self.action]) - 1 # último sprite da pasta, personagem vai ficar morto no chão
            else:
                self.frame_index = 0
    
    def update_action(self, nova_acao):
        # checa se a nova ação é deferente da ação anterior
        if nova_acao != self.action:
            self.action = nova_acao
            # update do cooldown da animação
            if self.action == 0:
                self.cooldown_animacao = 100 # cooldown da ação de Idle
            elif self.action == 1:
                self.cooldown_animacao = 100 # cooldown da ação de Run
            elif self.action == 2:
                self.cooldown_animacao = 100 # cooldown da ação de Jump
            elif self.action == 3:
                self.cooldown_animacao = 100 # cooldown da ação de Death
            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def check_vivo(self):
        if self.vida <= 0 or self.vivo == False:
            self.vida = 0
            self.velocidade = 0
            self.vivo = False
            self.update_action(3) # ação de morrer

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.img_player, self.flip, False), self.rect)

class Inimigo(Player, pygame.sprite.Sprite):
    # classe inimigo que herdeira da classe Player
    def __init__(self, char_type, x, y, velocidade, gravidade, escala=2, vida=100, cooldown_animacao=100):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(char_type, x, y, velocidade, gravidade, escala, vida, cooldown_animacao)
        self.move_counter = 0
        self.campo_visao = pygame.Rect(0, 0, 400, 40)
        self.idling = False
        self.idling_counter = 0
    
    def ai(self, player):
        if self.vivo and player.vivo:
            # fazendo o inimigo ficar parado
            if self.idling == False and randint(1, 200) == 1:
                self.update_action(0) # ação de idle
                self.idling = True
                self.idling_counter = 50
            # check se o inimigo está perto de um player
            if self.campo_visao.colliderect(player.rect):
                # parar de se mover e encarar o player
                self.update_action(0) # ação de idle
                self.shoot('player', 'bullet_laser')
            else:
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
                    self.campo_visao.center = (self.rect.centerx + 200 * self.direcao, self.rect.centery) # posição do campo de visão
                    # mudando a direção
                    if self.move_counter > 50:
                        self.direcao *= -1
                        self.move_counter *= -1
                else: 
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, x, y, direcao, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_type = bullet_type
        self.direcao = direcao
        self.velocidade = velocidade
        self.image = pygame.image.load(f'imagens/bullet/{self.bullet_type}.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        if self.direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self, entrada, entrada_tipo):
        # mover a bala
        self.rect.x += (self.direcao * self.velocidade)
        # checar se a bala saiu da tela
        if self.rect.right < 0 or self.rect.left > 1280:
            self.kill()
        # check collision with caracters
        if entrada_tipo == 'player':
            player = entrada
            if pygame.sprite.spritecollide(player, inimigo_bullet_group, False):
                if player.vivo:
                    player.vida -= 5 # dano que a bala causa
                    self.kill()
        else:
            inimigo = entrada
            if pygame.sprite.spritecollide(inimigo, player_bullet_group, False):
                if inimigo.vivo:
                    inimigo.vida -= 30 # dano que a bala causa
                    self.kill()

# Sprite Groups
player_bullet_group = pygame.sprite.Group()
inimigo_bullet_group = pygame.sprite.Group()
inimigo_group = pygame.sprite.Group()