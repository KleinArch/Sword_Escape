import random
import maps
import config
from save import writeFile, pocaoLista
from PPlay.sprite import Sprite
from PPlay.sound import Sound

# --- Sprites Principais e de Cenário ---
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

    return poc_lista


def celulas_livres(m):
    livres = []
    for linha_idx, linha in enumerate(m):
        for col_idx, tile in enumerate(linha):
            if tile == 0:
                livres.append((linha_idx, col_idx))
    return livres


def criar_inimigo(linha_idx, col_idx, tipo="base", num_fase=1):
    # Carrega dinamicamente os sprites dependendo do tipo e do número da fase/sufixo
    if tipo == "elite":
        inimigo = Sprite(f"PNG/IniElite_{num_fase}.png")
        inimigo.vida = 2                         # Inimigos de Elite possuem mais vida
        inimigo.vel = 65                         # São ligeiramente mais rápidos
        inimigo.eh_elite = True
    else:
        inimigo = Sprite(f"PNG/IniBase_{num_fase}.png")
        inimigo.vida = 1
        inimigo.vel = 45
        inimigo.eh_elite = False

    inimigo.x = col_idx * config.TAMANHO_TILE
    inimigo.y = linha_idx * config.TAMANHO_TILE
    inimigo.eh_chefe = False
    return inimigo


def criar_chefe(m, numero_sala):
    if numero_sala == 1:
        chefe_sprite = "PNG/Boss_1.png"
        vida_chefe = 3
    elif numero_sala == 2:
        chefe_sprite = "PNG/Boss_2.png"
        vida_chefe = 4
    else:
        chefe_sprite = "PNG/Boss_3.png"
        vida_chefe = 5

    chefe = Sprite(chefe_sprite)
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

    # Determinação do sufixo do sprite conforme a fase atual:
    # 1ª fase (sala_atual == 0) não gera inimigos comuns pois inicia liberada
    # 2ª fase (sala_atual == 1) -> num_fase = 1 (_1)
    # 3ª fase (sala_atual == 2) -> num_fase = 2 (_2)
    # Última fase (sala_atual == fim) -> num_fase = 3 (_3)
    if sala_atual == len(maps.mapas) - 1:
        num_fase = 3
    elif sala_atual == 2:
        num_fase = 2
    else:
        num_fase = 1

    inimigos_gerados = []
    for l, c in escolhidas:
        # Define aleatoriamente (ex: 30% de chance) se o inimigo criado será Base ou Elite
        tipo = "elite" if random.random() < 0.3 else "base"
        inimigos_gerados.append(criar_inimigo(l, c, tipo, num_fase))
    return inimigos_gerados


# --- Projéteis ---
PROJETIL_VELOCIDADE = 250
PROJETIL_TAMANHO = 16
INTERVALO_TIRO = 2.0

projeteis = []


def criar_projetil(x, y, dir_x, dir_y):
    proj = Sprite("PNG/fireball.png")
    proj.width = PROJETIL_TAMANHO
    proj.height = PROJETIL_TAMANHO
    proj.x = x
    proj.y = y
    proj.vel_x = dir_x * PROJETIL_VELOCIDADE
    proj.vel_y = dir_y * PROJETIL_VELOCIDADE
    return proj


def atualizar_chefe(chefe, delta, mapa_atual):
    cx = personagem.x + personagem.width / 2
    cy = personagem.y + personagem.height / 2
    bx = chefe.x + chefe.width / 2
    by = chefe.y + chefe.height / 2

    dx = cx - bx
    dy = cy - by
    dist = max((dx**2 + dy**2) ** 0.5, 1)

    vel_chefe = 80

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

    # Limites da janela
    chefe.x = max(config.TAMANHO_TILE, min(chefe.x, config.janela.width - chefe.width - config.TAMANHO_TILE))
    chefe.y = max(config.TAMANHO_TILE, min(chefe.y, config.janela.height - chefe.height - config.TAMANHO_TILE))


