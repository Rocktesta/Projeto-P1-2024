import pygame
import pygame_gui
import player_script
import vida_script
import weapons
from weapons import Shotgun
import boss_script
from boss_script import Boss
import keycard

pygame.init()

largura_tela = 1280
altura_tela = 720

tela = pygame.display.set_mode((largura_tela, altura_tela))
manager = pygame_gui.UIManager((largura_tela, altura_tela))
botao_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2), (100, 50)),text='Play', manager=manager)
botao_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 50, altura_tela//2 + 100), (100, 50)),text='Exit', manager=manager)
background = pygame.image.load("Image\\background.png").convert_alpha()
background = pygame.transform.scale(background, (background.get_width() * 3, background.get_height() * 3))

#cooldowns
tempo_ultima_geracao_coxinhas = 0
cooldown_novas_coxinhas = 5000
tempo_ultima_geracao_shotgun = 0
cooldown_nova_shotgun = 5000

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
    moving_left = False
    moving_right = False
    shoot = False
    equipada = True
    fire_cooldown = 300
    shoot_anima = False
    start_time = 0

    player = player_script.Player(300, 600, 3, gravidade, 3)
    
    barra_vida = vida_script.HealthBar(50, 50, 190, 20, 100)
    cracha = keycard.Keycard(2000, 400, tela, player)
    tela_scroll = 0

    # criando armas
        #shotgun
    shotgun_group = pygame.sprite.Group()

    # criando coxinhas
    coxinha_group = vida_script.Coxinha.gerar_coxinhas(player)

    # inimigos
    inimigo_group = player_script.inimigo_group
    inimigo1 = player_script.Inimigo('inimigo_robo', 700, 700, 2, gravidade, 3.5)
    #inimigo2 = player_script.Inimigo('inimigo_robo', 900, 700, 2, gravidade, 3.5)
    inimigo_group.add(inimigo1)
    #inimigo_group.add(inimigo2)

    boss = Boss(2560, 420)
    
    # Loop Principal do Jogo
    running = True
    while running:
        
        clock.tick(fps)

        pygame.Surface.fill(tela, BG)
        tela.blit((background), (back_x, 0))
        player_bullet_group = player_script.player_bullet_group
        #player_text = fonte.render(f"Player {inimigo1.vida}", True, (0, 0, 0))
        #tela.blit(player_text, (player.rect.x, player.rect.y - 50))
        player.update()
        player.draw(tela)
        player.check_vivo()
        cracha.draw()
        for shotgun in shotgun_group:
            shotgun.draw(tela)
            shotgun.update(player)
        barra_vida.draw(tela)
        for coxinha in coxinha_group:
            coxinha.draw(tela)
        for inimigo in inimigo_group:
            inimigo.ai(player, tela)
            inimigo.update()
            inimigo.draw(tela)
        boss.ai(player, tela)
        boss.update()
        boss.draw(tela)
        

        # updade e draw sprite groups
        player_bullet_group.update(inimigo_group, 'inimigo', player) # update de colisão tiro com inimigo
        player_bullet_group.draw(tela)
        player_bullet_hit_group = player_script.player_bullet_hit_group
        player_bullet_hit_group.update()
        player_bullet_hit_group.draw(tela)
        inimigo_bullet_group = player_script.inimigo_bullet_group
        inimigo_bullet_group.update(player, 'player', player)
        inimigo_bullet_group.draw(tela)
        missil_group = boss_script.missil_group
        missil_group.update(player)
        missil_group.draw(tela)
        explosoes_group = weapons.explosoes_group
        explosoes_group.update()
        explosoes_group.draw(tela)
       
        posicao_player_boss = (boss.rect.centerx - player.rect.centerx, boss.rect.centery - player.rect.centery)

        if player.mask.overlap(boss.mask, posicao_player_boss):
            print("colide")

        for coxinha in coxinha_group:
           if coxinha.render == True:
                vida = coxinha.update(player)
                player.vida += vida
        barra_vida.update(player.vida)
        # Gerando mais coxinhas se o player estiver se movimentando
        if moving_left or moving_right:
            tempo_atual_coxinha = pygame.time.get_ticks()
            global tempo_ultima_geracao_coxinhas
            if tempo_atual_coxinha - tempo_ultima_geracao_coxinhas >= cooldown_novas_coxinhas:
                # Gere novas coxinhas
                coxinha_group.add(vida_script.Coxinha.gerar_coxinhas(player, tela_scroll))
                tempo_ultima_geracao_coxinhas = tempo_atual_coxinha

        # Gerando novas shotguns se o player estiver se movimentando
        if moving_left or moving_right:
            tempo_atual_shotgun = pygame.time.get_ticks()
            global tempo_ultima_geracao_shotgun
            if tempo_atual_shotgun - tempo_ultima_geracao_shotgun >= cooldown_nova_shotgun:
                # Gere nova shotgun
                shotgun_group.add(Shotgun.gerar_shotgun(player, tela_scroll))
                tempo_ultima_geracao_shotgun = tempo_atual_shotgun

        # updade das ações do player
        if player.vivo:
            # shoot bullets
            if shoot:
                player.shoot('bullet0', tela)
            tela_scroll =  player.move(moving_left, moving_right) 
            back_x += tela_scroll * 0000.1
            
            for inimigo in inimigo_group:
                inimigo.rect.x += tela_scroll
            for coxinha in coxinha_group:
                coxinha.rect.x += tela_scroll
            back_x += tela_scroll
            for shotgun in shotgun_group:
                shotgun.rect.x += tela_scroll
            boss.rect.x += tela_scroll
            cracha.rect.x += tela_scroll
        
        elif player.vivo == False:
            player.update_action(3)
        for event in pygame.event.get():   # Loop para lidar com eventos
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()                 # jogo para de rodar se apertar o x da aba do jogo
            elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
                if event.key == pygame.K_ESCAPE:   # Se for tecla escape, jogo para de rodar
                    running = False 
                    pygame.quit()
                elif event.key == pygame.K_RETURN:
                    temp_inicial = pygame.time.get_ticks()
        # Pressionar teclas no teclado
        if player.vivo:
            if player.shotgun_equip:
                shoot_anima = 400
            else:
                 shoot_anima = 300
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_RETURN]:
                temp_atual = pygame.time.get_ticks()
                
                if temp_atual - temp_inicial >= fire_cooldown:
                    shoot_anima = True
                else:
                    shoot_anima = False
            if teclas[pygame.K_a] and teclas[pygame.K_RETURN]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(4)
                    else:
                        player.update_action(9)
                    shoot = True
                moving_left = True
                moving_right = False
            elif teclas[pygame.K_d] and teclas[pygame.K_RETURN]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(4)
                    else:
                        player.update_action(9)
                    shoot = True
                moving_right = True
                moving_left = False
            elif teclas[pygame.K_d] and not teclas[pygame.K_RETURN]:
                if not player.shotgun_equip:
                    player.update_action(1)
                else:
                    player.update_action(6)
                shoot = False
                moving_right = True
                moving_left = False
            elif teclas[pygame.K_a] and not teclas[pygame.K_RETURN]:
                if not player.shotgun_equip:
                    player.update_action(1)
                else:
                    player.update_action(6)
                shoot = False
                moving_left = True
                moving_right = False
            elif teclas[pygame.K_RETURN]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(5)
                    else:
                        player.update_action(8)
                    shoot = True
                moving_left = False
                moving_right = False
            elif not teclas[pygame.K_a] and  not teclas[pygame.K_d]:
                if not player.shotgun_equip:
                    player.update_action(0)
                else:
                    player.update_action(7)
                shoot = False
                moving_left = False
                moving_right = False
            if teclas[pygame.K_SPACE] and not teclas[pygame.K_a] and not teclas[pygame.K_d]:
                player.update_action(2)
                shoot = False
                moving_left = False
                moving_right = False
                player.jump = True
            elif teclas[pygame.K_SPACE] and teclas[pygame.K_a] and not teclas[pygame.K_d]:
                player.update_action(2)
                shoot = False
                moving_left = True
                moving_right = False
                player.jump = True
            elif teclas[pygame.K_SPACE] and not teclas[pygame.K_a] and teclas[pygame.K_d]:
                player.update_action(2)
                shoot = False
                moving_left = False
                moving_right = True
                player.jump = True
            if not teclas[pygame.K_SPACE]:
                player.jump = False
            
            
        
        
        
           
                        
        pygame.display.update()

menu()