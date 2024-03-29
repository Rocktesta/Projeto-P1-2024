import pygame
from pygame import mixer
import numpy
import math
import os
from pygame.sprite import Group

mixer.init()
# Carregando sons
som_explosao = mixer.Sound('Audio\Tiros\Som_explosao.wav')
som_shotgun_equip = mixer.Sound('Audio\\Metal_slug_Shotgun.wav')
som_shotgun_equip.set_volume(0.4)

#Scrpits para as armas e balas
def nova_posicao_item(player, tela_scroll):
        # gera uma posição aanguloatória para o item
        pos = [numpy.random.randint(400,1200) + tela_scroll, numpy.random.randint(200, 300)]
        while pos[0] == player.rect.x:
            pos = [numpy.random.randint(100,1200) + tela_scroll, numpy.random.randint(200, 300)]
        return pos

class Shotgun(pygame.sprite.Sprite): # classe da shotgun 
    def __init__(self, player, tela_scroll=0, sprite="Weapons\Shotgun_sprite.png", cooldown=1, escala=3):
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player, tela_scroll) # utilizado no staticmethod para spawnar shotguns
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * escala, self.sprite.get_height() * escala))
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        self.cooldown = cooldown # cooldown dos tiros
        self.equipada = False
        self.player = player
       

    @staticmethod #spawn aleatorio de shotguns pelo mapa do jogo, baseado na pos do player
    def gerar_shotgun(player, tela_scroll=0):
        shotgun_group = pygame.sprite.Group()
        if numpy.random.randint(1, 6) == 1:
            shotgun = Shotgun(player, tela_scroll) 
            shotgun_group.add(shotgun)
        return shotgun_group

    def draw(self, tela): #render
        if self.equipada == False:
            tela.blit(self.sprite, (self.rect.x , self.y))

    def update(self, player): #update de equipar, municao e renderizar
        if self.rect.colliderect(player) and not player.shotgun_equip:
            player.shotgun_equip = True
            player.shotgun_ammo = 10
            self.kill()
            som_shotgun_equip.play()
            
class ShotgunBlast(pygame.sprite.Sprite): #tiro/blast da shotgun
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] 
        for n in range(len(os.listdir(f'Weapons')) - 1): #loop pela quantidade de frames
            img = pygame.image.load(f'Weapons\Shotgun_blast{n}.png')
            img = pygame.transform.scale(img, (330, 200))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_blast = 8 # velocidade da animacao
        self.contador = 0 # contagem de imagens
        

    def update(self, x, y, inimigo_group): # update para danos no inimigo
        self.rect.center = (x, y)
        for inimigo in inimigo_group:
            if self.rect.colliderect(inimigo.rect):
                inimigo.vida -= 0.5
                inimigo.vida = int(inimigo.vida)
        
    def draw(self, tela, flip): # render e flip 
        self.contador += 1      # variacao  do frames (roda em loop no main)
        if self.contador >= self.velocidade_blast and self.frame_index < len(self.images) - 1:
            self.contador = 0
            self.frame_index += 1
            self.image = self.images[self.frame_index]
        if  self.frame_index >= len(self.images) - 1: # reset da animacao 
            self.frame_index = 0
            
        if flip: # inverte o frame
            self.image = pygame.transform.flip(self.images[self.frame_index], True, False)
            self.rect.x += 80
        else:
            self.image = self.images[self.frame_index]
            self.rect.x += 80

        tela.blit(self.image, self.rect) # blita na tela
        
        

class Missil(pygame.sprite.Sprite):  #classe do missil, arma do boss
    def __init__(self, start_pos, target_pos, altura, gravidade):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Image\\missil\\missil_sprite.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() , self.image.get_height() ))
        self.original_image = self.image.copy()
        self.rect = pygame.Rect(start_pos, (80, 50))
        self.rect.center = (start_pos[0], start_pos[1])
        self.speed = 3 # velocidade do míssil
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.distance_to_target = math.sqrt((target_pos[0] - start_pos[0]) ** 2 + (target_pos[1] - start_pos[1]) ** 2) #trajetoria balistica
        self.dx = (target_pos[0] - start_pos[0]) / self.distance_to_target # distancia balistica ate o player
        self.dy = (target_pos[1] - start_pos[1]) / self.distance_to_target # distancia balistica ate o player
        self.angle = math.atan2(-self.dy, self.dx)
        self.gravidade = gravidade
        self.vx = self.speed * math.cos(self.angle)    # velocidade angular x
        self.vy = self.speed * math.sin(self.angle) - altura  # velocidade angular y

    def update(self, player, tela): # updates do missil
        self.rect.x += self.vx
        self.vy += self.gravidade
        self.rect.y += self.vy
        self.rotacionar_imagem() # rotacionando a imagem
        # Verificando colisão com o chão
        if self.rect.y >= 500: # chão settado para 500
            self.kill()
            explosao = Explosao(self.rect.center)
            explosoes_group.add(explosao)
            som_explosao.play()
        # Verifique se o míssil atingiu o jogador
        if self.rect.colliderect(player.rect):
            self.kill()
            player.vida -= 10 # dano do míssil
            explosao = Explosao(self.rect.center)
            explosoes_group.add(explosao)
            som_explosao.play()

    def rotacionar_imagem(self):
        angulo_graus = math.degrees(math.atan2(self.vy, self.vx))
        # Rotaciona a imagem original para o ângulo calculado
        self.image = pygame.transform.rotate(self.original_image, -angulo_graus)
        # Atualiza o retângulo da imagem
        #self.rect = self.image.get_rect(center=self.rect.center)

class Explosao(pygame.sprite.Sprite): # classe explosao, instancias no colliderect do missil com player
    def __init__(self, posicao):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for n in range(len(os.listdir(f'Image\Explosão'))): # loop do diretorio de imagens
            img = pygame.image.load(f'Image\Explosão\{n}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 3))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (posicao[0], posicao[1] - 300)
        self.fps = 300
        self.count_cooldown = 0
        self.delay = int(1000/self.fps) # delay do ataque

    def update(self): # update de frames da explosao
        self.count_cooldown += 1
        if self.count_cooldown >= self.delay:
            self.count_cooldown = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill() # remove a explosão quando acabarem os frames
            else:
                self.image = self.images[self.frame_index]

class Laser(pygame.sprite.Sprite): # classe laser, ataque do boss
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = []
        for n in range(len(os.listdir('Image\\bullet\laser'))): # loop do diretorio
            img = pygame.image.load(f'Image\\bullet\laser\laser_{n}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.fps = 60
        self.count_cooldown = 0
        self.delay = int(1000/self.fps) # delay do ataque
        self.laser_duration = 0

    def update(self, player): # update dos frames da animacao
        self.count_cooldown += 1
        self.laser_duration += 1
        if self.count_cooldown >= self.delay:
            self.count_cooldown = 0
            self.frame_index += 1
            if self.frame_index > len(self.images) - 1:
                self.frame_index = len(self.images) - 1
            self.image = self.images[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            if self.image == self.images[3]:
                self.rect.center = (self.x - 1000, self.y)
        if self.laser_duration >= 100:
            self.kill() # dado um tempo, self.kill(Laser) para remover o laser da tela

        # dano
        if self.rect.colliderect(player.rect):  # danos no player por colisao
            player.vida -= 0.1 # dano do laser

# Sprite Grups       
weapons_group = pygame.sprite.Group()
shotgun_blast_group = pygame.sprite.Group() 
missil_group = pygame.sprite.Group()
explosoes_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()