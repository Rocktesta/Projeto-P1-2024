import pygame
#Scrpits para as armas

altura = 10
largura = 20

class Municao:
    def __init__(self, x, y): # incializa objeto municao com quantidade = 10
        self.rect = pygame.Rect(x, y,  40, 12)
        self.qnt = 10

class Pistol: #pistola
    def __init__(self, x, y, altura, largura):
        self.rect = pygame.Rect(x, y, 20, 10)

    def update_position(self, x, y):
        # Atualiza a posição da pistola para acompanhar o jogador
        self.rect.x = x + 35  # Ajuste conforme necessário para a posição da pistola em relação ao jogador
        self.rect.y = y + 5  # Ajuste conforme necessário para a posição da pistola em relação ao jogador

    
class Balas:
    def __init__(self, x, y, tela):
        self.rect_bala = pygame.Rect(x + 10, y, 10, 10)
        self.tela = tela

    def fogo(self, x, y, municao, player_dir):
        if municao > 0 and player_dir == 'right':
            self.rect_bala.x = x
            self.rect_bala.y = y
            pygame.draw.rect(self.tela, (255, 255, 255), self.rect_bala)
            municao -= 1
        elif municao > 0 and player_dir == 'left':
            self.rect_bala.x = x - 200
            self.rect_bala.y = y
            pygame.draw.rect(self.tela, (255, 255, 255), self.rect_bala)
            municao -= 1
        return municao
            

