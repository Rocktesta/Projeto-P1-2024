import pygame
import player_script_teste
pygame.init()

largura_tela = 1280
altura_tela = 720

tela = pygame.display.set_mode((largura_tela, altura_tela))

# framerate
clock = pygame.time.Clock()
fps = 60

BG = (152, 152, 152) 
def draw_bg():
    tela.fill(BG)
    pygame.draw.line(tela, (0, 0, 0), (0, 600), (largura_tela, 600))

def play():
    pygame.display.set_caption('PLAY')

    # Variáveis do jogo
    gravidade = 0.75

    # Movimentações do Player
    mooving_left = False
    mooving_right = False
    shoot = False

    player = player_script_teste.Boneco('player_Kiev', 200, 600, 3, gravidade, 3)

    # Loop Principal do Jogo
    running = True
    while running:
        
        clock.tick(fps)

        draw_bg()

        player.update()
        player.draw(tela)

        # updade e draw sprite groups
        bullet_group = player_script_teste.bullet_group
        bullet_group.update()
        bullet_group.draw(tela)

        # updade das ações do player
        
        if player.alive:
            # shoot bullets
            if shoot:
                player.shoot()
            '''if player.no_ar:
                player.updade_action(2) # animação de pulo
            elif mooving_left or mooving_right:
                player.update_action(1) # animação de corrida
            else:
                player.update_action(0) # retorna para o idle'''
            player.move(mooving_left, mooving_right) 

        for event in pygame.event.get():   # Loop para lidar com eventos
            if event.type == pygame.QUIT:
                running = False                 # jogo para de rodar se apertar o x da aba do jogo
            elif event.type == pygame.KEYDOWN:   # Se houver evento de pressionar tecla
                if event.key == pygame.K_ESCAPE:   # Se for tecla escape, jogo para de rodar
                    running = False 
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

play()
