import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, velocidade, escala, gravidade):
        pygame.sprite.Sprite.__init__(self)
        self.gravidade = gravidade
        self.vivo = True
        self.char_type = char_type
        self.velocidade = velocidade
        self.velocidade_y = 0
        self.dirececao = 1
        self.jump = False
        self.no_ar = True
        self.flip = False
        self.lista_animacoes = []
        self.frame_index = 0
        # 0 = Idle | 1 = Run | 2 = Jump
        self.action = 0
        self.update_tempo = pygame.time.get_ticks()

        animacao_types = ['Idle', 'Run', 'Jump']
        for animacao in animacao_types:
            # reset da lista temporária de imagens
            temp_list = []
            # contar o número de arquivos na pasta
            num_frames = len(os.listdir(f'imagens\Sprites\{self.char_type}\{animacao}'))
            for i in range(num_frames):
                img_player = pygame.image.load(f'imagens\Sprites\{self.char_type}\{animacao}\{self.char_type}{i}.png')
                img_player = pygame.transform.scale(img_player, (img_player.get_width() / 4, img_player.get_height() / 4))
                temp_list.append(img_player)
            self.lista_animacoes.append(temp_list)
        self.img_player = self.lista_animacoes[self.action][self.frame_index]
        self.player_rect = self.img_player.get_rect()
        self.player_rect.center = (x, y)
        
    def move(self, mooving_left, mooving_right):
        # reset as variáveis de movimento
        dx = 0
        dy = 0
        # checando se o player se move para a direita ou esquerda
        if mooving_left:
            dx = -self.velocidade
            self.flip = True
            self.dirececao = -1
        if mooving_right:
            dx = +self.velocidade
            self.flip = False
            self.dirececao = 1
        # Pulo
        if self.jump == True and self.no_ar == False:
            self.velocidade_y = -15 # altura do pulo
            self.jump = False
            self.no_ar = True
        self.velocidade_y += self.gravidade
        # ação da gravidade
        if self.velocidade_y > 10: # velocidade máxima
            self.velocidade_y
        dy += self.velocidade_y
        # checando colisão com o chão
        if self.player_rect.bottom + dy > 700:
            dy = 700 - self.player_rect.bottom
            self.no_ar = False
        # updade da posição do player_rect
        self.player_rect.x += dx
        self.player_rect.y += dy

    def update_animacao(self):
        # tempo de update da animação
        cooldown_animacao = 700
        # update da imagem dependendo do frame
        self.img_player = self.lista_animacoes[self.action][self.frame_index]
        # check se passou tempo suficiente desde o último update
        if pygame.time.get_ticks() - self.update_tempo > cooldown_animacao:
            self.update_tempo = pygame.time.get_ticks()
            self.frame_index += 1
        # se a animação chegar no final ela reinicia
        if self.frame_index >= len(self.lista_animacoes[self.action]):
            self.frame_index = 0
    
    def update_action(self, nova_acao):
        # checa se a nova ação é deferente da ação anterior
        if nova_acao != self.action:
            self.action = nova_acao
            # updade das configs da animação, para trocar para o começo da próxima animação
            self.frame_index = 0
            self.update_tempo = pygame.time.get_ticks()

    def draw(self, tela):
        tela.blit(pygame.transform.flip(self.img_player, self.flip, False), self.player_rect)
    
