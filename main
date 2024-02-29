import pygame
from player import Player
from weapons import Pistol

pygame.init()

# Obtendo as dimensões da tela do sistema
info = pygame.display.Info()
largura_tela = 1280
altura_tela = 720

tela = pygame.display.set_mode((largura_tela, altura_tela))
obj_player = Player(largura_tela//2, altura_tela //2, 40, 40)  # Corrigido para Player
obj_pistol = Pistol(obj_player.rect.x, obj_player.rect.y + 20, 20, 10)  # Corrigido para Pistol

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():   # Loop para lidar com eventos
        if event.type == pygame.QUIT:
            running = False                 # jogo para de rodar se apertar o x da aba do jogo
        elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
            if event.key == pygame.K_SPACE:   # Se for tecla espaco, jogo para de rodar
                running = False 

    obj_player.movimento(0,0) #metodo de movimento
    obj_pistol.update_position(obj_player.rect.x, obj_player.rect.y + 20) #metodo de movimento para acompanhar o player

    font = pygame.font.SysFont("Arial", 36)
    white = (255, 255, 255)

    tela.fill((0, 0, 0))      # fundo 0, 0, 0
    pygame.draw.rect(tela, (0, 0, 255), obj_player.rect) #desenho de um rectangulo, com base no rect do obj player
    pygame.draw.rect(tela, (255, 0, 0), obj_pistol.rect) #desenho de um retangulo na cor vermelha
    x_position_text = font.render(f"X Position: {obj_player.rect.x}", True, white) # posicao do player
    y_position_text = font.render(f"Y Position: {obj_player.rect.y}", True, white) # posicao do player
    tela.blit(x_position_text, (10, 10))  # Posição do texto X
    tela.blit(y_position_text, (10, 50))   # Posição do texto Y
    pygame.display.flip()     # updates da tela
    
    pygame.time.Clock().tick(60)    # taxa de quadros 60 fps

pygame.quit()
