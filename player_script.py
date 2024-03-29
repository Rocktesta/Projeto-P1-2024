import pygame
from pygame import mixer
from pygame.sprite import Group
import numpy
import os
import weapons
from weapons import Shotgun

mixer.init()
# carregando sons
pegar_pistola_sound = mixer.Sound('Audio\Pegando_arma.wav')
pistol_sound = mixer.Sound('Audio\Tiros\pistol_sound.wav')
pistol_sound.set_volume(0.3)
bullet_laser_sound = mixer.Sound('Audio\Tiros\\bullet_laser.wav')
shotgun_sound = mixer.Sound('Audio\Tiros\\shotgun_blast.mp3')
shotgun_sound.set_volume(0.3)

class Player(pygame.sprite.Sprite): #classe do player
    def __init__(self, x, y, velocidade, gravidade, tela, escala=3, vida=100, cooldown_animacao=100):
        pygame.sprite.Sprite.__init__(self)
        self.com_keycard = False # pegou ou não o cartão para zerar o jogo
        self.escala = escala
        self.gravidade = gravidade
        self.vivo = True
        self.velocidade = velocidade
        self.shoot_cooldown = 0
        self.shotgun_cooldown = 0
        self.cooldown_animacao = cooldown_animacao # tempo de update da animação
        self.vida = vida
        self.max_vida = 100
        self.velocidade_y = 0
        self.direcao = 1
        self.jump = False
        self.no_ar = True
        self.flip = False # inversao de sprites
        self.shotgun_equip = False
        self.shotgun_ammo = 0
        self.lista_animacoes = []
        self.frame_index = 0
        self.crouch = False # agachar flag
        self.sprite_sheet = pygame.image.load("Image\Sprites\Sprite_sheet_main.png").convert_alpha()    # arquivo com tiles 128x128, com todos os sprites do player
        frames = self.sprite_sheet.get_width() // 128
        linhas = self.sprite_sheet.get_height() // 128
        self.action = 0
        self.update_tempo = pygame.time.get_ticks()
        # lista de animacoes e frames
        self.idle_t = []
        self.x = x
        self.y = y
        self.run_t_shotgun = []
        self.idle_t_shotgun = []
        self.idle_p = []
        self.run_t_pistol = []
        self.run_p = []
        self.shoot_t = []
        self.die = []
        self.jump_sprites = []
        self.jump_shotgun = []
        self.coxinha = []
        self.keycard = []
        self.shotgun_shoot = []
        self.crouch_pistol = []
        self.crouch_shotgun = []
        self.nada = []
        self.pulo_perna = []
        self.perna_correndo = []
        self.pulo_pistola_torso = []
        # adicao de frames para a lista
        for i in range(linhas):
            for j in range(frames):
                imagem = pygame.Surface((128, 128)).convert_alpha()
                imagem.fill((0, 0, 0, 0))
                imagem.blit(self.sprite_sheet, (0, 0), ((j * 128), (i * 128), 128, 128))
                imagem = pygame.transform.scale(imagem, (128 * 3, 128 * 3)) 
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
                if i == 7:
                    self.die.append(imagem)
                if i == 8:
                    self.jump_sprites.append(imagem)
                if i == 9:
                    self.keycard.append(imagem)
                if i == 10:
                    self.coxinha.append(imagem)
                if i == 11:
                    self.shotgun_shoot.append(imagem)
                if i == 12:
                    self.crouch_shotgun.append(imagem)
                if i == 13:
                    self.crouch_pistol.append(imagem)
                if i == 16:
                    self.jump_shotgun.append(imagem)
                if i == 17:
                    self.pulo_perna.append(imagem)
                if i == 18:
                    self.perna_correndo.append(imagem)
                if i == 19:
                    self.pulo_pistola_torso.append(imagem)
                if i == 20:
                    self.nada.append(imagem)
        # rects do player, torso e perna separados  para facilitar a animação
        self.rect = pygame.Rect(x, y , 100, 300)
        self.mask = pygame.mask.from_surface(self.idle_t[0])
        self.imagem_mask = self.mask.to_surface()
        self.imagem_mask.set_colorkey((0, 0, 0))
        self.rect_pernas = pygame.Rect(self.rect.x, self.rect.y - 300, 100, 64)
        self.rect.center = (x, y)
        self.leg_index = 0
        self.shotgun_cooldown = 0
        self.blast = weapons.ShotgunBlast(300, 500)
        print(len(self.idle_t))

    def update(self, x, y, tela):   # updates do player, check de vivo e animacao
        # mudar de rect se agachar
        if self.crouch == True:
            self.rect = pygame.Rect(x, y + 100, 100, 180)
        else:
            self.rect = pygame.Rect(x, y, 100, 280)
        # animacao e check vivo
        self.update_animacao()
        self.check_vivo()
        # update cooldown, check de municao e equip da shotgun
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shotgun_cooldown > 0:
            self.shotgun_cooldown -= 1
        if self.shotgun_equip == True and self.shotgun_ammo <= 0:
            self.shotgun_equip = False
            pegar_pistola_sound.play()

    def move(self, moving_left, moving_right):  #movimentos do player, gera o tela_scroll(camera)
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
            if self.crouch == False:
                if self.rect.bottom + dy > 570: # chão setado para 570
                    dy = 570 - self.rect.bottom
                    self.no_ar = False
            else:
                if self.rect.bottom + dy > 470: # chão setado para 470
                    dy = 470 - self.rect.bottom
                    self.no_ar = False
                
            # updade da posição do rect do player
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.right > 1280 - 500 or self.rect.left < 200:    # travas da camera
                self.rect.x -= dx
                tela_scroll = -dx
            return tela_scroll
        else:
            return 0

    def shoot(self, bullet_type, tela): # tiros do player, com group de balas ou sprite collide da shotgun
        if not self.shotgun_equip:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 40
                if self.direcao == 1:   #flip
                    bullet = Bullet(bullet_type, self.rect.centerx + 70, self.rect.centery - 150, self.direcao, 7)
                elif self.direcao == -1:    #flip
                    bullet = Bullet(bullet_type, self.rect.centerx - 235, self.rect.centery - 150, self.direcao, 7)
                player_bullet_group.add(bullet)
                pistol_sound.play() # som do tiro da pistola
        else:
            if self.direcao  == 1:
                self.blast.update(self.rect.x + (310 * self.direcao), self.rect.y + 90, inimigo_group)
                self.blast.draw(tela, False)
            else:            
                self.blast.update(self.rect.x + (310 * self.direcao), self.rect.y + 90, inimigo_group)
                self.blast.draw(tela, True)
            if self.shotgun_cooldown == 0:
                self.shotgun_cooldown = 60
                shotgun_sound.play()    # som do tiro da shotgun
                self.shotgun_ammo -= 1    
            
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
            if self.frame_index >= 14:
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
        elif self.action == 2: # pulando
            # update da imagem dependendo do frame
            self.img_player = self.pulo_pistola_torso[self.frame_index]
            self.img_perna = self.pulo_perna[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 8:
                self.frame_index = 7
        elif self.action == 3: # morrendo
            # update da imagem dependendo do frame
            self.img_player = self.die[self.frame_index]
            self.img_perna = self.idle_p[10]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela para
            if self.frame_index >= 15:
                self.frame_index = len(self.die) - 1
        elif self.action == 4: # atirando corendo 
            # update da imagem dependendo do frame
            self.img_player = self.shoot_t[self.frame_index]
            self.img_perna = self.perna_correndo[self.leg_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
                self.leg_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 6:
                self.frame_index = 0
            if self.leg_index >= 6:
                self.leg_index = 0
        elif self.action == 5: # atirando parado
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
            if self.frame_index >= 14:
                self.frame_index = 0
        elif self.action == 8: #shotgun atirando parado
            # update da imagem dependendo do frame
            self.img_player = self.shotgun_shoot[self.frame_index]
            self.img_perna = self.idle_p[0]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 10:
                self.frame_index = 0
        elif self.action == 9: #shotgun atirando correndo
             # update da imagem dependendo do frame
            self.img_player = self.shotgun_shoot[self.frame_index]
            self.img_perna = self.perna_correndo[self.leg_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
                self.leg_index += 1
            # se a animação chegar no final ela reinicia   
            if self.frame_index >= 10:
                self.frame_index = 0
            if self.leg_index >= 6:
                self.leg_index = 0
        elif self.action == 10: #agachar pistola
             # update da imagem dependendo do frame
            self.img_player = self.crouch_pistol[self.frame_index]
            self.img_perna = self.nada[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
                self.leg_index += 1
            # se a animação chegar no final ela reinicia   
            if self.frame_index >= 4:
                self.frame_index = 3
            if self.leg_index >= 4:
                self.leg_index = 3
        elif self.action == 11: #agachar doze
             # update da imagem dependendo do frame
            self.img_player = self.crouch_shotgun[self.frame_index]
            self.img_perna = self.nada[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
                self.leg_index += 1
            # se a animação chegar no final ela reinicia   
            if self.frame_index >= 4:
                self.frame_index = 3
            if self.leg_index >= 4:
                self.leg_index = 3
        elif self.action == 12: #pular de doze
            # update da imagem dependendo do frame
            self.img_player = self.jump_shotgun[self.frame_index]
            self.img_perna = self.pulo_perna[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
                self.leg_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 8:
                self.frame_index = 7
            if self.leg_index >= 8:
                self.leg_index = 7 

    def update_action(self, nova_acao): #updates das animcoes com cooldown dos frames
        # checa se a nova ação é deferente da ação anterior
        if nova_acao != self.action:
            self.action = nova_acao
            # update do cooldown da animação
            if self.action == 0:
                self.cooldown_animacao = 200 # cooldown da ação de Idle
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
                self.cooldown_animacao = 100 # cooldown da ação idle com shotgun
            elif self.action == 8:
                self.cooldown_animacao = 100 # cooldown da ação shoot idle com shotgun
            elif self.action == 9:
                self.cooldown_animacao = 100 # cooldown da ação shoot run com shotgun
            elif self.action == 10:
                self.cooldown_animacao = 60 # cooldown da ação agachar com pistola
            

            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def check_vivo(self):   # verifica se o personagem está vivo
        if self.vida <= 0 or self.vivo == False:
            self.vida = 0
            if self.crouch == True:
                self.crouch = False
                self.rect.y = 290
            self.velocidade = 0
            self.vivo = False
            self.update_action(3) # ação de morrer

    def draw(self, tela):   # render do player
        if self.crouch == False:
            tela.blit(pygame.transform.flip(self.img_player, self.flip, False), (self.rect.x - 120, self.rect.y - 50))
            tela.blit(pygame.transform.flip(self.img_perna, self.flip, False), (self.rect.x - 120, self.rect.y - 50))

        else: 
            tela.blit(pygame.transform.flip(self.img_player, self.flip, False), (self.rect.x - 120, self.rect.y - 150))
            tela.blit(pygame.transform.flip(self.img_perna, self.flip, False), (self.rect.x - 120, self.rect.y - 150))

class Inimigo(pygame.sprite.Sprite):   # classe do inimigo
    def __init__(self, char_type, x, y, velocidade, gravidade, escala=100, vida=100):
        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.vida = vida
        self.char_type = char_type
        self.velocidade = velocidade
        self.gravidade = gravidade
        self.direcao = 1
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.cooldown_animacao = 100

        self.lista_animacoes = []
        animacao_tipos = ['Idle', 'Run', 'Shoot', 'Death']  # tipos de animacao dos inimigos
        for animacao in animacao_tipos:
            temp_list = []
            num_frames = len(os.listdir(f'Image\Sprites\{self.char_type}\{animacao}'))  # num de frames
            for i in range(num_frames):
                img = pygame.image.load(f'Image\Sprites\{self.char_type}\{animacao}\{i}.png')   # loop do diretorio
                img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
                temp_list.append(img)
            self.lista_animacoes.append(temp_list)

        self.image = self.lista_animacoes[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.shoot_cooldown = 0
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.atirando = False
        # alcance dos inimigos
        self.campo_visao_frente = pygame.Rect(0, 0, 700, 300)
        self.campo_visao_costas = pygame.Rect(0, 0, 400, 100)
    
    def move(self, moving_left, moving_right):  #movimentacao dos inimigos
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
        #check colisao com chao
        if self.rect.bottom + dy > 570: # chão settado para 550
            dy = 570 - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy

    def update(self):   #update dos inimigos
        self.update_animation()
        self.check_vivo()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_animation(self): #update das animacoes com cooldowns
        self.image = self.lista_animacoes[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.cooldown_animacao:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.lista_animacoes[self.action]):
            if self.action == 3:
                self.frame_index = len(self.lista_animacoes[self.action]) - 1
            else:
                self.frame_index = 0    # se chegar ao fim a animacao recomeca
    
    def update_action(self, nova_acao): #update das acoes do inimigo
        if nova_acao != self.action:
            self.action = nova_acao
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            if self.action == 0 or self.action == 1: # ação de idle ou run
                self.cooldown_animacao = 100
            elif self.action == 2: # ação de shoot
                self.cooldown_animacao = 100
            elif self.action == 3: # ação de death
                self.cooldown_animacao = 150
    
    def shoot(self, bullet_type):   #  dispara um tiro do inimigo
        if self.shoot_cooldown == 0 and self.frame_index == 5:
            self.shoot_cooldown = 60    # cooldwon do tiro
            bullet = Bullet(bullet_type, self.rect.centerx + (215 * self.direcao), self.rect.centery + 15, self.direcao, 7)
            inimigo_bullet_group.add(bullet) # add ou group das balas do inimigos
            bullet_laser_sound.play()
    
    def check_vivo(self):   # verifica se o inimigo esta vivo
        if self.vida <= 0:
            self.vida = 0
            self.velocidade = 0
            self.vivo = False
            self.update_action(3)
    
    def draw(self, tela):   # render dos inimigos
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def ai(self, player, tela, tela_scroll):    # ai rudimentar, para perseguir e atirar no player
        if self.vivo and player.vivo:   # se o player estiver vivo e o inimigo tambem, ai ativa
            if self.idling == False and numpy.random.randint(1, 100) == 1:
                self.atirando = False
                self.update_action(0) # ação de idle
                self.idling = True
                self.idling_counter = 50
                self.campo_visao_frente.center = (self.rect.centerx + (300 * self.direcao) + tela_scroll, self.rect.centery - 100)
                self.campo_visao_costas.center = (self.rect.centerx - (230 * self.direcao) + tela_scroll, self.rect.centery + 20)
            # check se o player está no campo de visão da frente
            if self.campo_visao_frente.colliderect(player.rect):
                if self.atirando == False:
                    self.update_action(0) # ação de idle
                    self.update_action(2) # ação de tiro
                    self.atirando = True
                self.shoot('bullet_laser')
                self.campo_visao_frente.center = (self.rect.centerx + (300 * self.direcao) + tela_scroll, self.rect.centery - 100)
                self.campo_visao_costas.center = (self.rect.centerx - (230 * self.direcao) + tela_scroll, self.rect.centery + 20)
            elif self.campo_visao_costas.colliderect(player.rect):
                self.atirando = False
                self.flip = not self.flip
                self.direcao *= -1
                self.campo_visao_frente.center = (self.rect.centerx + (300 * self.direcao) + tela_scroll, self.rect.centery - 100)
                self.campo_visao_costas.center = (self.rect.centerx - (230 * self.direcao) + tela_scroll, self.rect.centery + 20)
            else:
                self.atirando = False
                if self.idling == False:
                    if self.direcao == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) # ação de correr
                    self.move_counter += 1
                    # updade do campo de visão quando se mover
                    self.campo_visao_frente.center = (self.rect.centerx + 300 * self.direcao + tela_scroll, self.rect.centery - 100)
                    self.campo_visao_costas.center = (self.rect.centerx - 230 * self.direcao + tela_scroll, self.rect.centery + 20)

                    distancia_percorrida = numpy.random.randint(60, 150)
                    if self.move_counter > distancia_percorrida:
                        self.direcao *= -1
                        self.move_counter *= -1
                # se não estiverem em idle
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False
        elif not player.vivo:
            self.update_action(0) # ação de idle

class Bullet(pygame.sprite.Sprite): # classe das balas
    def __init__(self, bullet_type, x, y, direcao, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_type = bullet_type
        self.direcao = direcao
        self.velocidade = velocidade
        self.image = pygame.image.load(f'Image/bullet/{self.bullet_type}.png') #balas no diretorio, tipos distintos para player e inimigo
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.mask = pygame.mask.from_surface(self.image)
        if self.direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.center = (x, y)
    
    def update(self, entrada, entrada_tipo, player):    # update das balas, pos e colisao
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
            # a entrada é o grupo de inimigos
            for alvo in entrada:
                if pygame.sprite.spritecollide(alvo, player_bullet_group, False):
                    if alvo.vivo:
                        alvo.vida -= 30 # dano que a bala causa
                        if player.direcao == 1:
                            hit = BulletHit(alvo.rect.x + 200, alvo.rect.y + 275, False) # atirando da esquerda pra direita
                        elif player.direcao == -1:
                            hit = BulletHit(alvo.rect.x + 245, alvo.rect.y + 275, True) # atirando da direita para a esquerda
                        player_bullet_hit_group.add(hit)
                        self.kill()

class BulletHit(pygame.sprite.Sprite):  # animacao de impacto das balas
    def __init__(self, x, y, flip):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for n in range(len(os.listdir(f'Image\\bullet\\bullet_impact')) - 1):   # loop do diretorio
            img = pygame.image.load(f'Image\\bullet\\bullet_impact\impact{n}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            if flip == True:
                img = pygame.transform.flip(img, True, False)
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.fps = 350 # velocidade da animação
        self.count_cooldown = 0
        self.delay = int(1000/self.fps)

    def update(self):   # atualização da imagem
        self.count_cooldown += 1
        if self.count_cooldown >= self.delay:
            self.count_cooldown = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill() # remove a animação quando acabarem os frames
            else:
                self.image = self.images[self.frame_index]

# Sprite Groups
player_bullet_group = pygame.sprite.Group()
player_bullet_hit_group = pygame.sprite.Group()
inimigo_bullet_group = pygame.sprite.Group()
inimigo_group = pygame.sprite.Group()
shotgun_blast_group = weapons.shotgun_blast_group