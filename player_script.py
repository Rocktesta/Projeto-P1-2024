import pygame
from pygame import mixer
import os
from random import randint
from pygame.sprite import Group

mixer.init()
# carregando sons
pistol_sound = mixer.Sound('Audio\pistol_sound.wav')
pistol_sound.set_volume(0.3)
bullet_laser_sound = mixer.Sound('Audio\\bullet_laser.mp3')

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
        self.max_vida = 100
        self.velocidade_y = 0
        self.direcao = 1
        self.jump = False
        self.no_ar = True
        self.flip = False
        self.lista_animacoes = []
        self.frame_index = 0
        self.sprite_sheet = pygame.image.load("Image\Sprites\Sprite_sheet_Kiev.png").convert_alpha()
        frames = self.sprite_sheet.get_width() // 128
        linhas = self.sprite_sheet.get_height() // 128
        # 0 = Idle | 1 = Run | 2 = Jump | 3 = Death
        self.action = 0
        self.update_tempo = pygame.time.get_ticks()
        self.idle_t = []
        self.run_t_shotgun = []
        self.idle_t_shotgun = []
        self.idle_p = []
        self.run_t_pistol = []
        self.run_p = []
        self.shoot_t = []
        for i in range(linhas):
            for j in range(frames):
                imagem = pygame.Surface((128, 128)).convert_alpha()
                imagem.fill((0, 0, 0, 0))
                imagem.blit(self.sprite_sheet, (0, 0), ((j * 128), (i * 128), 128, 128))
                imagem = pygame.transform.scale(imagem, (128 * escala, 128 * escala)) 
                imagem.convert_alpha()
                if pygame.transform.average_color(imagem) == ((0, 0, 0, 0)):
                    imagem == None
                if i == 0:
                    self.idle_t.append(imagem)
                if i == 1: 
                    self.idle_p.append(imagem)
                if i == 2:   
                    self.run_t_pistol.append(imagem)
                if i == 3:
                    self.run_p.append(imagem)
                if i == 4:
                    self.shoot_t.append(imagem)
                if i == 5:
                    self.run_t_shotgun.append(imagem)
                if i == 6:
                    self.idle_t_shotgun.append(imagem)
                
        self.rect = pygame.Rect(x, y, 100, 384)
        self.rect_pernas = pygame.Rect(self.rect.x, self.rect.y - 300, 100, 64)
        self.rect.center = (x, y)
        print(len(self.idle_t))


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
                self.velocidade_y = -23 # altura do pulo
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
            bullet = Bullet(bullet_type, self.rect.centerx + (0.42 * self.rect.size[0] * self.direcao), self.rect.centery - 45, self.direcao, 10)
            if alvo == 'inimigo': 
                player_bullet_group.add(bullet)
                pistol_sound.play()
            else:
                inimigo_bullet_group.add(bullet)
                bullet_laser_sound.play()

    def update_animacao(self):
        if self.action == 0: # idle
            # update da imagem dependendo do frame
            self.img_player = self.idle_t[self.frame_index]
            self.img_perna = self.idle_p[0]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 2:
                self.frame_index = 0
        elif self.action == 1: # correndo
            # update da imagem dependendo do frame
            self.img_player = self.run_t_pistol[self.frame_index]
            self.img_perna = self.run_p[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 6:
                self.frame_index = 0
        elif self.action == 4: # atirando corendo 
            # update da imagem dependendo do frame
            self.img_player = self.shoot_t[self.frame_index]
            self.img_perna = self.run_p[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 6:
                self.frame_index = 0
        elif self.action == 5: # atirando parado
            self.leg_index = 0
            # update da imagem dependendo do frame
            self.img_player = self.shoot_t[self.frame_index]
            self.img_perna = self.idle_p[self.leg_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 6:
                self.frame_index = 0
            if self.leg_index >= 1:
                self.leg_index = 0
        elif self.action == 6: # run shotgun
            self.leg_index = 0
            # update da imagem dependendo do frame
            self.img_player = self.run_t_shotgun[self.frame_index]
            self.img_perna = self.run_p[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 6:
                self.frame_index = 0
        elif self.action == 7: # idle shotgun
            # update da imagem dependendo do frame
            self.img_player = self.idle_t_shotgun[self.frame_index]
            self.img_perna = self.idle_p[0]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 2:
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
                self.cooldown_animacao = 100 # cooldown da ação de Shoot run
            elif self.action == 5:
                self.cooldown_animacao = 100 # cooldown da ação de Shoot idle
            elif self.action == 6:
                self.cooldown_animacao = 100 # cooldown da ação run com shotgun
            elif self.action == 7:
                self.cooldown_animacao = 300 # cooldown da ação idle com shotgun
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
        tela.blit(pygame.transform.flip(self.img_player, self.flip, False), (self.rect.x - 120, self.rect.y))
        tela.blit(pygame.transform.flip(self.img_perna, self.flip, False), (self.rect.x - 120, self.rect.y - 10))

class Inimigo(Player, pygame.sprite.Sprite):
    # classe inimigo que herdeira da classe Player
    def __init__(self, char_type, x, y, velocidade, gravidade, escala=2, vida=100, cooldown_animacao=100):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(char_type, x, y, velocidade, gravidade, escala, vida, cooldown_animacao)
        self.perseguindo = False
        self.move_counter = 0
        self.linha_de_fogo = pygame.Rect(0, 0, 600, 40)
        self.campo_visao = pygame.Rect(0, 0, 00, 40)
        self.idling = False
        self.idling_counter = 0
    
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
                self.shoot('player', 'bullet_laser')
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, x, y, direcao, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_type = bullet_type
        self.direcao = direcao
        self.velocidade = velocidade
        self.image = pygame.image.load(f'Image/bullet/{self.bullet_type}.png')
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