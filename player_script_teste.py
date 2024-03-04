import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, escala, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.velocidade = velocidade
        self.dirececao = 1
        self.flip = False
        img_player = pygame.image.load(f'imagens\{self.char_type}.png')
        self.img_player = pygame.transform.scale(img_player, (img_player.get_width()/2, img_player.get_height()/2))
        self.player_rect = self.img_player.get_rect()
        self.player_rect.center = (x, y)
        
    def move(self, mooving_left, mooving_right):
        # reset as variáveis de movimento
        dx = 0
        dy = 0
        # checando se o player se move para a direita ou esquerda
        if mooving_left:
            dx = -self.velocidade
            self.flip = True
            self.dirececao = -1
        if mooving_right:
            dx = +self.velocidade
            self.flip = False
            self.dirececao = 1
        # updade da posição do player_rect
        self.player_rect.x += dx
        self.player_rect.y += dy

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.img_player, self.flip, False), self.player_rect)
    