from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
import random

janela = Window(1000, 600)
janela.set_title("Jogo com Mapa")

personagem = Sprite("PNG/personagem-1.png.png")
floor = Sprite("PNG/Brickwall5_Texture.png")
floor.width = 50
floor.height = 50

personagem.x = janela.width / 2 - personagem.width / 2
personagem.y = janela.height / 2 - personagem.height / 2

VELOCIDADE = 200
TAMANHO_TILE = 50

direcao = "right"

espada = Sprite("PNG/kkkkkkkkkkk-1.png.png")
ESPADA_W = espada.width   # guarda o tamanho real
ESPADA_H = espada.height

ataque_ativo = False
ataque_timer = 0
ATAQUE_DURACAO = 0.15

mapa = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def celulas_livres():
    livres = []
    for linha_idx, linha in enumerate(mapa):
        for col_idx, tile in enumerate(linha):
            if tile == 0:
                livres.append((linha_idx, col_idx))
    return livres

def criar_inimigo(linha_idx, col_idx):
    inimigo = Sprite("PNG/personagem-1.png.png")  # troque pelo sprite do inimigo
    inimigo.x = col_idx * TAMANHO_TILE
    inimigo.y = linha_idx * TAMANHO_TILE
    return inimigo

posicoes_possiveis = celulas_livres()
posicoes_escolhidas = random.sample(posicoes_possiveis, 3)
inimigos = [criar_inimigo(l, c) for l, c in posicoes_escolhidas]

def posicionar_espada():
    cx = personagem.x + personagem.width / 2
    cy = personagem.y + personagem.height / 2

    if direcao == "right":
        espada.x = personagem.x + personagem.width
        espada.y = cy - ESPADA_H / 2
    elif direcao == "left":
        espada.x = personagem.x - ESPADA_W
        espada.y = cy - ESPADA_H / 2
    elif direcao == "down":
        espada.x = cx - ESPADA_W / 2
        espada.y = personagem.y + personagem.height
    elif direcao == "up":
        espada.x = cx - ESPADA_W / 2
        espada.y = personagem.y - ESPADA_H

    espada.x = max(0, min(espada.x, janela.width - ESPADA_W))
    espada.y = max(0, min(espada.y, janela.height - ESPADA_H))

def jogar():
    global direcao, ataque_ativo, ataque_timer

    while True:
        delta = janela.delta_time()

        if janela.keyboard.key_pressed("esc"):
            break

        # --- Direção e movimento eixo X ---
        antigo_x = personagem.x
        if janela.keyboard.key_pressed("left"):
            personagem.x -= VELOCIDADE * delta
            direcao = "left"
        if janela.keyboard.key_pressed("right"):
            personagem.x += VELOCIDADE * delta
            direcao = "right"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * TAMANHO_TILE
                    floor.y = linha_idx * TAMANHO_TILE
                    if personagem.collided(floor):
                        personagem.x = antigo_x

        # --- Direção e movimento eixo Y ---
        antigo_y = personagem.y
        if janela.keyboard.key_pressed("up"):
            personagem.y -= VELOCIDADE * delta
            direcao = "up"
        if janela.keyboard.key_pressed("down"):
            personagem.y += VELOCIDADE * delta
            direcao = "down"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * TAMANHO_TILE
                    floor.y = linha_idx * TAMANHO_TILE
                    if personagem.collided(floor):
                        personagem.y = antigo_y

        personagem.x = max(0, min(personagem.x, janela.width - personagem.width))
        personagem.y = max(0, min(personagem.y, janela.height - personagem.height))

        # --- Ataque com espada ---
        if janela.keyboard.key_pressed("space") and not ataque_ativo:
            ataque_ativo = True
            ataque_timer = ATAQUE_DURACAO
            posicionar_espada()

        if ataque_ativo:
            ataque_timer -= delta
            posicionar_espada()

            inimigos_vivos = []
            for inimigo in inimigos:
                if espada.collided(inimigo):
                    pass  # inimigo atingido: descartado
                else:
                    inimigos_vivos.append(inimigo)
            inimigos[:] = inimigos_vivos

            if ataque_timer <= 0:
                ataque_ativo = False

        # --- REFRESH ---
        janela.set_background_color((40, 40, 40))

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * TAMANHO_TILE
                    floor.y = linha_idx * TAMANHO_TILE
                    floor.draw()

        for inimigo in inimigos:
            inimigo.draw()

        personagem.draw()

        if ataque_ativo:
            if (espada.x >= 0 and espada.y >= 0 and
                espada.x + espada.width <= janela.width and
                espada.y + espada.height <= janela.height):
                espada.draw()

        janela.update()

jogar()