import config
import maps
import entities
from save import writeFile
from PPlay.sound import Sound  # Importa a classe de som do PPlay

# --- Variáveis de Estado do Jogo ---
sala_atual = 0
mapa = maps.mapas[sala_atual]

estado_salas = ["lutando" for _ in maps.mapas]
estado_salas[0] = "liberada"

jogo_vencido = False
direcao = "right"
ataque_ativo = False
ataque_timer = 0

# Variável global para controlar a música de fundo
musica_fundo = None


def abrir_porta_da_sala(idx):
    porta = maps.PORTAS_SAIDA[idx]
    if porta is not None:
        l, c = porta
        maps.mapas[idx][l][c] = 2


# Inicializa a porta da sala 0
abrir_porta_da_sala(0)

if estado_salas[sala_atual] == "lutando":
    inimigos = entities.gerar_inimigos_para_sala(mapa)
else:
    inimigos = []


def trocar_sala(novo_index, entrar_pela_esquerda):
    global sala_atual, mapa, inimigos, ataque_ativo

    sala_atual = novo_index
    mapa = maps.mapas[sala_atual]
    ataque_ativo = False

    if estado_salas[sala_atual] == "lutando":
        inimigos = entities.gerar_inimigos_para_sala(mapa)
    else:
        inimigos = []

    if entrar_pela_esquerda:
        entities.personagem.x = config.TAMANHO_TILE * 1.2
    else:
        entities.personagem.x = config.janela.width - config.TAMANHO_TILE * 2.2

    entities.personagem.y = max(0, min(entities.personagem.y, config.janela.height - entities.personagem.height))


def posicionar_espada():
    cx = entities.personagem.x + entities.personagem.width / 2
    cy = entities.personagem.y + entities.personagem.height / 2

    if direcao == "right":
        entities.espada.x = entities.personagem.x + entities.personagem.width
        entities.espada.y = cy - entities.ESPADA_H / 2
    elif direcao == "left":
        entities.espada.x = entities.personagem.x - entities.ESPADA_W
        entities.espada.y = cy - entities.ESPADA_H / 2
    elif direcao == "down":
        entities.espada.x = cx - entities.ESPADA_W / 2
        entities.espada.y = entities.personagem.y + entities.personagem.height
    elif direcao == "up":
        entities.espada.x = cx - entities.ESPADA_W / 2
        entities.espada.y = entities.personagem.y - entities.ESPADA_H

    entities.espada.x = max(0, min(entities.espada.x, config.janela.width - entities.ESPADA_W))
    entities.espada.y = max(0, min(entities.espada.y, config.janela.height - entities.ESPADA_H))


