import pygame
from player_script import Player
import weapons
from Item_vida_script import Coxinha
from piso_script import Piso
from botao import Botao
from Bar_vida_script import HealthBar
from weapons import Balas

pygame.init()

# Obtendo as dimensões da tela do sistema
largura_tela = 1280
altura_tela = 720
tela_scroll = 0
tela = pygame.display.set_mode((largura_tela, altura_tela))
background = pygame.image.load("Trecho_teste.png").convert_alpha()
player_sprite =  pygame.image.load("Player_sprite_k.png").convert_alpha()
pygame.display.set_caption('MENU')

def main_menu(): # tela do menu principal 
    while True:
        tela.fill((0, 0, 0)) #tela preta, pode ser colocado algum outro fundo

        menu_mouse_pos = pygame.mouse.get_pos()

        #menu_texto = pygame.font.SysFont('Arial', 50)

        # Botões que aparecem na tela
        play_botao = Botao(imagem = None, texto_input='Jogar', pos=(640, 250), fonte=pygame.font.SysFont('Arial', 36), cor_base='#d7fcd4', cor_hoover='White')
        quit_botao = Botao(imagem = None, texto_input='Sair', pos=(640, 400), fonte=pygame.font.SysFont('Arial', 36), cor_base='#d7fcd4', cor_hoover='White')

        
        for botao in [play_botao, quit_botao]:
            botao.mudarcor(menu_mouse_pos)
            botao.update(tela, menu_mouse_pos)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if play_botao.checarinput(menu_mouse_pos):
                    play()
                if quit_botao.checarinput(menu_mouse_pos):
                    pygame.quit()



def play():
    pygame.display.set_caption('Play')
    
    while True:
        player_dir ='right'
        gravidade = 0.4
        background_1 = 0
        obj_piso = Piso(0, 600)
        obj_municao = weapons.Municao(300, obj_piso.rect.top - 50)
        obj_coxinha = Coxinha(250, obj_municao.rect.top - 60)
        obj_player = Player(largura_tela//2, obj_piso.rect.top - 70, 32, 64, player_sprite)  # Corrigido para Player
        obj_pistol = weapons.Pistol(500 , 500 , 20, 10)  # Corrigido para Pistol
        vida = obj_player.vida
        obj_health = HealthBar(10, 100, 150, 25, vida)
        obj_bala = Balas(obj_player.rect.x + 40 ,obj_player.rect.y, tela)
        municao = obj_player.municao 

        lista_game_objs = [obj_coxinha, obj_player, obj_municao] # lista de objetos, usada para o consumo de itens

        arma_equipada = False  # booleana para armas

        # Loop principal do jogo
        running = True
        while running:
            tela.fill((0, 0, 0))
            tela.blit((background), (background_1 , 0))
            for event in pygame.event.get():   # Loop para lidar com eventos
                if event.type == pygame.QUIT:
                    running = False                 # jogo para de rodar se apertar o x da aba do jogo
                elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
                    if event.key == pygame.K_ESCAPE:   # Se for tecla escape, jogo para de rodar
                        running = False 
            tecla_press = pygame.key.get_pressed( )     # Obtem os teclas
            if tecla_press[pygame.K_a] or tecla_press[pygame.K_LEFT] and obj_player.velocidade_x > - 6:
                obj_player.velocidade_x -= 3
                player_dir = 'left'
            if tecla_press[pygame.K_d] or tecla_press[pygame.K_RIGHT] and obj_player.velocidade_x < 6:
                obj_player.velocidade_x += 3
                player_dir = 'right'
            if  tecla_press[pygame.K_SPACE] and obj_player.pulo == False:
                obj_player.velocidade_y -= 10
                obj_player.pulo = True
            if obj_player.velocidade_x != 0:
                if obj_player.velocidade_x > 0:
                    obj_player.velocidade_x -= 1
                    round(obj_player.velocidade_x)
                else:
                    obj_player.velocidade_x += 1
                    round(obj_player.velocidade_x)
            if tecla_press[pygame.K_f] and municao > 0 and arma_equipada:
                municao = obj_bala.fogo(obj_pistol.rect.x + 100, obj_pistol.rect.y, municao, player_dir)
                



            
        

            tela_scroll = obj_player.movimento() #metodo de movimento
            
            obj_pistol.rect.x += tela_scroll
           

            obj_piso.rect.x += tela_scroll
            

            obj_coxinha.rect.x += tela_scroll
            

            obj_municao.rect.x += tela_scroll
            background_1 += tela_scroll
           

            obj_health.update(vida)
            



           

            if arma_equipada == True:
                if player_dir == 'right' :
                    obj_pistol.update_position(obj_player.rect.x, obj_player.rect.y + 20) 
                else:
                     obj_pistol.update_position(obj_player.rect.x - 60, obj_player.rect.y + 20) 

            fonte = pygame.font.SysFont("Arial", 36)
            white = (255, 255, 255)
            
            
            
            pygame.draw.rect(tela, (0, 128, 0), obj_player.rect)
            pygame.draw.rect(tela, (128, 128, 128), (0,0,350, 150))
            pygame.draw.rect(tela, (255, 0, 0), obj_pistol.rect) #desenho de um retangulo na cor vermelha
            pygame.draw.rect(tela, (255, 255, 255), obj_piso.rect)
            obj_health.draw(tela)
            if obj_coxinha in lista_game_objs:
                pygame.draw.rect(tela, (230, 139, 39), obj_coxinha) #desenho do item coxinha(vida)
            if obj_municao in lista_game_objs:
                pygame.draw.rect(tela, (255, 201, 39), obj_municao) #desenho do item municao
            x_position_text = fonte.render(f"X Position: {obj_player.velocidade_x}", True, white) # posicao do player
            y_position_text = fonte.render(f"Y Position: {obj_player.rect.y}", True, white) # posicao do player
            vida_text = fonte.render(f"Vida: {vida}", True, white) # vida do player
            municao_text = fonte.render(f"Municão: {municao}", True, white) # municao do jogador
            arma_equip_text = fonte.render(f"Arma: Pistola",  True, white) # Arma que esta sendo usado
            

            tela.blit(x_position_text, (10, 10))  # Posição do texto X
            tela.blit(y_position_text, (10, 50))   # Posição do texto Y
            tela.blit(vida_text, (10, 100)) # posicao texto vida
            tela.blit(municao_text, (180, 100)) # posicao texto vida
            if arma_equipada == True:   # apenas se arma estiver equipada o texto aparece (pre-alpha)
                tela.blit(arma_equip_text, (750, 650))

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

main_menu()
