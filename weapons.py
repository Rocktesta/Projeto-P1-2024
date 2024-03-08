import pygame
from pygame.sprite import _Group

#Scrpits para as armas

class shotgun(pygame.sprite.Sprite):
    def __init__(self, tela, x, y, sprite, cooldown=1):
        pygame.sprite.Sprite.__init__(self)
        self.tela = tela
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.rect = pygame.rect(x, y, (self.sprite.get_width, self.sprite.get_height))
        self.cooldown = cooldown
        self.equip = False
    def equip(self, equipada, player):
        if equipada == True:
            self.equip = True
        self.rect.x = player.rect.x 
        self.rect.y = player.rect.y
        
