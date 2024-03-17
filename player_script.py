import pygame
from pygame import mixer
from pygame.sprite import Group
import numpy
import os
import weapons
from weapons import Shotgun

mixer.init()
# carregando sons
pistol_sound = mixer.Sound('Audio\pistol_sound.wav')
pistol_sound.set_volume(0.3)
bullet_laser_sound = mixer.Sound('Audio\\bullet_laser.mp3')

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade, gravidade, escala=3, vida=100, cooldown_animacao=100):
        pygame.sprite.Sprite.__init__(self)
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
        self.flip = False
        self.shotgun_equip = False
        self.lista_animacoes = []
        self.frame_index = 0
        self.sprite_sheet = pygame.image.load("Image\Sprites\Sprite_sheet_main.png").convert_alpha()
        frames = self.sprite_sheet.get_width() // 128
        linhas = self.sprite_sheet.get_height() // 128
        # 0 = Idle | 1 = Run | 2 = Jump | 3 = Death
        self.action = 0
        self.update_tempo = pygame.time.get_ticks()
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
        self.coxinha = []
        self.keycard = []
        self.shotgun_shoot = []
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

                
        self.rect = pygame.Rect(x, y, 120, 360)
        self.mask = pygame.mask.from_surface(self.idle_t[0])
        self.imagem_mask = self.mask.to_surface()
        self.imagem_mask.set_colorkey((0, 0, 0))
        self.rect_pernas = pygame.Rect(self.rect.x, self.rect.y - 300, 100, 64)
        self.rect.center = (x, y)
        self.leg_index = 0
        self.shotgun_cooldown = 0
        print(len(self.idle_t))


    def update(self):
        self.update_animacao()
        self.check_vivo()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.shotgun_cooldown > 0:
            self.shotgun_cooldown -= 1
            print(self.shotgun_cooldown)

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
            if self.rect.bottom + dy > 600: # chão setado para 700
                dy = 600 - self.rect.bottom
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


    def shoot(self, bullet_type, tela):
        if not self.shotgun_equip:
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 40
                if self.direcao == 1:
                    bullet = Bullet(bullet_type, self.rect.centerx + 70, self.rect.centery - 120, self.direcao, 7)
                elif self.direcao == -1:
                    bullet = Bullet(bullet_type, self.rect.centerx - 235, self.rect.centery - 120, self.direcao, 7)
                player_bullet_group.add(bullet)
                pistol_sound.play()
        else:
            if self.shotgun_cooldown == 0:
                blast = weapons.ShotgunBlast(self.rect.x + (300 * self.direcao), self.rect.y + 200)
                print(len(blast.images))
                for i in range(len(blast.images)):
                    blast.update()
                    blast.draw(tela)
                    pygame.display.update()
                self.shotgun_cooldown = 50
            
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
            self.img_player = self.jump_sprites[self.frame_index]
            self.img_perna = self.jump_sprites[10]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= 8:
                self.frame_index = 0
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
            self.img_perna = self.run_p[self.leg_index]
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
            self.img_perna = self.run_p[self.leg_index]
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

    def update_action(self, nova_acao):
        # checa se a nova ação é deferente da ação anterior
        if nova_acao != self.action:
            self.action = nova_acao
            # update do cooldown da animação
            if self.action == 0:
                self.cooldown_animacao = 200 # cooldown da ação de Idle
            elif self.action == 1:
                self.cooldown_animacao = 100 # cooldown da ação de Run
            elif self.action == 2:
                self.cooldown_animacao = 200 # cooldown da ação de Jump
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

class Inimigo(pygame.sprite.Sprite):
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
        animacao_tipos = ['Idle', 'Run', 'Shoot', 'Death']
        for animacao in animacao_tipos:
            temp_list = []
            num_frames = len(os.listdir(f'Image\Sprites\{self.char_type}\{animacao}'))
            for i in range(num_frames):
                img = pygame.image.load(f'Image\Sprites\{self.char_type}\{animacao}\{i}.png')
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
        self.campo_visao_frente = pygame.Rect(0, 0, 700, 40)
        self.campo_visao_costas = pygame.Rect(0, 0, 300, 40)
    
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
        if self.rect.bottom + dy > 570: # chão settado para 550
            dy = 570 - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        self.update_animation()
        self.check_vivo()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_animation(self):
        self.image = self.lista_animacoes[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.cooldown_animacao:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.lista_animacoes[self.action]):
            if self.action == 3:
                self.frame_index = len(self.lista_animacoes[self.action]) - 1
            else:
                self.frame_index = 0
    
    def update_action(self, nova_acao):
        if nova_acao != self.action:
            self.action = nova_acao
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            if self.action == 0 or self.action == 1: # ação de idle ou run
                self.cooldown_animacao = 100
            elif self.action == 2: # ação de shoot
                self.cooldown_animacao = 200
            elif self.action == 3: # ação de death
                self.cooldown_animacao = 150
    
    def shoot(self, bullet_type):
        if self.shoot_cooldown == 0:
            self.update_action(2)
            self.shoot_cooldown = 50
            bullet = Bullet(bullet_type, self.rect.centerx + (100 * self.direcao), self.rect.centery, self.direcao, 7)
            inimigo_bullet_group.add(bullet)
            bullet_laser_sound.play()
    
    def check_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.velocidade = 0
            self.vivo = False
            self.update_action(3)
    
    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def ai(self, player, tela):
        if self.vivo:
            self.campo_visao_frente.center = (self.rect.centerx + 300 * self.direcao, self.rect.centery)
            self.campo_visao_costas.center = (self.rect.centerx - 200 * self.direcao, self.rect.centery)
            if self.idling == False and numpy.random.randint(1, 100) == 1:
                self.update_action(0) # ação de idle
                self.idling = True
                self.idling_counter = 50
            # check se o player está no campo de visão da frente
            if self.campo_visao_frente.colliderect(player.rect):
                self.update_action(0) # ação de idle
                self.shoot('bullet_laser')
            elif self.campo_visao_costas.colliderect(player.rect):
                self.flip = not self.flip
                self.direcao *= -1
            else:
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
                    self.campo_visao_frente.center = (self.rect.centerx + 300 * self.direcao, self.rect.centery)
                    self.campo_visao_costas.center = (self.rect.centerx - 200 * self.direcao, self.rect.centery)
                    pygame.draw.rect(tela, (255, 0, 0), self.campo_visao_frente)
                    pygame.draw.rect(tela, (0, 0, 255), self.campo_visao_costas)

                    distancia_percorrida = numpy.random.randint(60, 150)
                    if self.move_counter > distancia_percorrida:
                        self.direcao *= -1
                        self.move_counter *= -1
                # se não estiverem em idle
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_type, x, y, direcao, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_type = bullet_type
        self.direcao = direcao
        self.velocidade = velocidade
        self.image = pygame.image.load(f'Image/bullet/{self.bullet_type}.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.mask = pygame.mask.from_surface(self.image)
        if self.direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = pygame.Rect(x, y, 40, 40)
        self.rect.center = (x, y)
    
    def update(self, entrada, entrada_tipo, player):
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

class BulletHit(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for n in range(len(os.listdir(f'Image\\bullet\\bullet_impact')) - 1):
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

    def update(self):
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