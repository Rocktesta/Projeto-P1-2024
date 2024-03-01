import pygame
import time
from player_script import Player
from weapons import Pistol
from Item_vida_script import Coxinha
from Municao_script import Municao
from piso_script import Piso
from camera import Camera
pygame.init()

# Obtendo as dimensões da tela do sistema
info = pygame.display.Info()
largura_tela = 1280
altura_tela = 720

gravidade = 0.4
tela = pygame.display.set_mode((largura_tela, altura_tela))
obj_piso = Piso(0, 600)
obj_municao = Municao(300, obj_piso.rect.top - 50)
obj_pistol = Pistol(500, 500, 20, 10)  # Corrigido para Pistol
obj_coxinha = Coxinha(250, obj_municao.rect.top - 60)
obj_player = Player(largura_tela//2, obj_piso.rect.top - 70, 32, 64)  # Corrigido para Player
obj_camera = Camera(obj_player)
vida = obj_player.vida
municao = obj_player.municao 

lista_game_objs = [obj_coxinha, obj_player, obj_pistol, obj_municao] # lista de objetos, usada para o consumo de itens

arma_equipada = False  # booleana para armas

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():   # Loop para lidar com eventos
        if event.type == pygame.QUIT:
            running = False                 # jogo para de rodar se apertar o x da aba do jogo
        elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
            if event.key == pygame.K_ESCAPE:   # Se for tecla escape, jogo para de rodar
                running = False 
    tecla_press = pygame.key.get_pressed( )     # Obtem os teclas
    if tecla_press[pygame.K_a] or tecla_press[pygame.K_LEFT] and obj_player.velocidade_x > - 10:
        obj_player.velocidade_x -= 1
    if tecla_press[pygame.K_d] or tecla_press[pygame.K_RIGHT] and obj_player.velocidade_x < 10:
        obj_player.velocidade_x += 1
    if  tecla_press[pygame.K_SPACE] and obj_player.pulo == False:
        obj_player.velocidade_y -= 10
        obj_player.pulo = True
    if obj_player.velocidade_x != 0:
        if obj_player.velocidade_x > 0:
            obj_player.velocidade_x -= 0.4
            round(obj_player.velocidade_x)
        else:
            obj_player.velocidade_x += 0.4
            round(obj_player.velocidade_x)
    obj_player.movimento() #metodo de movimento
   



    if arma_equipada == True:
        obj_pistol.update_position(obj_player.rect.x, obj_player.rect.y + 20) 

    fonte = pygame.font.SysFont("Arial", 36)
    white = (255, 255, 255)

    tela.fill((0, 0, 0))      # fundo 0, 0, 0
    pygame.draw.rect(tela, (0, 0, 255), obj_player.rect) #desenho de um rectangulo, com base no rect do obj player
    pygame.draw.rect(tela, (255, 0, 0), obj_pistol.rect) #desenho de um retangulo na cor vermelha
    pygame.draw.rect(tela, (255, 255, 255), obj_piso.rect)
    if obj_coxinha in lista_game_objs:
        pygame.draw.rect(tela, (230, 139, 39), obj_coxinha) #desenho do item coxinha(vida)
    if obj_municao in lista_game_objs:
        pygame.draw.rect(tela, (255, 201, 39), obj_municao) #desenho do item municao
    x_position_text = fonte.render(f"X Position: {obj_player.rect.x}", True, white) # posicao do player
    y_position_text = fonte.render(f"Y Position: {obj_player.rect.y}", True, white) # posicao do player
    vida_text = fonte.render(f"Vida: {vida}", True, white) # vida do player
    municao_text = fonte.render(f"Municão: {municao}", True, white) # municao do jogador
    arma_equip_text = fonte.render(f"Arma: Pistola",  True, white) # Arma que esta sendo usado
    

    tela.blit(x_position_text, (10, 10))  # Posição do texto X
    tela.blit(y_position_text, (10, 50))   # Posição do texto Y
    tela.blit(vida_text, (10, 100)) # posicao texto vida
    tela.blit(municao_text, (10, 150)) # posicao texto vida
    if arma_equipada == True:   # apenas se arma estiver equipada o texto aparece (pre-alpha)
        tela.blit(arma_equip_text, (750, 600))

    #colisoes  entre os objetos (remove objetos apos uso ou equipa)
    if obj_coxinha.rect.colliderect(obj_player) == 1 and obj_coxinha in lista_game_objs: 
        vida += obj_coxinha.vida
        lista_game_objs.remove(obj_coxinha)
    if obj_municao.rect.colliderect(obj_player) == 1 and obj_municao in lista_game_objs:
        municao +=  obj_municao.qnt
        lista_game_objs.remove(obj_municao)
    if obj_pistol.rect.colliderect(obj_player) == 1:
        arma_equipada = True
    if obj_player.rect.colliderect(obj_piso): 
        obj_player.velocidade_y = 0
        obj_player.pulo = False
    else:
        obj_player.velocidade_y += gravidade
   
        




    pygame.display.flip()     # updates da tela
    
    pygame.time.Clock().tick(60)    # taxa de quadros 60 fps

pygame.quit()
