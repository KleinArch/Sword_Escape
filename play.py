from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *
import random

janela = Window(1000, 600)
janela.set_title("Jogo")

personagem = Sprite("PNG/personagem-1.png.png")
floor = Sprite("PNG/Brickwall5_Texture.png")

personagem.x = janela.width / 2 - personagem.width / 2
personagem.y = janela.height / 2 - personagem.height / 2

VELOCIDADE = 200  # pixels por segundo

inimigos = []  # lista de inimigos na tela
spawn_timer = 0
SPAWN_INTERVALO = 2  # segundos entre cada spawn

def jogar():
    global spawn_timer

    while True:
        delta = janela.delta_time()  # tempo desde o último frame

        # --- Sair ---
        if janela.keyboard.key_pressed("esc"):
            break

        # --- Movimento do personagem ---
        if janela.keyboard.key_pressed("left"):
            personagem.x -= VELOCIDADE * delta
        if janela.keyboard.key_pressed("right"):
            personagem.x += VELOCIDADE * delta
        if janela.keyboard.key_pressed("up"):
            personagem.y -= VELOCIDADE * delta
        if janela.keyboard.key_pressed("down"):
            personagem.y += VELOCIDADE * delta

        # Limitar o personagem dentro da janela
        personagem.x = max(0, min(personagem.x, janela.width - personagem.width))
        personagem.y = max(0, min(personagem.y, janela.height - personagem.height))

        # --- Spawn de inimigos ---
        """spawn_timer += delta
        if spawn_timer >= SPAWN_INTERVALO:
            inimigos.append(criar_inimigo())
            spawn_timer = 0"""

        # --- Desenhar ---
        floor.draw()
        personagem.draw()
        """for inimigo in inimigos:
            inimigo.draw()"""

        janela.update()


jogar()