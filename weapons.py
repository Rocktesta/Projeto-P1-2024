import pygame
#Scrpits para as armas

class Shotgun(pygame.sprite.Sprite):
    def __init__(self,  x, y, sprite="Weapons\Shotgun_sprite.png", cooldown=1, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * escala, self.sprite.get_height() * escala))
        self.rect = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())
        self.cooldown = cooldown
        self.equipada = False
    def draw(self, tela):
        if self.equipada == False:
            tela.blit(self.sprite, (self.rect.x , self.y))
    def update(self, player):
        if self.rect.colliderect(player):
            self.equipada = True
            #player.char_type = 'player_Kiev_shotgun' # mudar o sprite do player
            self.kill()
         
        
weapons_group = pygame.sprite.Group() #Grupo