def atualizar_inimigos_comuns(inimigos_lista, delta, mapa_atual):
    """Faz com que os inimigos comuns persigam o jogador respeitando as colisões com paredes."""
    for inimigo in inimigos_lista:
        if inimigo.eh_chefe:
            continue

        cx = personagem.x + personagem.width / 2
        cy = personagem.y + personagem.height / 2
        ix = inimigo.x + inimigo.width / 2
        iy = inimigo.y + inimigo.height / 2

        dx = cx - ix
        dy = cy - iy
        dist = max((dx**2 + dy**2) ** 0.5, 1)

        # Movimento e colisão no Eixo X
        antigo_x = inimigo.x
        inimigo.x += (dx / dist) * inimigo.vel * delta
        for linha_idx, linha in enumerate(mapa_atual):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if inimigo.collided(floor):
                        inimigo.x = antigo_x

        # Movimento e colisão no Eixo Y
        antigo_y = inimigo.y
        inimigo.y += (dy / dist) * inimigo.vel * delta
        for linha_idx, linha in enumerate(mapa_atual):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if inimigo.collided(floor):
                        inimigo.y = antigo_y


def atualizar_projeteis(delta, mapa_atual):
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

        if proj.x <= MIN_X or proj.x >= MAX_X:
            proj.vel_x *= -1
            proj.x = max(MIN_X, min(proj.x, MAX_X))
        
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

        if proj.y <= MIN_Y or proj.y >= MAX_Y:
            proj.vel_y *= -1
            proj.y = max(MIN_Y, min(proj.y, MAX_Y))

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

        if proj.collided(personagem):
            acertou_jogador = True
        else:
            ativos.append(proj)

    projeteis = ativos
    return acertou_jogador


# --- Variáveis de Estado do Jogo ---
sala_atual = 0
mapa = maps.mapas[sala_atual]

estado_salas = ["lutando" for _ in maps.mapas]
estado_salas[0] = "liberada"  # Define que a primeira sala inicia livre de batalhas normais

jogo_vencido = False
jogador_morto = False
vida_jogador = 10
player_inv_timer = 0.0

direcao = "right"
ataque_ativo = False
ataque_timer = 0
recarga_timer = 0
RECARGA_DURACAO = 0.5
tiro_timer = 0

musica_fundo = None


def abrir_porta_da_sala(idx):
    porta = maps.PORTAS_SAIDA[idx]
    if porta is not None:
        l, c = porta
        maps.mapas[idx][l][c] = 2


abrir_porta_da_sala(0)

if estado_salas[sala_atual] == "lutando":
    inimigos = gerar_inimigos_para_sala(mapa)
else:
    inimigos = []


def trocar_sala(novo_index, entrar_pela_esquerda):
    global sala_atual, mapa, inimigos, ataque_ativo

    sala_atual = novo_index
    mapa = maps.mapas[sala_atual]
    ataque_ativo = False

    if estado_salas[sala_atual] == "lutando":
        inimigos = gerar_inimigos_para_sala(mapa)
    else:
        inimigos = []

    if entrar_pela_esquerda:
        personagem.x = config.TAMANHO_TILE * 1.2
    else:
        personagem.x = config.janela.width - config.TAMANHO_TILE * 2.2

    personagem.y = max(0, min(personagem.y, config.janela.height - personagem.height))


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

    espada.x = max(0, min(espada.x, config.janela.width - ESPADA_W))
    espada.y = max(0, min(espada.y, config.janela.height - ESPADA_H))


