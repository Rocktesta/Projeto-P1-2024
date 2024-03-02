class Botao():
    def __init__(self, imagem, pos, texto_input, fonte, cor_base, cor_hoover):
        # Propriedades do botao
        self.imagem = imagem
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.texto_input = texto_input
        self.fonte = fonte
        self.cor_base = cor_base
        self.cor_hoover = cor_hoover
        self.texto = self.fonte.render(self.texto_input, True, self.cor_base)
        if self.imagem is None:
            self.imagem = self.texto
        self.rect = self.imagem.get_rect(center = (self.x_pos, self.y_pos))
        self.texto_rect = self.texto.get_rect(center = (self.x_pos, self.y_pos))

    def update(self, tela, mouse_pos):
        # Muda a cor do botão quando passar o mouse por cima
        if self.rect.collidepoint(mouse_pos):
            cor_atual = self.cor_hoover
        else:
            cor_atual = self.cor_base

        # Renderiza o texto com a cor atual
        self.texto = self.fonte.render(self.texto_input, True, cor_atual)

        # Desenha o botão na tela
        tela.blit(self.texto, self.rect)

    def checarinput(self, posicao):
        # Checa se clicou ou não no botão
        if posicao[0] in range(self.rect.left, self.rect.right) and posicao[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False
    
    def mudarcor(self, posicao):
    # Muda a cor do botão quando passar o mouse por cima
        if posicao[0] in range(self.rect.left, self.rect.right) and posicao[1] in range(self.rect.top, self.rect.bottom):
            self.texto = self.fonte.render(self.texto_input, True, self.cor_hoover)
        else:
            self.texto = self.fonte.render(self.texto_input, True, self.cor_base)