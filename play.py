from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(1000,600)
janela.set_title("Jogo")


def jogar():

 while True:
    janela.set_background_color("blue")

    if(janela.keyboard.key_pressed("esc")):
                break

    janela.update()       
