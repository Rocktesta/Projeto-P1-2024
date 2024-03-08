import pygame
import player_script_teste
import pygame_gui
import weapons
from Bar_vida_script import HealthBar
from Item_vida_script import Coxinha
from weapons import Shotgun

pygame.init()

largura_tela = 1280
altura_tela = 720

tela = pygame.display.set_mode((largura_tela, altura_tela))
manager = pygame_gui.UIManager((largura_tela, altura_tela))
botao_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2), (100, 50)),text='Play', manager=manager)
botao_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2 + 100), (100, 50)),text='Exit', manager=manager)
background = pygame.image.load("Trecho_teste.png").convert_alpha()

# framerate
clock = pygame.time.Clock()
fps = 60

def menu():
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Saindo da função e encerrando o loop do jogo
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == botao_play:
                        play()
                    elif event.ui_element == botao_quit:
                        pygame.quit()
                        return

        manager.process_events(event)  # Processa eventos da GUI

        # Atualiza e desenha a GUI
        
        manager.update(fps)
        manager.draw_ui(tela)

        pygame.display.update()





BG = (152, 152, 152) 
def draw_bg():
    pygame.draw.line(tela, (0, 0, 0), (0, 600), (largura_tela, 600))

def play():
    pygame.display.set_caption('PLAY')

    # Variáveis do jogo
    gravidade = 0.75
    back_x = 0
    fonte = pygame.font.SysFont("Arial", 36)
    white = (255, 255, 255)
    

    # Movimentações do Player
    mooving_left = False
    mooving_right = False
    shoot = False
    equipada = True

    player = player_script_teste.Player('soldier', 300, 600, 3, gravidade, 3)
    barra_vida = HealthBar(50, 50, 190, 20, 100)
    coxinha = Coxinha(1300, 500, 20, 20)
    shotgun = Shotgun(1200, 300)
    
    #armas
    weapons_group = weapons.weapons_group
    weapons_group.add(shotgun)

    # inimigos
    inimigo_group = player_script_teste.inimigo_group
    inimigo1 = player_script_teste.Inimigo('soldier', 700, 600, 3, gravidade, 3)
    inimigo2 = player_script_teste.Inimigo('soldier', 400, 600, 3, gravidade, 3)
    inimigo_group.add(inimigo1)
    inimigo_group.add(inimigo2)

    
    # Loop Principal do Jogo
    running = True
    while running:
        
        clock.tick(fps)

        pygame.Surface.fill(tela, BG)
        tela.blit((background), (back_x, 0))
        player_bullet_group = player_script_teste.player_bullet_group
        player_text = fonte.render(f"Player {inimigo1.vida}", True, (0, 0, 0))
        tela.blit(player_text, (player.rect.x + 10, player.rect.y - 50))
        player.update()
        player.draw(tela)
        shotgun.draw(tela)
        shotgun.update(player)
        barra_vida.draw(tela)
        coxinha.draw(tela)

        for inimigo in inimigo_group:
            inimigo.ai(player)
            inimigo.update()
            inimigo.draw(tela)
            player_bullet_group.update(inimigo, 'inimigo')

        # updade e draw sprite groups
        
        
        player_bullet_group.draw(tela)
        inimigo_bullet_group = player_script_teste.inimigo_bullet_group
        inimigo_bullet_group.update(player, 'player')


        inimigo_bullet_group.draw(tela)
        if coxinha.render == True:
            vida = coxinha.update(player.rect)
            player.vida += vida
        barra_vida.update(player.vida)

        # updade das ações do player
        if player.vivo:
            # shoot bullets
            if shoot:
                player.shoot('inimigo')
            if player.no_ar:
                player.update_action(2) # animação de pulo
            elif mooving_left or mooving_right:
                player.update_action(1) # animação de corrida
            else:
                player.update_action(0) # retorna para o idle
            tela_scroll =  player.move(mooving_left, mooving_right) 
            

            inimigo1.rect.x += tela_scroll
            inimigo2.rect.x += tela_scroll
            coxinha.rect.x += tela_scroll
            back_x += tela_scroll
            shotgun.rect.x += tela_scroll
        
        else:
            player
        for event in pygame.event.get():   # Loop para lidar com eventos
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()                 # jogo para de rodar se apertar o x da aba do jogo
            elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
                if event.key == pygame.K_ESCAPE:   # Se for tecla escape, jogo para de rodar
                    running = False 
                    pygame.quit()
            # Pressionar teclas no teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mooving_left = True
                if event.key == pygame.K_d:
                    mooving_right = True
                if event.key == pygame.K_RETURN:
                    shoot = True
                if event.key == pygame.K_SPACE and player.alive:
                    player.jump = True
            # Soltar teclas no teclado
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mooving_left = False
                if event.key == pygame.K_d:
                    mooving_right = False
                if event.key == pygame.K_RETURN:
                    shoot = False
            
        pygame.display.update()

menu()