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

porta_sprite = Sprite("PNG/preto.png")  # troque por sprite de porta se tiver
porta_sprite.width = 50
porta_sprite.height = 50

personagem.x = janela.width / 2 - personagem.width / 2
personagem.y = janela.height / 2 - personagem.height / 2

VELOCIDADE = 200
TAMANHO_TILE = 50

direcao = "right"

espada = Sprite("PNG/kkkkkkkkkkk-1.png.png")
ESPADA_W = espada.width
ESPADA_H = espada.height

ataque_ativo = False
ataque_timer = 0
ATAQUE_DURACAO = 0.15

# 0 = livre | 1 = parede | 2 = porta para próxima sala (some quando liberada)
# 3 = porta para sala anterior (sempre passável)
# A posição da porta "2" também é guardada separadamente em PORTAS_SAIDA[],
# porque ela começa BLOQUEADA (tratada como parede) até o chefe morrer.

mapa1 = [
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

mapa2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1],
    [1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1],
    [1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

mapa3 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1],
    [1,0,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
    [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1],
    [3,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1],
    [1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

mapas = [mapa1, mapa2, mapa3]

# Posição da porta de saída de cada sala (linha, coluna).
# Ela começa como PAREDE (1) no mapa e só vira passagem (2) quando o chefe morre.
PORTAS_SAIDA = [
    (6, 19),  # mapa1 -> sala 1
    (6, 19),  # mapa2 -> sala 2
    None,     # mapa3 não tem porta de saída (é a sala final)
]

for idx, porta in enumerate(PORTAS_SAIDA):
    if porta is not None:
        l, c = porta
        mapas[idx][l][c] = 1  # garante que começa bloqueada

sala_atual = 0
mapa = mapas[sala_atual]

# Estado de cada sala: "lutando" -> "chefe" -> "liberada"
estado_salas = ["lutando" for _ in mapas]

jogo_vencido = False


def celulas_livres(m):
    livres = []
    for linha_idx, linha in enumerate(m):
        for col_idx, tile in enumerate(linha):
            if tile == 0:
                livres.append((linha_idx, col_idx))
    return livres


def criar_inimigo(linha_idx, col_idx):
    inimigo = Sprite("PNG/personagem-1.png.png")  # troque pelo sprite do inimigo comum
    inimigo.x = col_idx * TAMANHO_TILE
    inimigo.y = linha_idx * TAMANHO_TILE
    inimigo.vida = 1
    inimigo.eh_chefe = False
    return inimigo


def criar_chefe(m):
    chefe = Sprite("PNG/Boss_1.png")  # idealmente troque por um sprite próprio do chefe
    livres = celulas_livres(m)
    centro = livres[len(livres) // 2]
    chefe.x = centro[1] * TAMANHO_TILE
    chefe.y = centro[0] * TAMANHO_TILE
    chefe.vida = 3
    chefe.eh_chefe = True
    return chefe


def gerar_inimigos_para_sala(m, quantidade=3):
    livres = celulas_livres(m)
    qtd = min(quantidade, len(livres))
    escolhidas = random.sample(livres, qtd)
    return [criar_inimigo(l, c) for l, c in escolhidas]


inimigos = gerar_inimigos_para_sala(mapa)


def trocar_sala(novo_index, entrar_pela_esquerda):
    """Troca a sala atual, reposiciona o personagem e prepara os inimigos."""
    global sala_atual, mapa, inimigos, ataque_ativo

    sala_atual = novo_index
    mapa = mapas[sala_atual]
    ataque_ativo = False

    if estado_salas[sala_atual] == "lutando":
        inimigos = gerar_inimigos_para_sala(mapa)
    else:
        inimigos = []

    if entrar_pela_esquerda:
        personagem.x = TAMANHO_TILE * 1.2
    else:
        personagem.x = janela.width - TAMANHO_TILE * 2.2

    personagem.y = max(0, min(personagem.y, janela.height - personagem.height))


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


def abrir_porta_da_sala(idx):
    """Transforma a parede bloqueada da porta em passagem livre."""
    porta = PORTAS_SAIDA[idx]
    if porta is not None:
        l, c = porta
        mapas[idx][l][c] = 2  # passa a ser porta passável


def jogar():
    global direcao, ataque_ativo, ataque_timer, jogo_vencido, inimigos

    while True:
        delta = janela.delta_time()

        if janela.keyboard.key_pressed("esc"):
            break

        if jogo_vencido:
            janela.set_background_color((10, 60, 10))
            janela.draw_text("VOCE VENCEU O JOGO!", 280, 270, size=36, color=(255, 255, 0))
            janela.draw_text("Pressione ESC para sair", 400, 320, size=18, color=(255, 255, 255))
            janela.update()
            continue

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

        # --- Verifica portas (troca de sala) ---
        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 2 and sala_atual + 1 < len(mapas):
                    porta_sprite.x = coluna_idx * TAMANHO_TILE
                    porta_sprite.y = linha_idx * TAMANHO_TILE
                    if personagem.collided(porta_sprite):
                        trocar_sala(sala_atual + 1, entrar_pela_esquerda=True)
                elif tile == 3 and sala_atual - 1 >= 0:
                    porta_sprite.x = coluna_idx * TAMANHO_TILE
                    porta_sprite.y = linha_idx * TAMANHO_TILE
                    if personagem.collided(porta_sprite):
                        trocar_sala(sala_atual - 1, entrar_pela_esquerda=False)

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
                    inimigo.vida -= 1
                    if inimigo.vida > 0:
                        inimigos_vivos.append(inimigo)
                else:
                    inimigos_vivos.append(inimigo)
            inimigos[:] = inimigos_vivos

            if ataque_timer <= 0:
                ataque_ativo = False

        # --- Transições de estado da sala (inimigos -> chefe -> porta) ---
        if estado_salas[sala_atual] == "lutando" and len(inimigos) == 0:
            estado_salas[sala_atual] = "chefe"
            inimigos = [criar_chefe(mapa)]

        elif estado_salas[sala_atual] == "chefe" and len(inimigos) == 0:
            estado_salas[sala_atual] = "liberada"
            if sala_atual == len(mapas) - 1:
                jogo_vencido = True
            else:
                abrir_porta_da_sala(sala_atual)

        # --- REFRESH ---
        janela.set_background_color((40, 40, 40))

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * TAMANHO_TILE
                    floor.y = linha_idx * TAMANHO_TILE
                    floor.draw()
                elif tile in (2, 3):
                    porta_sprite.x = coluna_idx * TAMANHO_TILE
                    porta_sprite.y = linha_idx * TAMANHO_TILE
                    porta_sprite.draw()

        for inimigo in inimigos:
            inimigo.draw()

        personagem.draw()

        if ataque_ativo:
            if (espada.x >= 0 and espada.y >= 0 and
                espada.x + espada.width <= janela.width and
                espada.y + espada.height <= janela.height):
                espada.draw()

        # --- HUD simples de status da sala ---
        if estado_salas[sala_atual] == "lutando":
            janela.draw_text(f"Inimigos restantes: {len(inimigos)}", 10, 10, size=16, color=(255, 255, 255))
        elif estado_salas[sala_atual] == "chefe":
            vida_chefe = inimigos[0].vida if inimigos else 0
            janela.draw_text(f"CHEFE - vida: {vida_chefe}", 10, 10, size=16, color=(255, 60, 60))
        else:
            janela.draw_text("Sala liberada!", 10, 10, size=16, color=(120, 255, 120))

        janela.update()


jogar()