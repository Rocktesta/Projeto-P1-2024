import pygame
import player_script
import pygame_gui
import weapons
import vida_script
from weapons import Shotgun

pygame.init()

largura_tela = 1280
altura_tela = 720

tela = pygame.display.set_mode((largura_tela, altura_tela))
manager = pygame_gui.UIManager((largura_tela, altura_tela))
botao_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2), (100, 50)),text='Play', manager=manager)
botao_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2 + 100), (100, 50)),text='Exit', manager=manager)
background = pygame.image.load("Image\\background.png").convert_alpha()
background = pygame.transform.scale(background, (background.get_width() * 4, background.get_height() * 4))

#cooldowns
tempo_ultima_geracao_coxinhas = 0
cooldown_novas_coxinhas = 5000


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

    player = player_script.Player('soldier', 300, 600, 3, gravidade, 3)
    barra_vida = vida_script.HealthBar(50, 50, 190, 20, 100)
    shotgun = Shotgun(1200, 300)

    # criando coxinhas
    #coxinha = vida_script.Coxinha(player)
    coxinha_group = vida_script.Coxinha.gerar_coxinhas(player)

    #armas
    weapons_group = weapons.weapons_group
    weapons_group.add(shotgun)

    # inimigos
    inimigo_group = player_script.inimigo_group
    inimigo1 = player_script.Inimigo('soldier', 700, 600, 3, gravidade, 3)
    inimigo2 = player_script.Inimigo('soldier', 400, 600, 3, gravidade, 3)
    inimigo_group.add(inimigo1)
    inimigo_group.add(inimigo2)

    
    # Loop Principal do Jogo
    running = True
    while running:
        
        clock.tick(fps)

        pygame.Surface.fill(tela, BG)
        tela.blit((background), (back_x, 0))
        player_bullet_group = player_script.player_bullet_group
        player_text = fonte.render(f"Player {inimigo1.vida}", True, (0, 0, 0))
        tela.blit(player_text, (player.rect.x, player.rect.y - 50))
        player.update()
        player.draw(tela)
        shotgun.draw(tela)
        shotgun.update(player)
        barra_vida.draw(tela)
        #coxinha.draw(tela)
        for coxinha in coxinha_group:
            coxinha.draw(tela)

        for inimigo in inimigo_group:
            inimigo.ai(player)
            inimigo.update()
            inimigo.draw(tela)
            player_bullet_group.update(inimigo, 'inimigo') # update de colisão tiro com inimigo

        # updade e draw sprite groups
        player_bullet_group.draw(tela)
        inimigo_bullet_group = player_script.inimigo_bullet_group
        inimigo_bullet_group.update(player, 'player')
        inimigo_bullet_group.draw(tela)

        for coxinha in coxinha_group:
            if coxinha.render == True:
                vida = coxinha.update(player.rect)
                player.vida += vida
        barra_vida.update(player.vida)
        # Gerando mais coxinhas
        if player.move:
            tempo_atual = pygame.time.get_ticks()
            global tempo_ultima_geracao_coxinhas
            if tempo_atual - tempo_ultima_geracao_coxinhas >= cooldown_novas_coxinhas:
                print('fim do cooldown')
                # Gere novas coxinhas
                coxinha_group.add(vida_script.Coxinha.gerar_coxinhas(player))
                tempo_ultima_geracao_coxinhas = tempo_atual

        # updade das ações do player
        if player.vivo:
            # shoot bullets
            if shoot:
                player.shoot('inimigo', 'bullet0')
            #if player.no_ar:
                #player.update_action(2) # animação de pulo
            elif mooving_left or mooving_right:
                player.update_action(1) # animação de corrida
            else:
                player.update_action(0) # retorna para o idle
            tela_scroll =  player.move(mooving_left, mooving_right) 
            

            inimigo1.rect.x += tela_scroll
            inimigo2.rect.x += tela_scroll
            for coxinha in coxinha_group:
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