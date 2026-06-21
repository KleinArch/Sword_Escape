import random
from PPlay.sprite import Sprite
import config
from save import *

# Instanciação dos Sprites Principais e de Cenário
personagem = Sprite("PNG/player.png")
personagem.x = config.janela.width / 2 - personagem.width / 2
personagem.y = config.janela.height / 2 - personagem.height / 2

floor = Sprite("PNG/Brickwall.png")
floor.width = config.TAMANHO_TILE
floor.height = config.TAMANHO_TILE

porta_sprite = Sprite("PNG/preto.png")
porta_sprite.width = config.TAMANHO_TILE
porta_sprite.height = config.TAMANHO_TILE

espada = Sprite("PNG/sword_player.png")
ESPADA_W = espada.width
ESPADA_H = espada.height

vec = pocaoLista()

def criar_lista_poc(vec):
    poc_lista = []

    if vec == []:
        return poc_lista

    if len(vec) == 1:
        poc_v = Sprite("PNG/poc_veloc.png")
        poc_lista.append(poc_v)

    elif len(vec) == 2:
        poc_cura = Sprite("PNG/poc_cura.png")
        poc_lista.append(poc_cura)

    elif len(vec) == 3:
        poc_forca = Sprite("PNG/poc_forca.png")
        poc_lista.append(poc_forca)

def celulas_livres(m):
    livres = []
    for linha_idx, linha in enumerate(m):
        for col_idx, tile in enumerate(linha):
            if tile == 0:
                livres.append((linha_idx, col_idx))
    return livres


def criar_inimigo(linha_idx, col_idx):
    inimigo = Sprite("PNG/IniBase_1.png")
    inimigo.x = col_idx * config.TAMANHO_TILE
    inimigo.y = linha_idx * config.TAMANHO_TILE
    inimigo.vida = 1
    inimigo.eh_chefe = False
    return inimigo

def criar_chefe(m, numero_sala):
    # Determina o arquivo do Boss com base na ordem das salas
    # Sala 1 -> boss_1 | Sala 2 -> boss_2 | Sala 3 -> boss_3
    if numero_sala == 1:
        chefe_sprite = "PNG/Boss_1.png"  # Substitua pelo nome correto do seu arquivo do boss_1
        vida_chefe = 3
    elif numero_sala == 2:
        chefe_sprite = "PNG/Boss_2.png"  # Substitua pelo nome correto do seu arquivo do boss_2
        vida_chefe = 4                   # Boss 2 um pouco mais forte
    else:
        chefe_sprite = "PNG/Boss_3.png"  # Substitua pelo nome correto do seu arquivo do boss_3
        vida_chefe = 5                   # Boss final com mais vida

    chefe = Sprite(chefe_sprite)
    # Posiciona no centro da sala
    livres = celulas_livres(m)
    centro = livres[len(livres) // 2]
    chefe.x = centro[1] * config.TAMANHO_TILE
    chefe.y = centro[0] * config.TAMANHO_TILE
    chefe.vida = vida_chefe
    chefe.eh_chefe = True
    return chefe

def gerar_inimigos_para_sala(m, quantidade=3):
    livres = celulas_livres(m)
    qtd = min(quantidade, len(livres))
    escolhidas = random.sample(livres, qtd)
    return [criar_inimigo(l, c) for l, c in escolhidas]