def jogar():
    global direcao, ataque_ativo, ataque_timer, jogo_vencido, inimigos, mapa, musica_fundo

    # Inicia a música da primeira fase em loop
    musica_fundo = Sound("AUDIO/fase_01.mp3")
    musica_fundo.play()

    while True:
        delta = config.janela.delta_time()

        if config.janela.keyboard.key_pressed("esc"):
            musica_fundo.stop()  # Para a música caso saia para o menu
            break

        if jogo_vencido:
            config.janela.set_background_color((10, 60, 10))
            config.janela.draw_text("VOCE VENCEU O JOGO!", 280, 270, size=36, color=(255, 255, 0))
            config.janela.draw_text("Pressione ESC para sair", 400, 320, size=18, color=(255, 255, 255))
            config.janela.update()
            continue

        # --- Movimento Eixo X ---
        antigo_x = entities.personagem.x
        if config.janela.keyboard.key_pressed("left"):
            entities.personagem.x -= config.VELOCIDADE * delta
            direcao = "left"
        if config.janela.keyboard.key_pressed("right"):
            entities.personagem.x += config.VELOCIDADE * delta
            direcao = "right"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    entities.floor.x = coluna_idx * config.TAMANHO_TILE
                    entities.floor.y = linha_idx * config.TAMANHO_TILE
                    if entities.personagem.collided(entities.floor):
                        entities.personagem.x = antigo_x

        # --- Movimento Eixo Y ---
        antigo_y = entities.personagem.y
        if config.janela.keyboard.key_pressed("up"):
            entities.personagem.y -= config.VELOCIDADE * delta
            direcao = "up"
        if config.janela.keyboard.key_pressed("down"):
            entities.personagem.y += config.VELOCIDADE * delta
            direcao = "down"

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    entities.floor.x = coluna_idx * config.TAMANHO_TILE
                    entities.floor.y = linha_idx * config.TAMANHO_TILE
                    if entities.personagem.collided(entities.floor):
                        entities.personagem.y = antigo_y

        entities.personagem.x = max(0, min(entities.personagem.x, config.janela.width - entities.personagem.width))
        entities.personagem.y = max(0, min(entities.personagem.y, config.janela.height - entities.personagem.height))

        # --- Portas e Troca de Sala ---
        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 2 and sala_atual + 1 < len(maps.mapas):
                    entities.porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    entities.porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    if entities.personagem.collided(entities.porta_sprite):
                        trocar_sala(sala_atual + 1, entrar_pela_esquerda=True)
                elif tile == 3 and sala_atual - 1 >= 0:
                    entities.porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    entities.porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    if entities.personagem.collided(entities.porta_sprite):
                        trocar_sala(sala_atual - 1, entrar_pela_esquerda=False)

        # --- Sistema de Ataque ---
        if config.janela.keyboard.key_pressed("space") and not ataque_ativo:
            ataque_ativo = True
            ataque_timer = config.ATAQUE_DURACAO
            posicionar_espada()

        if ataque_ativo:
            ataque_timer -= delta
            posicionar_espada()

            inimigos_vivos = []
            for inimigo in inimigos:
                if entities.espada.collided(inimigo):
                    inimigo.vida -= 1
                    if inimigo.vida > 0:
                        inimigos_vivos.append(inimigo)
                else:
                    inimigos_vivos.append(inimigo)
            inimigos[:] = inimigos_vivos

            if ataque_timer <= 0:
                ataque_ativo = False

        # --- Estados das Salas e Derrota de Boss ---
        if estado_salas[sala_atual] == "lutando" and len(inimigos) == 0:
            estado_salas[sala_atual] = "chefe"
            inimigos = [entities.criar_chefe(mapa, sala_atual)]

        elif estado_salas[sala_atual] == "chefe" and len(inimigos) == 0:
            estado_salas[sala_atual] = "liberada"
            # SE FOR O PRIMEIRO BOSS (SALA_ATUAL == 1), TROCA A MÚSICA
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

        # --- Renderização (Refresh) ---
        config.janela.set_background_color((40, 40, 40))

        for linha_idx, linha in enumerate(mapa):
            for coluna_idx, tile in enumerate(linha):
                if tile == 1:
                    entities.floor.x = coluna_idx * config.TAMANHO_TILE
                    entities.floor.y = linha_idx * config.TAMANHO_TILE
                    entities.floor.draw()
                elif tile in (2, 3):
                    entities.porta_sprite.x = coluna_idx * config.TAMANHO_TILE
                    entities.porta_sprite.y = linha_idx * config.TAMANHO_TILE
                    entities.porta_sprite.draw()

        for inimigo in inimigos:
            inimigo.draw()

        entities.personagem.draw()

        if ataque_ativo:
            if (entities.espada.x >= 0 and entities.espada.y >= 0 and
                entities.espada.x + entities.ESPADA_W <= config.janela.width and
                entities.espada.y + entities.ESPADA_H <= config.janela.height):
                entities.espada.draw()

        # --- Interface (HUD) ---
        if estado_salas[sala_atual] == "lutando":
            config.janela.draw_text(f"Inimigos restantes: {len(inimigos)}", 10, 10, size=16, color=(255, 255, 255))
        elif estado_salas[sala_atual] == "chefe":
            vida_chefe = inimigos[0].vida if inimigos else 0
            config.janela.draw_text(f"CHEFE - vida: {vida_chefe}", 10, 10, size=16, color=(255, 60, 60))
        else:
            config.janela.draw_text("Sala liberada!", 10, 10, size=16, color=(120, 255, 120))

        config.janela.update()


if __name__ == "__main__":
    jogar()
