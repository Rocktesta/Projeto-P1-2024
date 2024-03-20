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

Musica_played = False
def play_boss_music(musica_anterior, musica_atual):
    global Musica_played
    if not Musica_played:
        musica_anterior.fadeout(1200)
        musica_atual.set_volume(0.9)
        musica_atual.play()
        Musica_played = True

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
    update_camera = False
    update_camera_2 = False
    cam_cooldown = 40

    player = player_script.Player(300, 600, 3, gravidade, tela,  3)
    barra_vida = vida_script.HealthBar(50, 50, 190, 20, 100)
    cracha = keycard.Keycard(3200, 300, tela, player)
    tela_scroll = 0

    # Sons
    pygame.mixer.init()
    Musica_main = pygame.mixer.Sound('Audio\\Musica_main.mp3')
    Musica_boss = pygame.mixer.Sound('Audio\\Musica_boss.mp3')
    win_sound = pygame.mixer.Sound('Audio\\win.mp3')
    Musica_main.play()

    # Imagens
    pistol_img = pygame.image.load('Image\\bullet\pistola.png')
    pistol_img = pygame.transform.scale(pistol_img, (400, 400))
    pistol_bullet_img = pygame.image.load('Image\\bullet\\balas_pistola.png')
    pistol_bullet_img = pygame.transform.scale(pistol_bullet_img, (200, 200))
    shotgun_img = pygame.image.load('Weapons\Shotgun_sprite.png')
    shotgun_img = pygame.transform.scale(shotgun_img, (350, 350))
    shotgun_bullet_img = pygame.image.load('Image\\bullet\shotgun_bullet.png')
    shotgun_bullet_img = pygame.transform.scale(shotgun_bullet_img, (200, 200))

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
    inimigo_group.add(boss)
    
    # Loop Principal do Jogo
    running = True
    while running:
        
        clock.tick(fps)

        pygame.Surface.fill(tela, BG)
        tela.blit((background), (back_x, 0))

        # Munições
        # Munição da shotgun
        if player.shotgun_equip:
            tela.blit(shotgun_img, (150, -115))
            for x in range(player.shotgun_ammo):
                tela.blit(shotgun_bullet_img, (300 + (x * 20), -45))
        # Munição pistola
        else:
            tela.blit(pistol_img, (90, -135))
            tela.blit(pistol_bullet_img, ((300, -35)))
        
        player.update(player.rect.x, player.rect.y, tela)
        player.draw(tela)
        if boss.vivo == False:
            cracha.update(player)
            cracha.draw()
        for shotgun in shotgun_group:
            shotgun.draw(tela)
            shotgun.update(player)
        barra_vida.draw(tela)
        for coxinha in coxinha_group:
            coxinha.draw(tela)
        for inimigo in inimigo_group:
            inimigo.ai(player, tela, tela_scroll)
            inimigo.update()
            inimigo.draw(tela)        

        # updade e draw sprite groups
        player_bullet_group = player_script.player_bullet_group
        player_bullet_group.update(inimigo_group, 'inimigo', player) # update de colisão tiro com inimigo
        player_bullet_group.draw(tela)
        player_bullet_hit_group = player_script.player_bullet_hit_group
        player_bullet_hit_group.update()
        player_bullet_hit_group.draw(tela)
        inimigo_bullet_group = player_script.inimigo_bullet_group
        inimigo_bullet_group.update(player, 'player', player)
        inimigo_bullet_group.draw(tela)
        missil_group = boss_script.missil_group
        missil_group.update(player, tela)
        missil_group.draw(tela)
        explosoes_group = weapons.explosoes_group
        explosoes_group.update()
        explosoes_group.draw(tela)
        laser_group = weapons.laser_group
        laser_group.update(player)
        laser_group.draw(tela)
        
        posicao_player_boss = (boss.rect.centerx - player.rect.centerx, boss.rect.centery - player.rect.centery)

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
                if player.shotgun_equip == False:
                    shotgun_group.add(Shotgun.gerar_shotgun(player, tela_scroll))
                tempo_ultima_geracao_shotgun = tempo_atual_shotgun

    
        # updade das ações do player
        if player.vivo:
            # shoot bullets
            if shoot:
                player.shoot('bullet0', tela)


            tela_scroll =  player.move(moving_left, moving_right) 

            if boss.music:
                play_boss_music(Musica_main, Musica_boss)
                if not update_camera:
                    tela_scroll -= 800
                    player.rect.x -= 700
                    update_camera = True
                if boss.vivo and player.mask.overlap(boss.mask, posicao_player_boss):
                    if moving_right == True:
                            player.velocidade = 0
                    else:
                            player.velocidade = 5
                if tela_scroll > 0:
                    tela_scroll = 0
                if not boss.vivo:
                    cam_cooldown -= 1
                    if not update_camera_2 and cam_cooldown == 0:
                        win_sound.play()
                        win_sound.fadeout(9000)
                        tela_scroll -= 800
                        player.rect.x -= 300
                        update_camera_2 = True
                    



            
                
                




            back_x += tela_scroll * 0000.1

            
            for inimigo in inimigo_group:
                inimigo.rect.x += tela_scroll
            for coxinha in coxinha_group:
                coxinha.rect.x += tela_scroll
            back_x += tela_scroll
            for shotgun in shotgun_group:
                shotgun.rect.x += tela_scroll
            #boss.rect.x += tela_scroll
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
            if player.no_ar == False and teclas[pygame.K_a] and teclas[pygame.K_RETURN] and not teclas[pygame.K_LCTRL]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(4)
                    else:
                        player.update_action(9)
                    shoot = True
                moving_left = True
                moving_right = False
            elif player.no_ar == False and teclas[pygame.K_d] and teclas[pygame.K_RETURN] and not teclas[pygame.K_LCTRL]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(4)
                    else:
                        player.update_action(9)
                    shoot = True
                moving_right = True
                moving_left = False
            elif player.no_ar == False and teclas[pygame.K_d] and not teclas[pygame.K_RETURN] and not teclas[pygame.K_LCTRL]:
                if not player.shotgun_equip:
                    player.update_action(1)
                else:
                    player.update_action(6)
                shoot = False
                moving_right = True
                moving_left = False
            elif player.no_ar == False and  teclas[pygame.K_a] and not teclas[pygame.K_RETURN] and not teclas[pygame.K_LCTRL]:
                if not player.shotgun_equip:
                    player.update_action(1)
                else:
                    player.update_action(6)
                shoot = False
                moving_left = True
                moving_right = False
            elif player.no_ar == False and teclas[pygame.K_RETURN] and not teclas[pygame.K_LCTRL]:
                if shoot_anima:
                    if not player.shotgun_equip:
                        player.update_action(5)
                    else:
                        player.update_action(8)
                    shoot = True
                moving_left = False
                moving_right = False
            elif player.no_ar == False and not teclas[pygame.K_a] and  not teclas[pygame.K_d] and not teclas[pygame.K_LCTRL]:
                if not player.shotgun_equip:
                    player.update_action(0)
                else:
                    player.update_action(7)
                shoot = False
                moving_left = False
                moving_right = False
            if teclas[pygame.K_SPACE] and not teclas[pygame.K_a] and not teclas[pygame.K_d] or player.no_ar == True and not teclas[pygame.K_a] and not teclas[pygame.K_d]:
                if not player.shotgun_equip:
                    player.update_action(2)
                else:
                    player.update_action(12)
                shoot = False
                moving_left = False
                moving_right = False
                player.jump = True
            elif teclas[pygame.K_SPACE] and teclas[pygame.K_a] and not teclas[pygame.K_d] or player.no_ar == True and teclas[pygame.K_a] and not teclas[pygame.K_d]:
                if not player.shotgun_equip:
                    player.update_action(2)
                else:
                    player.update_action(12)
                shoot = False
                moving_left = True
                moving_right = False
                player.jump = True
            elif teclas[pygame.K_SPACE] and not teclas[pygame.K_a] and teclas[pygame.K_d] or player.no_ar == True and not teclas[pygame.K_a] and teclas[pygame.K_d]:
                if not player.shotgun_equip:
                    player.update_action(2)
                else:
                    player.update_action(12)
                shoot = False
                moving_left = False
                moving_right = True
                player.jump = True
            if not teclas[pygame.K_SPACE]:
                player.jump = False
            if teclas[pygame.K_LCTRL] and player.no_ar == False:
                if not player.shotgun_equip:
                    player.update_action(10)
                else:
                    player.update_action(11)
                shoot = False
                moving_left = False
                moving_right = False
                player.crouch = True
            if not teclas[pygame.K_LCTRL]:
                player.crouch = False
                
            
            
        
        
        
           
                        
        pygame.display.update()

menu()