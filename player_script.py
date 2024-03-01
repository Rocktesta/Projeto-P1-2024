import pygame
#Script do player

class Player:  #classe do jogador
    def __init__(self, x, y, largura, altura):  #inicializa o objeto jogador
        self.rect = pygame.Rect(x, y, largura, altura)
        self.vida = 100
        self.municao = 30
        self.velocidade_x = 5
        self.velocidade_y = 30
        self.pulo = False

    def movimento(self, dx, dy):
        velocidade = 0
        self.rect.x += dx
        self.rect.y += dy

        tecla_pressionada = pygame.key.get_pressed()
        if tecla_pressionada[pygame.K_LEFT] or tecla_pressionada[pygame.K_a]:
            self.rect.x -= self.velocidade_x
        if tecla_pressionada[pygame.K_RIGHT] or tecla_pressionada[pygame.K_d]:
            self.rect.x += self.velocidade_x
        if tecla_pressionada[pygame.K_UP] or tecla_pressionada[pygame.K_w] and self.pulo == False:
            self.rect.y -= self.velocidade_y
            self.pulo == True
        
