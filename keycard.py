import pygame

class Keycard(pygame.sprite.Sprite):
    def __init__(self, x, y, tela, player):
        pygame.sprite.Sprite.__init__(self)
        self.tela = tela
        self.images = player.keycard
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 4, 4)
        self.render = True
        self.frame_index = 0
        self.update_tempo = 0
        self.cooldown_animacao = 100

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.com_keycard = True
            self.render = False
        
    def draw (self):
        if self.render:
            sprite = self.images[self.frame_index]
            # check se passou tempo suficiente desde o último update
            if pygame.time.get_ticks() - self.update_tempo > self.cooldown_animacao:
                self.update_tempo = pygame.time.get_ticks()
                self.frame_index += 1
            # se a animação chegar no final ela reinicia
            if self.frame_index >= len(self.images):
                self.frame_index = 0
            self.tela.blit(sprite, self.rect)

       