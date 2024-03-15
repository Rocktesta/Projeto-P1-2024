import pygame
import numpy
import math
import os
#Scrpits para as armas e balas

TEMPO_AGORA = 0

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
        self.update_time = pygame.time.get_ticks()
        self.blast_list = []
        self.frame_index = 0
        self.num_frames = len(os.listdir(f'Weapons')) - 1
        for i in range(self.num_frames):
                img = pygame.image.load(f'Weapons\Shotgun_blast{i}.png')
                img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
                self.blast_list.append(img) 

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
            #player.char_dadepe = 'player_Kiev_shotgun' # mudar o sprite do player
            self.kill()

    def draw_blast(self, tela):
        cooldown_animacao = 300  
        
        
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacao:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()  

        imagem_blast = self.blast_list[self.frame_index]
        tela.blit(imagem_blast, (self.player.rect.x - 100, self.player.rect.centery - 150))

        
        if self.frame_index >= self.num_frames:
            self.frame_index = 0
                        
             
         


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
missil_group = pygame.sprite.Group()