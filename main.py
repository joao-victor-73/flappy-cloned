# IMPORTAÇÃO DE BIBLIOTECAS
import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

# Instânciando as imagens do jogo
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imagens', 'pine.png')))
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
        
        self.imagem = IMGS[0]

class Cano:
    pass

class Chao:
    pass