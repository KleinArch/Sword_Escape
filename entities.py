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

    return poc_lista  # CORRIGIDO: faltava este return


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
        chefe_sprite = "PNG/Boss_1.png"
        vida_chefe = 3
    elif numero_sala == 2:
        chefe_sprite = "PNG/Boss_2.png"
        vida_chefe = 4                   # Boss 2 um pouco mais forte
    else:
        chefe_sprite = "PNG/Boss_3.png"
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


# --- Projéteis ---
PROJETIL_VELOCIDADE = 250
PROJETIL_TAMANHO = 16
INTERVALO_TIRO = 2.0  # segundos entre cada tiro do chefe

projeteis = []  # lista global de projéteis ativos


def criar_projetil(x, y, dir_x, dir_y):
    """Cria uma bola de fogo na posição do chefe com direção normalizada (dir_x, dir_y)."""
    proj = Sprite("PNG/fireball.png")
    proj.width = PROJETIL_TAMANHO
    proj.height = PROJETIL_TAMANHO
    proj.x = x
    proj.y = y
    proj.vel_x = dir_x * PROJETIL_VELOCIDADE
    proj.vel_y = dir_y * PROJETIL_VELOCIDADE
    return proj
def atualizar_chefe(chefe, delta, mapa_atual):
    """Move o chefe em direção ao jogador respeitando as paredes."""
    cx = personagem.x + personagem.width / 2
    cy = personagem.y + personagem.height / 2
    bx = chefe.x + chefe.width / 2
    by = chefe.y + chefe.height / 2

    dx = cx - bx
    dy = cy - by
    dist = max((dx**2 + dy**2) ** 0.5, 1)

    vel_chefe = 80  # pixels por segundo

    # Movimento e colisão no Eixo X
    antigo_x = chefe.x
    chefe.x += (dx / dist) * vel_chefe * delta
    for linha_idx, linha in enumerate(mapa_atual):
        for coluna_idx, tile in enumerate(linha):
            if tile == 1:
                floor.x = coluna_idx * config.TAMANHO_TILE
                floor.y = linha_idx * config.TAMANHO_TILE
                if chefe.collided(floor):
                    chefe.x = antigo_x

    # Movimento e colisão no Eixo Y
    antigo_y = chefe.y
    chefe.y += (dy / dist) * vel_chefe * delta
    for linha_idx, linha in enumerate(mapa_atual):
        for coluna_idx, tile in enumerate(linha):
            if tile == 1:
                floor.x = coluna_idx * config.TAMANHO_TILE
                floor.y = linha_idx * config.TAMANHO_TILE
                if chefe.collided(floor):
                    chefe.y = antigo_y

    # Mantém dentro dos limites da janela (respeitando as paredes externas)
    chefe.x = max(config.TAMANHO_TILE, min(chefe.x, config.janela.width - chefe.width - config.TAMANHO_TILE))
    chefe.y = max(config.TAMANHO_TILE, min(chefe.y, config.janela.height - chefe.height - config.TAMANHO_TILE))


def atualizar_projeteis(delta, mapa_atual):
    """Move os projéteis, faz ricochete nas paredes e detecta colisão com o jogador.
    Retorna True se algum projétil acertou o jogador."""
    global projeteis

    MIN_X = config.TAMANHO_TILE
    MAX_X = config.janela.width - config.TAMANHO_TILE - PROJETIL_TAMANHO
    MIN_Y = config.TAMANHO_TILE
    MAX_Y = config.janela.height - config.TAMANHO_TILE - PROJETIL_TAMANHO

    acertou_jogador = False
    ativos = []

    for proj in projeteis:
        # --- Eixo X ---
        antigo_x = proj.x
        proj.x += proj.vel_x * delta

        # Ricochete nas bordas externas X
        if proj.x <= MIN_X or proj.x >= MAX_X:
            proj.vel_x *= -1
            proj.x = max(MIN_X, min(proj.x, MAX_X))
        # Ricochete nas paredes internas X
        colidiu_x = False
        for linha_idx, linha in enumerate(mapa_atual):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if proj.collided(floor):
                        colidiu_x = True
                        break
            if colidiu_x:
                break
        if colidiu_x:
            proj.vel_x *= -1
            proj.x = antigo_x

        # --- Eixo Y ---
        antigo_y = proj.y
        proj.y += proj.vel_y * delta

        # Ricochete nas bordas externas Y
        if proj.y <= MIN_Y or proj.y >= MAX_Y:
            proj.vel_y *= -1
            proj.y = max(MIN_Y, min(proj.y, MAX_Y))

        # Ricochete nas paredes internas Y
        colidiu_y = False
        for linha_idx, linha in enumerate(mapa_atual):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if proj.collided(floor):
                        colidiu_y = True
                        break
            if colidiu_y:
                break
        if colidiu_y:
            proj.vel_y *= -1
            proj.y = antigo_y

        # Colisão com o jogador
        if proj.collided(personagem):
            acertou_jogador = True
        else:
            ativos.append(proj)

    projeteis = ativos
    return acertou_jogador
