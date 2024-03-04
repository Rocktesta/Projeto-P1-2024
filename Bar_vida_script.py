import pygame

class HealthBar:
    def __init__(self, x, y, largura, altura, vida):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida_max = 100
        self.vida_atual = vida

    def update(self, nova_vida):
        self.vida_atual = nova_vida

    def draw(self, tela):
        # Draw the background of the health bar (entire bar)
        pygame.draw.rect(tela, (255, 0, 0), (self.x, self.y, self.largura, self.altura))
        
        # Calculate the width of the remaining health bar based on the current health
        largura_restante = (self.vida_atual / self.vida_max) * self.largura
        
        # Draw the remaining health bar
        pygame.draw.rect(tela, (0, 255, 0), (self.x, self.y, largura_restante, self.altura))