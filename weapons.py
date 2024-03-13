import pygame
from random import randint
#Scrpits para as armas

def nova_posicao_item(player, tela_scroll):
        # gera uma posição aleatória para o item
        pos = [randint(400,1200) + tela_scroll, randint(400, 600) + tela_scroll]
        while pos[0] == player.rect.x:
            pos = [randint(100,1200), randint(400, 600)]
        return pos

class Shotgun(pygame.sprite.Sprite):
    def __init__(self, player, tela_scroll=0, sprite="Weapons\Shotgun_sprite.png", cooldown=1, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.pos = nova_posicao_item(player, tela_scroll)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * escala, self.sprite.get_height() * escala))
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        self.cooldown = cooldown
        self.equipada = False

    @staticmethod
    def gerar_shotgun(player, tela_scroll=0):
        shotgun_group = pygame.sprite.Group()
        if randint(1, 10) == 1:
            shotgun = Shotgun(player, tela_scroll) 
            shotgun_group.add(shotgun)
        return shotgun_group

    def draw(self, tela):
        if self.equipada == False:
            tela.blit(self.sprite, (self.rect.x , self.y))
    def update(self, player):
        if self.rect.colliderect(player):
            self.equipada = True
            #player.char_type = 'player_Kiev_shotgun' # mudar o sprite do player
            self.kill()

# Sprite Grups       
weapons_group = pygame.sprite.Group() 