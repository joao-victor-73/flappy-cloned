# IMPORTAÇÃO DE BIBLIOTECAS
import pygame
import os
import random


"""
No Pygame: 
- Para a direita: X +
- Para a esquerda: X -
- Para cima: Y -
- Para baixo: Y +
"""


TELA_LARGURA = 500
TELA_ALTURA = 800

# Instânciando as imagens do jogo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


# CRIANDO OS OBJETOS QUE SERVIRÃO PARA O JOGO

class Passaro:
    IMGS = IMAGENS_PASSARO

    # Animações da rotação do passaro
    ROTACAO_MAXIMA = 25 
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    # Atributos do passaro ( ou seja, as informações do passaro)
    def __init__(self, x_inicial, y_inicial):
        self.x = x_inicial
        self.y = y_inicial

        self.angulo = 0
        self.velocidade = 0 # Essa velocidade é a que ele se movimenta para cima e para baixo
        self.altura = self.y

        # Parâmetros auxiliares
        self.tempo = 0
        self.contagem_imagem = 0 # servirá para saber qual a imagem do passaro (bird1, bird2 ou bird3)
        
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover_passaro(self):
        # Calcular o deslocamento
        self.tempo += 1

        # formula do SORVETÃO do ensino médio para calcular o deslocamento
        # S = so + vot + at^2/2
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo


        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento


        # O angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar_passaro(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[2]

        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]

        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]

        # Se o passaro tiver caindo, eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    # Essa distância é entre o cano de cima e o de baixo
    # E esse valor de 200 é em px
    DISTANCIA = 200 
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO

        self.passou = False

        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA


    def mover_cano(self):
        self.x -= self.VELOCIDADE

    
    def desenhar_cano(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE_CHAO = 5
    LARGURA_CHAO = IMAGEM_CHAO.get_width()
    IMG_CHAO = IMAGEM_CHAO

    def __init__ (self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA_CHAO 
        # x0 = é o chão 1 / x1 = é o chão 2

    def mover_chao(self):
        self.x0 -= self.VELOCIDADE_CHAO
        self.x1 -= self.VELOCIDADE_CHAO

        if self.x0 + self.LARGURA_CHAO < 0:
            self.x0 = self.x0 + self.LARGURA_CHAO
        
        if self.x1 + self.LARGURA_CHAO < 0:
            self.x1 = self.x1 + self.LARGURA_CHAO

    def desenhar_chao(self, tela):
        tela.blit(self.IMG_CHAO, (self.x0, self.y))
        tela.blit(self.IMG_CHAO, (self.x1, self.y))


# PROGRAMA PRINCIPAL
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    
    for passaro in passaros:
        passaro.desenhar_passaro(tela)

    for cano in canos:
        cano.desenhar_cano(tela)

    texto = FONTE_PONTOS.render(f"PONTUAÇÃO: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    chao.desenhar_chao(tela)

    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.constants.QUIT:
                pygame.quit()
                quit()
                break

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()


        for passaro in passaros:
            passaro.mover_passaro()
        chao.mover_chao()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                
                if not cano.passou and passaro.x > cano.x:
                    cano.passou  = True
                    adicionar_cano = True
            
            cano.mover_cano()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()