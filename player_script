import pygame
#Script do player

altura = 50
largura = 50

class Player:  #classe do jogador
    def __init__(self, x, y, largura, altura):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, largura, altura)

    def movimento(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        tecla_pressionada = pygame.key.get_pressed()
        if tecla_pressionada[pygame.K_LEFT] or tecla_pressionada[pygame.K_a]:
            self.rect.x -= 3
        if tecla_pressionada[pygame.K_RIGHT] or tecla_pressionada[pygame.K_d]:
            self.rect.x += 3
        if tecla_pressionada[pygame.K_UP] or tecla_pressionada[pygame.K_w]:
            self.rect.y -= 3
        if tecla_pressionada[pygame.K_DOWN] or tecla_pressionada[pygame.K_s]:
            self.rect.y += 3