def jogar():
    global direcao, ataque_ativo, ataque_timer, recarga_timer, tiro_timer
    global jogador_morto, jogo_vencido, inimigos, mapa, musica_fundo
    global sala_atual, estado_salas, projeteis, vida_jogador, player_inv_timer

    sala_atual = 0
    mapa = maps.mapas[sala_atual]
    estado_salas[:] = ["lutando" for _ in maps.mapas]
    estado_salas[0] = "liberada"

    for idx, porta in enumerate(maps.PORTAS_SAIDA):
        if porta is not None:
            l, c = porta
            maps.mapas[idx][l][c] = 1
    abrir_porta_da_sala(0)

    if estado_salas[sala_atual] == "lutando":
        inimigos = gerar_inimigos_para_sala(mapa)
    else:
        inimigos = []
    projeteis.clear()

    personagem.x = config.janela.width / 2 - personagem.width / 2
    personagem.y = config.janela.height / 2 - personagem.height / 2

    direcao = "right"
    ataque_ativo = False
    ataque_timer = 0
    recarga_timer = 0
    tiro_timer = 0
    jogador_morto = False
    jogo_vencido = False
    vida_jogador = 5
    player_inv_timer = 0.0

    musica_fundo = Sound("AUDIO/fase_01.mp3")
    musica_fundo.play()

    while True:
        delta = config.janela.delta_time()

        if config.janela.keyboard.key_pressed("esc"):
            musica_fundo.stop()
            break

        if jogo_vencido:
            config.janela.set_background_color((10, 60, 10))
            config.janela.draw_text("VOCE VENCEU O JOGO!", 280, 270, size=36, color=(255, 255, 0))
            config.janela.draw_text("Pressione ESC para sair", 400, 320, size=18, color=(255, 255, 255))
            config.janela.update()
            continue

        if jogador_morto:
            config.janela.set_background_color((60, 10, 10))
            config.janela.draw_text("VOCE MORREU!", 330, 270, size=36, color=(255, 60, 60))
            config.janela.draw_text("Pressione ESC para sair", 400, 320, size=18, color=(255, 255, 255))
            config.janela.update()
            continue

        if player_inv_timer > 0:
            player_inv_timer -= delta

        # --- Movimento Eixo X ---
        antigo_x = personagem.x
        if config.janela.keyboard.key_pressed("left"):
            personagem.x -= config.VELOCIDADE * delta
            direcao = "left"
        if config.janela.keyboard.key_pressed("right"):
            personagem.x += config.VELOCIDADE * delta
            direcao = "right"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if personagem.collided(floor):
                        personagem.x = antigo_x

        # --- Movimento Eixo Y ---
        antigo_y = personagem.y
        if config.janela.keyboard.key_pressed("up"):
            personagem.y -= config.VELOCIDADE * delta
            direcao = "up"
        if config.janela.keyboard.key_pressed("down"):
            personagem.y += config.VELOCIDADE * delta
            direcao = "down"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    if personagem.collided(floor):
                        personagem.y = antigo_y

        personagem.x = max(0, min(personagem.x, config.janela.width - personagem.width))
        personagem.y = max(0, min(personagem.y, config.janela.height - personagem.height))

        # --- Portas e Troca de Sala ---
        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 2 and sala_atual + 1 < len(maps.mapas):
                    porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    if personagem.collided(porta_sprite):
                        trocar_sala(sala_atual + 1, entrar_pela_esquerda=True)
                elif tile == 3 and sala_atual - 1 >= 0:
                    porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    if personagem.collided(porta_sprite):
                        trocar_sala(sala_atual - 1, entrar_pela_esquerda=False)

        # --- Movimento de Inimigos Normais/Elites ---
        if estado_salas[sala_atual] == "lutando":
            atualizar_inimigos_comuns(inimigos, delta, mapa)

        # --- Sistema de Ataque ---
        if recarga_timer > 0:
            recarga_timer -= delta

        if config.janela.keyboard.key_pressed("space") and not ataque_ativo and recarga_timer <= 0:
            ataque_ativo = True
            ataque_timer = config.ATAQUE_DURACAO
            recarga_timer = RECARGA_DURACAO
            posicionar_espada()

        if ataque_ativo:
            ataque_timer -= delta
            posicionar_espada()

            inimigos_vivos = []
            for inimigo in inimigos:
                if espada.collided(inimigo):
                    if not hasattr(inimigo, 'inv_timer') or inimigo.inv_timer <= 0:
                        inimigo.vida -= 1
                        inimigo.inv_timer = 1.0
                    if inimigo.vida > 0:
                        inimigos_vivos.append(inimigo)
                else:
                    inimigos_vivos.append(inimigo)
            inimigos[:] = inimigos_vivos

            if ataque_timer <= 0:
                ataque_ativo = False

        for inimigo in inimigos:
            if hasattr(inimigo, 'inv_timer') and inimigo.inv_timer > 0:
                inimigo.inv_timer -= delta

        # --- Estados das Salas e Derrota de Boss ---
        if estado_salas[sala_atual] == "lutando" and len(inimigos) == 0:
            estado_salas[sala_atual] = "chefe"
            inimigos = [criar_chefe(mapa, sala_atual)]
            tiro_timer = INTERVALO_TIRO
            projeteis.clear()

        elif estado_salas[sala_atual] == "chefe" and len(inimigos) == 0:
            projeteis.clear()
            estado_salas[sala_atual] = "liberada"

            if sala_atual == 1:
                writeFile("poc_veloc")
                musica_fundo.stop()
                musica_fundo = Sound("AUDIO/fase_02.mp3")
                musica_fundo.play()

            if sala_atual == 2:
                writeFile("poc_cura")
                musica_fundo.stop()
                musica_fundo = Sound("AUDIO/fase_03.mp3")
                musica_fundo.play()

            if sala_atual == 3:
                writeFile("poc_forca")

            if sala_atual == len(maps.mapas) - 1:
                jogo_vencido = True
            else:
                abrir_porta_da_sala(sala_atual)

        if estado_salas[sala_atual] == "chefe" and inimigos:
            chefe = inimigos[0]
            atualizar_chefe(chefe, delta, mapa)

            tiro_timer -= delta
            if tiro_timer <= 0:
                tiro_timer = INTERVALO_TIRO
                dx = personagem.x - chefe.x
                dy = personagem.y - chefe.y
                dist = max((dx**2 + dy**2) ** 0.5, 1)
                projeteis.append(criar_projetil(
                    chefe.x + chefe.width / 2,
                    chefe.y + chefe.height / 2,
                    dx / dist,
                    dy / dist
                ))

        # --- Detecção de Dano (Projéteis + Contato Direto com Inimigos comuns) ---
        dano_recebido = atualizar_projeteis(delta, mapa)

        if estado_salas[sala_atual] == "lutando":
            for inimigo in inimigos:
                if inimigo.collided(personagem):
                    dano_recebido = True
                    break

        if dano_recebido:
            if player_inv_timer <= 0:
                vida_jogador -= 1
                player_inv_timer = 0.8
                if vida_jogador <= 0:
                    jogador_morto = True

        # --- Renderização ---
        config.janela.set_background_color((40, 40, 40))

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    floor.x = coluna_idx * config.TAMANHO_TILE
                    floor.y = linha_idx * config.TAMANHO_TILE
                    floor.draw()
                elif tile in (2, 3):
                    porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    porta_sprite.draw()

        for inimigo in inimigos:
            inimigo.draw()

        personagem.draw()

        if ataque_ativo:
            if (espada.x >= 0 and espada.y >= 0 and
                espada.x + ESPADA_W <= config.janela.width and
                espada.y + ESPADA_H <= config.janela.height):
                espada.draw()

        for proj in projeteis:
            proj.draw()

        # --- HUD ---
        if estado_salas[sala_atual] == "lutando":
            config.janela.draw_text(f"Inimigos restantes: {len(inimigos)}", 10, 10, size=16, color=(255, 255, 255))
        elif estado_salas[sala_atual] == "chefe":
            vida_chefe = inimigos[0].vida if inimigos else 0
            config.janela.draw_text(f"CHEFE - vida: {vida_chefe}", 10, 10, size=16, color=(255, 60, 60))
        else:
            config.janela.draw_text("Sala liberada!", 10, 10, size=16, color=(120, 255, 120))

        config.janela.draw_text(f"Sua Vida: {vida_jogador}", 10, 35, size=16, color=(0, 255, 0))

        config.janela.update()
