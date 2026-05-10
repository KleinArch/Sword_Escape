from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(1000,600)
janela.set_title("Jogo")
personagem = Sprite("PNG/personagem-1.png.png")
floor = Sprite("PNG/Brickwall5_Texture.png")
slime_lv1 = Sprite("PNG/slime_lv1.png")

personagem.x = janela.width/2 - personagem.width/2
personagem.y = janela.height/2 - personagem.height/2

slime_lv1.x = 100
slime_lv1.y = 100


def jogar():

 while True:
    
    if(janela.keyboard.key_pressed("esc")):
                break


    floor.draw()
    personagem.draw()
    slime_lv1.draw()            
    janela.update()       
