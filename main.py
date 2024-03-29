import pygame
from pyvidplayer import Video
import pygame_gui
import player_script
import vida_script
import weapons
from weapons import Shotgun
import boss_script
from boss_script import Boss
import keycard

pygame.init()

# resolucao 
largura_tela = 1280
altura_tela = 720

#  definicao da tela, ui manager do jogo e load de assets
tela = pygame.display.set_mode((largura_tela, altura_tela))
manager = pygame_gui.UIManager((largura_tela, altura_tela))
botao_play = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 90, altura_tela//2 + 125), (200, 50)),text='Play', manager=manager)
botao_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((largura_tela//2 - 65, altura_tela//2 + 200), (150, 50)),text='Exit', manager=manager)
background = pygame.image.load("Image\\background.png").convert_alpha()
background = pygame.transform.scale(background, (background.get_width() * 3, background.get_height() * 3))
background_menu = pygame.image.load('Assets\TELA_INICIO.jpg')
background_menu = pygame.transform.scale(background_menu, (background_menu.get_width()*1, background_menu.get_height()*1))
game_over_img = pygame.image.load('Assets\GAME_OVER.png')
game_win_img = pygame.image.load('Assets\WIN.png')




#cooldowns
tempo_ultima_geracao_coxinhas = 0
cooldown_novas_coxinhas = 5000
tempo_ultima_geracao_shotgun = 0
cooldown_nova_shotgun = 5000

# framerate
clock = pygame.time.Clock()
fps = 60

# intro inicial video
def intro(rodar_intro=True):
    if rodar_intro == False:
        menu()
    else:
        vid = Video('Assets\INTRODU.mp4')   
        vid.set_size((1280, 720)) # resolucao

        tempo_inicial = pygame.time.get_ticks()

        while True: # se o video parar, vai para o menu
            tempo_atual = pygame.time.get_ticks()
            tempo_decorrido = tempo_atual - tempo_inicial
            if not vid.active:
                menu()
                return

            vid.draw(tela, (0, 0), force_draw=True)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return # saindo da função e encerrando o loop do jogo
                if event.type == pygame.KEYDOWN:
                    vid.close()
                    menu()
            if tempo_decorrido == 19000:
                print('vou fechar')
                vid.close()
                menu()

Menu_play = False
#var global para a musica do menu (flag)
def menu(): # funcao do menu do jogo
    global Menu_play
    running = True
    menu_musica = pygame.mixer.Sound('Audio\\Musica_Menu.mp3')
    if not Menu_play:
        menu_musica.play()
        Menu_play = False
    
    while running:
        clock.tick(fps)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Saindo da função e encerrando o loop do jogo
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED: # eventos dos buttons do pygame_gui
                    if event.ui_element == botao_play:
                        menu_musica.fadeout(2000)
                        menu_musica.stop()
                        play()
                    elif event.ui_element == botao_quit:
                        pygame.quit()
                        return
        
            manager.process_events(event)  # Processa eventos da GUI
        


        # Atualiza e desenha a GUI
        tela.blit(background_menu,(0, 0))   # fundo do menu

        manager.update(fps)
        manager.draw_ui(tela)
        

        pygame.display.update()



BG = (152, 152, 152) 
def draw_bg():
    pygame.draw.line(tela, (0, 0, 0), (0, 600), (largura_tela, 600))

Musica_played = False
# var global para musica do game (flag)
def play_boss_music(musica_anterior, musica_atual): # funcao para alterar as musicas durante gameplay
    global Musica_played
    if not Musica_played:
        musica_anterior.fadeout(1200)
        musica_atual.set_volume(0.9)
        musica_atual.play()
        Musica_played = True

def play(): # funcao principal do jogo
    pygame.display.set_caption('PLAY')
    

    # Variáveis do jogo
    gravidade = 0.75
    back_x = 0
    fonte = pygame.font.SysFont("Arial", 36)
    white = (255, 255, 255)

    # Movimentações do Player , vars de cooldown e flags
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
    cooldown_die = 30

    # instancias dos game objs
    player = player_script.Player(300, 600, 3, gravidade, tela,  3)
    barra_vida = vida_script.HealthBar(50, 50, 190, 20, 100)
    cracha = keycard.Keycard(8300, 300, tela, player)

    # var da camera
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
    inv_wall = pygame.Rect(8700, 0, 230, 830)
    Inv_wall_init = pygame.Rect(300, 0, 230, 830)

    # criando armas
        #shotgun
    shotgun_group = pygame.sprite.Group()

    # criando coxinhas
    coxinha_group = vida_script.Coxinha.gerar_coxinhas(player)

    # inimigos
    inimigo_group = player_script.inimigo_group
    # primeira tela
    inimigo1 = player_script.Inimigo('inimigo_robo', 1790, 700, 2, gravidade, 3.5)
    inimigo2 = player_script.Inimigo('inimigo_robo', 2300, 700, 2, gravidade, 3.5)
    # segunda tela
    inimigo3 = player_script.Inimigo('inimigo_robo', 3180, 700, 2, gravidade, 3.5)
    inimigo4 = player_script.Inimigo('inimigo_robo', 3200, 700, 2, gravidade, 3.5)
    # terceira tela
    inimigo5 = player_script.Inimigo('inimigo_robo', 4935, 700, 2, gravidade, 3.5)
    # inimigo novo x = 4410
    # quarta tela
    # inimigo novo x = 5790
    inimigo6 = player_script.Inimigo('inimigo_robo', 5460, 700, 2, gravidade, 3.5)
    inimigo7 = player_script.Inimigo('inimigo_robo', 6285, 700, 2, gravidade, 3.5)
    inimigo8 = player_script.Inimigo('inimigo_robo', 6240, 700, 2, gravidade, 3.5)
    # inimigo novo x = 6645
    # inimigo novo x = 7542
    inimigo9 = player_script.Inimigo('inimigo_robo', 7095, 700, 2, gravidade, 3.5) 
    inimigo_group.add(inimigo1, inimigo2, inimigo3, 
                      inimigo4, inimigo5, inimigo6, 
                      inimigo7, inimigo8, inimigo9)

    boss = Boss(8000, 420)
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
            # atira balas
            if shoot:
                player.shoot('bullet0', tela)
            if player.com_keycard:
                tela.blit(game_win_img, (0, 0))


            tela_scroll =  player.move(moving_left, moving_right) 

            if boss.music:
                play_boss_music(Musica_main, Musica_boss)
                if not update_camera:
                    tela_scroll -= 600
                    player.rect.x -= 400
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
                        play_boss_music(Musica_boss, Musica_main)
                        tela_scroll -= 500
                        player.rect.x -= 400
                        update_camera_2 = True
                    


                
            if inv_wall.colliderect(player.rect) and tela_scroll < 0:
                tela_scroll = 0  
            if Inv_wall_init.colliderect(player.rect) and tela_scroll > 0:
                tela_scroll = 0  





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
            inv_wall.x += tela_scroll
            Inv_wall_init.x += tela_scroll
        
        elif player.vivo == False:
            player.update_action(3)
            tela.blit(game_over_img, (0, 0))

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
                elif event.key == pygame.K_SPACE and (player.vivo == False or player.com_keycard):
                    running = False
                    Musica_main.stop()
                    Musica_boss.stop()
                    boss.kill()
                    for inimigo in inimigo_group:
                        inimigo.kill()
                    global Musica_played
                    global Menu_play
                    Musica_played = False
                    Menu_play = False
                    return intro(False)

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

intro()